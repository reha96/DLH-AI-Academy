import json
import os
import urllib.parse
import urllib.request
from typing import List, Optional

import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from functools import wraps

from data_loader import load_all_embeddings, get_embedding_models, EmbeddingLibrary
from recommender import MusicRecommender, popularity_label

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
app.secret_key = "beatrec-secret-key-change-in-production"

# Load all embedding models
embedding_library: EmbeddingLibrary = None
recommenders: dict = {}  # model_name -> MusicRecommender


def load_all_models():
    """Load all embedding models and create recommenders for each."""
    global embedding_library, recommenders
    embedding_library = load_all_embeddings()
    recommenders = {}
    
    for model_name in embedding_library.embeddings_dict.keys():
        embeddings = embedding_library.get_embeddings(model_name)
        recommenders[model_name] = MusicRecommender(embedding_library.df, embeddings)
        print(f"Initialized recommender for: {model_name}")


load_all_models()


def fetch_itunes_preview(title: str, artist: str) -> Optional[str]:
    """Fetch preview URL from iTunes API."""
    try:
        query = urllib.parse.quote(f"{title} {artist}")
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            results = data.get("results", [])
            if results:
                return results[0].get("previewUrl")
    except Exception:
        return None
    return None


@app.route("/")
def home():
    """Page 1: User Persona Creation."""
    return render_template("page1_profile.html")


@app.route("/preferences")
def preferences():
    """Page 2: Preferences (Valence/Energy, genres, decades)."""
    return render_template("page2_preferences.html")


@app.route("/recommendations")
def recommendations():
    """Page 3: Song Recommendations."""
    return render_template("page3_recommendations.html")


def _find_itunes_available_song(df: pd.DataFrame, genre: str, exclude_track_ids: set) -> Optional[pd.Series]:
    """Find a song in the given genre that has a preview URL available on iTunes."""
    genre_df = df[df["playlist_genre"].str.lower() == genre.lower()].copy()
    genre_df = genre_df[~genre_df["track_id"].isin(exclude_track_ids)]
    
    # Shuffle to get random candidates
    genre_df = genre_df.sample(frac=1, random_state=None)
    
    for _, row in genre_df.iterrows():
        preview_url = fetch_itunes_preview(row["track_name"], row["track_artist"])
        if preview_url:
            return row, preview_url
    
    return None, None


@app.route("/api/sample-songs", methods=["GET"])
def sample_songs():
    """Get 10 sample songs for rating (optionally filtered by selected genres).

    Songs are sampled from the full dataset. If a song is not available on iTunes,
    it is replaced with another song from the same genre that is available.
    """
    import numpy as np

    genres = request.args.get("genres", "")
    df = embedding_library.df.copy()

    # Filter by genres if provided
    if genres:
        genre_list = [g.strip().lower() for g in genres.split(",") if g.strip()]
        mask = df["playlist_genre"].str.lower().isin(genre_list)
        df = df[mask]

    # Sample 10 songs
    n_samples = min(10, len(df))
    if n_samples < 10:
        # If not enough, sample from full dataset
        df = embedding_library.df.copy()
        n_samples = min(10, len(df))

    # Sample from different genres for diversity
    unique_genres = df["playlist_genre"].unique()
    sampled_indices = []
    per_genre = max(1, n_samples // len(unique_genres))

    for genre in unique_genres:
        genre_df = df[df["playlist_genre"] == genre]
        n_take = min(per_genre, len(genre_df))
        sampled = genre_df.sample(n=n_take, random_state=None)
        sampled_indices.extend(sampled.index.tolist())

    # Fill remaining if needed
    while len(sampled_indices) < n_samples:
        remaining = [i for i in df.index.tolist() if i not in sampled_indices]
        if not remaining:
            break
        sampled_indices.append(np.random.choice(remaining))

    sampled_df = df.loc[sampled_indices[:n_samples]]

    tracks = []
    excluded_track_ids = set()

    for _, row in sampled_df.iterrows():
        preview_url = fetch_itunes_preview(row["track_name"], row["track_artist"])

        # If no preview URL found, try to find a replacement from the same genre
        if not preview_url:
            genre = row.get("playlist_genre", "Unknown")
            excluded_track_ids.add(row["track_id"])
            replacement_row, replacement_url = _find_itunes_available_song(
                embedding_library.df, genre, excluded_track_ids
            )
            if replacement_row is not None:
                row = replacement_row
                preview_url = replacement_url
                excluded_track_ids.add(row["track_id"])
        
        tracks.append({
            "track_id": str(row["track_id"]),
            "title": str(row["track_name"]),
            "artist": str(row["track_artist"]),
            "preview_url": preview_url,
            "duration_ms": int(row["duration_ms"]),
            "genre": row.get("playlist_genre", "Unknown"),
        })

    return jsonify({"tracks": tracks})


@app.route("/api/genres", methods=["GET"])
def get_genres():
    """Get unique genres from dataset."""
    genres = sorted(embedding_library.df["playlist_genre"].dropna().unique().tolist())
    return jsonify({"genres": genres})


@app.route("/api/embedding-models", methods=["GET"])
def get_embedding_models_api():
    """Get list of available embedding models."""
    models = list(get_embedding_models().keys())
    return jsonify({"models": models, "default": "MiniLM"})


@app.route("/api/decades", methods=["GET"])
def get_decades():
    """Get unique decades from dataset."""
    # Use the pre-computed decade column
    decades = sorted(embedding_library.df["decade"].dropna().unique().tolist())
    return jsonify({"decades": decades})


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """Get song recommendations based on user preferences."""
    import pandas as pd

    data = request.json
    ratings = data.get("ratings", [])  # List of {track_id, rating}
    valence = float(data.get("valence", 0.5))
    energy = float(data.get("energy", 0.5))
    mainstream = float(data.get("mainstream", 0.5))  # 0-1 scale
    history_match = float(data.get("history_match", 0.5))  # 0-1 scale
    selected_genres = data.get("genres", [])
    decade = data.get("decade", "Mixed")
    embedding_model = data.get("embedding_model", "MiniLM")  # Selected embedding model

    # Convert ratings to list of integers
    rating_values = [r.get("rating", 3) for r in ratings] if ratings else None

    # Get the recommender for the selected embedding model
    selected_recommender = recommenders.get(embedding_model, recommenders.get("MiniLM"))
    if selected_recommender is None:
        selected_recommender = next(iter(recommenders.values()))

    # Get recommendations (oversampled for iTunes filtering)
    genre_choice = selected_genres[0] if selected_genres else "Mixed"
    k_target = 5  # We want exactly 5 recommendations with iTunes previews
    
    candidates = selected_recommender.recommend(
        popularity=int(mainstream * 10),
        genre=genre_choice,
        target_valence=valence,
        target_energy=energy,
        k=k_target,
        ratings=rating_values,
        decade=decade,
        model="hybrid",  # Always use hybrid scoring
        oversample_factor=4.0,  # Get 20 candidates to filter from
    )

    # Verify iTunes availability and collect 5 unique songs
    recommendations = []
    seen_track_ids = set()
    itunes_checked = set()
    
    for candidate in candidates:
        track_id = candidate["track_id"]
        
        # Skip if already in final recommendations
        if track_id in seen_track_ids:
            continue
        
        # Check iTunes availability
        if track_id not in itunes_checked:
            preview_url = fetch_itunes_preview(candidate["title"], candidate["artist"])
            itunes_checked.add(track_id)
            
            if preview_url:
                candidate["preview_url"] = preview_url
                recommendations.append(candidate)
                seen_track_ids.add(track_id)
                
                if len(recommendations) >= k_target:
                    break
    
    # Clean up internal fields
    for rec in recommendations:
        rec.pop("_score", None)

    return jsonify({"recommendations": recommendations})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
