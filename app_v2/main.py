import json
import os
import urllib.parse
import urllib.request
from typing import List, Optional

import pandas as pd
from flask import Flask, render_template, request, jsonify, session, redirect, Blueprint
from flask_compress import Compress
from functools import wraps

from data_loader import load_all_embeddings, get_embedding_models, EmbeddingLibrary
from recommender import MusicRecommender, popularity_label
from model_manager import ModelManager

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Support subpath deployment (e.g., rehatuncer.com/beatrec)
SUBPATH = os.environ.get("SUBPATH", "").strip("/")

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
app.secret_key = os.environ.get("SECRET_KEY", "beatrec-secret-key-change-in-production")

# Enable gzip compression for faster load times
app.config['COMPRESS_ALGORITHM'] = 'gzip'
app.config['COMPRESS_LEVEL'] = 6  # Balance between speed and compression ratio
app.config['COMPRESS_MIN_SIZE'] = 500  # Only compress responses larger than 500 bytes
Compress(app)


def create_bp():
    """Create and configure the Blueprint with all routes."""
    bp = Blueprint('beatrec', __name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
    bp.secret_key = app.secret_key

    # Load dataset and embedding metadata (but NOT the actual embeddings yet)
    embedding_library: EmbeddingLibrary = None
    model_manager: ModelManager = None

    def initialize_models():
        """
        Initialize the embedding library and model manager.
        
        Memory optimization: Only loads the dataset and embedding metadata,
        not the actual embedding vectors. Models are loaded on-demand via
        the ModelManager with LRU caching.
        """
        nonlocal embedding_library, model_manager
        
        print("Loading dataset and embedding metadata...")
        embedding_library = load_all_embeddings()
        
        # ModelManager with LRU caching (max 2 models in memory at once)
        # This reduces memory from ~670MB (all models) to ~150MB (2 largest models)
        model_manager = ModelManager(embedding_library, max_cached_models=2)
        
        print(f"Initialized ModelManager with {len(model_manager.get_available_models())} models")
        print(f"Available models: {model_manager.get_available_models()}")

    initialize_models()

    def fetch_itunes_track(title: str, artist: str) -> dict:
        """Fetch track info (preview URL + album art) from iTunes API.
        
        Validates that the returned song matches the searched title/artist
        to ensure correct album art and preview data.
        """
        result = {
            "preview_url": None,
            "artwork_url": None,
            "itunes_title": None,
            "itunes_artist": None,
        }
        try:
            query = urllib.parse.quote(f"{title} {artist}")
            url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=5"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                results = data.get("results", [])
                
                if not results:
                    return result
                
                # Find best matching result
                best_match = None
                best_score = 0
                
                for track in results:
                    itunes_title = track.get("trackName", "").lower()
                    itunes_artist = track.get("artistName", "").lower()
                    search_title = title.lower().strip()
                    search_artist = artist.lower().strip()
                    
                    # Calculate match score
                    score = 0
                    
                    # Artist match (most important)
                    if search_artist in itunes_artist or itunes_artist in search_artist:
                        score += 50
                    elif any(word in itunes_artist for word in search_artist.split()):
                        score += 25
                    
                    # Title match
                    if search_title in itunes_title or itunes_title in search_title:
                        score += 50
                    elif any(word in itunes_title for word in search_title.split()):
                        score += 25
                    
                    # Exact match bonus
                    if search_title == itunes_title and search_artist == itunes_artist:
                        score += 100
                    
                    if score > best_score:
                        best_score = score
                        best_match = track
                
                # Use best match if score is reasonable (at least 50)
                if best_match and best_score >= 50:
                    result["preview_url"] = best_match.get("previewUrl")
                    result["itunes_title"] = best_match.get("trackName")
                    result["itunes_artist"] = best_match.get("artistName")
                    
                    # Get higher resolution artwork (600x600)
                    artwork = best_match.get("artworkUrl100", "")
                    if artwork:
                        result["artwork_url"] = artwork.replace("100x100bb", "600x600bb")
                        
        except Exception as e:
            print(f"iTunes API error for '{title}' by '{artist}': {e}")
            
        return result

    def fetch_itunes_preview(title: str, artist: str) -> Optional[str]:
        """Fetch preview URL from iTunes API."""
        result = fetch_itunes_track(title, artist)
        return result.get("preview_url")

    @bp.context_processor
    def inject_subpath():
        """Inject subpath into all templates for constructing correct URLs."""
        subpath = SUBPATH.strip("/") if SUBPATH else ""
        prefix = f"/{subpath}" if subpath else ""
        return {"subpath": subpath, "url_prefix": prefix}

    @bp.route("/")
    def home():
        """Welcome Page."""
        return render_template("welcome.html")

    @bp.route("/rate-songs")
    def rate_songs():
        """Page 1: User Persona Creation - Material UI."""
        return render_template("page1_profile_material.html")

    @bp.route("/select-genres")
    def select_genres():
        """Page 2: Genre Selection."""
        return render_template("genre_selection.html")

    @bp.route("/preferences")
    def preferences():
        """Page 3: Preferences (Valence/Energy, genres, decades)."""
        return render_template("page2_preferences.html")

    @bp.route("/recommendations")
    def recommendations():
        """Page 4: Song Recommendations."""
        return render_template("page3_recommendations.html")

    def _find_itunes_available_song(df: pd.DataFrame, genre: str, exclude_track_ids: set) -> tuple:
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

    @bp.route("/api/sample-songs", methods=["GET"])
    def sample_songs():
        """Get sample songs for rating.
        
        If genres are provided (user selected specific genres), sample 5 songs from those genres.
        If no genres provided (default behavior), sample 1 song per genre from all genres.

        Songs are sampled from the full dataset. If a song is not available on iTunes,
        it is replaced with another song from the same genre that is available.
        """
        genres = request.args.get("genres", "")
        df = embedding_library.df.copy()
        use_default_behavior = False

        # Filter by genres if provided
        if genres:
            genre_list = [g.strip().lower() for g in genres.split(",") if g.strip()]
            if genre_list:  # Explicit check for non-empty list
                mask = df["playlist_genre"].str.lower().isin(genre_list)
                df_filtered = df[mask]
                
                # Check if filtered dataframe has data
                if len(df_filtered) > 0:
                    df = df_filtered
                else:
                    # No matching genres, use default behavior
                    use_default_behavior = True
            else:
                # Empty genre list after filtering, use default behavior
                use_default_behavior = True
        else:
            # No genres provided, use default behavior (1 song per genre)
            use_default_behavior = True

        if use_default_behavior:
            # Default behavior: sample 1 song from each genre (max 6 total)
            unique_genres = df["playlist_genre"].unique()
            
            # Limit to 6 genres if there are more
            if len(unique_genres) > 6:
                unique_genres = pd.Series(unique_genres).sample(n=6, random_state=None).tolist()
            
            sampled_indices = []
            for genre in unique_genres:
                genre_df = df[df["playlist_genre"] == genre]
                if len(genre_df) > 0:
                    sampled = genre_df.sample(n=1, random_state=None)
                    sampled_indices.extend(sampled.index.tolist())

            sampled_df = df.loc[sampled_indices]
        else:
            # Sample 6 songs from selected genres with diversity
            n_samples = min(6, len(df))
            unique_genres = df["playlist_genre"].unique()

            if len(unique_genres) > 1 and n_samples > len(unique_genres):
                # Ensure at least 1 song per genre, then distribute remaining
                sampled_indices = []
                for genre in unique_genres:
                    genre_df = df[df["playlist_genre"] == genre]
                    if len(genre_df) > 0:
                        sampled = genre_df.sample(n=1, random_state=None)
                        sampled_indices.extend(sampled.index.tolist())

                # Fill remaining slots
                remaining_count = n_samples - len(sampled_indices)
                if remaining_count > 0:
                    remaining_df = df[~df.index.isin(sampled_indices)]
                    if len(remaining_df) > 0:
                        remaining = remaining_df.sample(n=min(remaining_count, len(remaining_df)), random_state=None)
                        sampled_indices.extend(remaining.index.tolist())

                sampled_df = df.loc[sampled_indices]
            else:
                sampled_df = df.sample(n=n_samples, random_state=None)

        tracks = []
        excluded_track_ids = set()

        for _, row in sampled_df.iterrows():
            itunes_data = fetch_itunes_track(row["track_name"], row["track_artist"])
            preview_url = itunes_data.get("preview_url")
            artwork_url = itunes_data.get("artwork_url")

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
                    artwork_url = fetch_itunes_track(row["track_name"], row["track_artist"]).get("artwork_url")
                    excluded_track_ids.add(row["track_id"])

            tracks.append({
                "track_id": str(row["track_id"]),
                "title": str(row["track_name"]),
                "artist": str(row["track_artist"]),
                "preview_url": preview_url,
                "artwork_url": artwork_url,
                "duration_ms": int(row["duration_ms"]),
                "genre": row.get("playlist_genre", "Unknown"),
            })

        return jsonify({"tracks": tracks})

    @bp.route("/api/genres", methods=["GET"])
    def get_genres():
        """Get unique genres from dataset."""
        genres = sorted(embedding_library.df["playlist_genre"].dropna().unique().tolist())
        return jsonify({"genres": genres})

    @bp.route("/api/embedding-models", methods=["GET"])
    def get_embedding_models_api():
        """Get list of available embedding models."""
        models = model_manager.get_available_models()
        default = model_manager.get_default_model()
        return jsonify({"models": models, "default": default})

    @bp.route("/api/decades", methods=["GET"])
    def get_decades():
        """Get unique decades from dataset."""
        # Use the pre-computed decade column
        decades = sorted(embedding_library.df["decade"].dropna().unique().tolist())
        return jsonify({"decades": decades})

    @bp.route("/api/recommend", methods=["POST"])
    def recommend():
        """Get song recommendations based on user preferences."""
        data = request.json
        
        # DEBUG: Log raw received data
        print("[BeatRec API] === RECEIVED REQUEST /api/recommend ===")
        print("[BeatRec API] Raw data keys:", data.keys() if data else "NO DATA")
        
        ratings = data.get("ratings", [])  # List of {track_id, rating}
        valence = float(data.get("valence", 0.5))
        energy = float(data.get("energy", 0.5))
        mainstream = float(data.get("mainstream", 0.5))  # 0-1 scale
        diversity = float(data.get("diversity", 0.5))  # 0-1 scale (0 = familiar/high history match, 1 = diverse/low history match)
        selected_genres = data.get("genres", [])
        decade = data.get("decade", "Mixed")
        model = data.get("model", "hybrid")  # Recommendation model: hybrid, content, collaborative
        embedding_model = data.get("embedding_model", "MiniLM")  # Embedding model

        # DEBUG: Log extracted parameters
        print("[BeatRec API] Extracted parameters:")
        print(f"[BeatRec API]   valence: {valence}")
        print(f"[BeatRec API]   energy: {energy}")
        print(f"[BeatRec API]   mainstream: {mainstream}")
        print(f"[BeatRec API]   diversity: {diversity}")
        print(f"[BeatRec API]   genres: {selected_genres}")
        print(f"[BeatRec API]   decade: {decade}")
        print(f"[BeatRec API]   model: {model}")
        print(f"[BeatRec API]   embedding_model: {embedding_model}")
        print(f"[BeatRec API]   ratings count: {len(ratings) if ratings else 0}")
        print("[BeatRec API] ===========================================")

        # Convert ratings to list of integers
        # Handles both formats: [{track_id, rating}, ...] or [rating, ...]
        rating_values = []
        if ratings:
            for r in ratings:
                if isinstance(r, dict):
                    rating_values.append(r.get("rating", 3))
                elif isinstance(r, (int, float)):
                    rating_values.append(int(r))
                else:
                    rating_values.append(3)  # Default rating

        # Get the recommender for the selected embedding model (lazy-loaded)
        selected_recommender = model_manager.get_recommender(embedding_model)
        if selected_recommender is None:
            # Fallback to default model if selected model not found
            default_model = model_manager.get_default_model()
            if default_model:
                selected_recommender = model_manager.get_recommender(default_model)
            if selected_recommender is None:
                return jsonify({"error": "No embedding models available"}), 500

        # Get recommendations (oversampled for iTunes filtering)
        genre_choice = selected_genres[0] if selected_genres else "Mixed"
        k_target = 5  # We want exactly 5 recommendations with iTunes previews

        # Convert diversity to history_match (reversed: diversity 0 = history_match 1, diversity 1 = history_match 0)
        history_match = 1 - diversity

        candidates = selected_recommender.recommend(
            popularity=int(mainstream * 10),
            genre=genre_choice,
            target_valence=valence,
            target_energy=energy,
            k=k_target,
            ratings=rating_values,
            decade=decade,
            model=model,  # Use selected recommendation model
            history_match=history_match,  # Pass the converted value
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
                itunes_data = fetch_itunes_track(candidate["title"], candidate["artist"])
                itunes_checked.add(track_id)

                if itunes_data.get("preview_url"):
                    candidate["preview_url"] = itunes_data["preview_url"]
                    candidate["artwork_url"] = itunes_data.get("artwork_url")
                    recommendations.append(candidate)
                    seen_track_ids.add(track_id)

                    if len(recommendations) >= k_target:
                        break

        # Clean up internal fields
        for rec in recommendations:
            rec.pop("_score", None)

        return jsonify({"recommendations": recommendations})

    @bp.route("/feedback")
    def feedback():
        """Feedback Page - Step 6 of 6."""
        return render_template("feedback.html")

    @bp.route("/api/feedback", methods=["POST"])
    def submit_feedback():
        """Save user feedback to CSV."""
        import csv
        import os
        from datetime import datetime

        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract feedback data
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "accuracy": data.get("accuracy"),
            "diversity": data.get("diversity"),
            "serendipity": data.get("serendipity"),
            "usability": data.get("usability"),
            "comment": data.get("comment", ""),
            "session_name": data.get("session", {}).get("name", "Anonymous"),
            "session_genres": ",".join(data.get("session", {}).get("genres", [])),
            "session_valence": data.get("session", {}).get("valence"),
            "session_energy": data.get("session", {}).get("energy"),
            "session_mainstream": data.get("session", {}).get("mainstream"),
            "session_diversity": data.get("session", {}).get("diversity"),
            "session_decade": data.get("session", {}).get("decade"),
            "session_model": data.get("session", {}).get("model"),  # hybrid/content/collaborative
            "embedding_model": data.get("embedding_model", "MiniLM"),  # NEW: MiniLM/MPNet/etc.
            "num_ratings": len(data.get("session", {}).get("ratings", []))
        }

        # Define CSV file path
        feedback_file = os.path.join(BASE_DIR, "feedback_results.csv")

        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(feedback_file)

        try:
            with open(feedback_file, "a", newline="", encoding="utf-8") as f:
                fieldnames = [
                    "timestamp", "accuracy", "diversity", "serendipity", "usability",
                    "comment", "session_name", "session_genres", "session_valence",
                    "session_energy", "session_mainstream", "session_diversity",
                    "session_decade", "session_model", "embedding_model", "num_ratings"
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                writer.writerow(feedback_data)

            return jsonify({"message": "Feedback saved successfully"}), 200
        except Exception as e:
            print(f"Error saving feedback: {e}")
            return jsonify({"error": "Failed to save feedback"}), 500

    @bp.route("/admin/dashboard")
    def admin_dashboard():
        """Admin Dashboard - View feedback analytics."""
        return render_template("admin_dashboard.html")

    @bp.route("/api/admin/feedback-data", methods=["GET"])
    def get_feedback_data():
        """Get feedback data for admin dashboard, grouped by embedding model."""
        import csv
        import os
        from collections import defaultdict

        feedback_file = os.path.join(BASE_DIR, "feedback_results.csv")

        if not os.path.exists(feedback_file):
            return jsonify({"feedback": [], "by_model": {}}), 200

        try:
            feedback_data = []
            model_data = defaultdict(lambda: {
                'ratings': [],
                'accuracy': [],
                'diversity': [],
                'serendipity': [],
                'usability': [],
                'liked_songs': 0,
                'count': 0
            })
            
            with open(feedback_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    feedback_data.append(row)
                    
                    # Group by embedding_model (not session_model)
                    model = row.get('embedding_model', 'Unknown')
                    model_data[model]['count'] += 1
                    model_data[model]['ratings'].append(
                        (float(row.get('accuracy', 0) or 0) +
                         float(row.get('diversity', 0) or 0) +
                         float(row.get('serendipity', 0) or 0) +
                         float(row.get('usability', 0) or 0)) / 4
                    )
                    model_data[model]['accuracy'].append(float(row.get('accuracy', 0) or 0))
                    model_data[model]['diversity'].append(float(row.get('diversity', 0) or 0))
                    model_data[model]['serendipity'].append(float(row.get('serendipity', 0) or 0))
                    model_data[model]['usability'].append(float(row.get('usability', 0) or 0))
                    model_data[model]['liked_songs'] += int(row.get('num_ratings', 0) or 0)

            # Calculate averages per model
            by_model = {}
            for model, data in model_data.items():
                by_model[model] = {
                    'avg_rating': sum(data['ratings']) / len(data['ratings']) if data['ratings'] else 0,
                    'liked_songs': data['liked_songs'],
                    'avg_accuracy': sum(data['accuracy']) / len(data['accuracy']) if data['accuracy'] else 0,
                    'avg_diversity': sum(data['diversity']) / len(data['diversity']) if data['diversity'] else 0,
                    'avg_serendipity': sum(data['serendipity']) / len(data['serendipity']) if data['serendipity'] else 0,
                    'avg_usability': sum(data['usability']) / len(data['usability']) if data['usability'] else 0,
                    'response_count': data['count']
                }

            return jsonify({"feedback": feedback_data, "by_model": by_model}), 200
        except Exception as e:
            print(f"Error reading feedback data: {e}")
            return jsonify({"error": "Failed to read feedback data"}), 500

    @bp.route("/admin/export-feedback", methods=["GET"])
    def export_feedback():
        """Export feedback data as CSV download."""
        import csv
        import os
        from flask import send_file
        from io import StringIO

        feedback_file = os.path.join(BASE_DIR, "feedback_results.csv")

        if not os.path.exists(feedback_file):
            # Return empty CSV with headers
            output = StringIO()
            fieldnames = [
                "timestamp", "accuracy", "diversity", "serendipity", "usability",
                "comment", "session_name", "session_genres", "session_valence",
                "session_energy", "session_mainstream", "session_diversity",
                "session_decade", "session_model", "num_ratings"
            ]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            # Create a BytesIO for the empty CSV
            from io import BytesIO
            output_bytes = BytesIO(output.getvalue().encode('utf-8'))
            output_bytes.name = "feedback_results.csv"
            return send_file(
                output_bytes,
                mimetype="text/csv",
                as_attachment=True,
                download_name="feedback_results.csv"
            )

        return send_file(
            feedback_file,
            mimetype="text/csv",
            as_attachment=True,
            download_name="feedback_results.csv"
        )

    return bp


# Register blueprint with URL prefix if SUBPATH is set
if SUBPATH:
    bp = create_bp()
    app.register_blueprint(bp, url_prefix="/" + SUBPATH)
    
    # Redirect root to subpath
    @app.route("/")
    def root_redirect():
        return redirect("/" + SUBPATH)
else:
    bp = create_bp()
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
