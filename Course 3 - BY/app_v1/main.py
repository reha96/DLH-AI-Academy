import json
import os
import urllib.parse
import urllib.request
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from data_loader import load_music_data
from recommender import MusicRecommender, popularity_label

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="BeatRec Recommender")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

music_data = load_music_data()
recommender = MusicRecommender(music_data.df, music_data.embeddings)


class RecommendationRequest(BaseModel):
    name: str = "Listener"
    mood: str
    popularity: int
    selected_genres: Optional[List[str]] = None
    genre: Optional[str] = None
    decade: Optional[str] = None
    ratings: Optional[List[int]] = None
    valence: Optional[float] = None
    energy: Optional[float] = None


class RecommendationSong(BaseModel):
    track_id: str
    title: str
    artist: str
    duration: str
    match: str
    genre: str
    emoji: str
    preview_url: Optional[str] = None


class RecommendationResponse(BaseModel):
    name: str
    mood: str
    genre: str
    popularity: int
    popularity_label: str
    recommendations: List[RecommendationSong]


@app.get("/", response_class=FileResponse)
def home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


def fetch_itunes_preview(title: str, artist: str) -> Optional[str]:
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


def query_itunes_tracks(term: str, limit: int = 8):
    try:
        query = urllib.parse.quote(term)
        url = f"https://itunes.apple.com/search?term={query}&media=music&entity=song&limit={limit}&explicit=No"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            tracks = []
            for item in data.get("results", []):
                preview = item.get("previewUrl")
                if not preview:
                    continue
                tracks.append({
                    "title": item.get("trackName", "Unknown"),
                    "artist": item.get("artistName", "Unknown"),
                    "preview_url": preview,
                    "artwork_url": item.get("artworkUrl100"),
                })
            return tracks
    except Exception:
        return []


@app.get("/api/itunes-search")
def itunes_search(term: str = "top hits", limit: int = 8):
    return {"tracks": query_itunes_tracks(term, limit)}


@app.get("/api/sample-rating-songs")
def sample_rating_songs(genres: Optional[str] = None):
    """Sample 5 songs from the dataset, optionally filtered by genres."""
    import numpy as np
    from recommender import normalize_text
    
    df = music_data.df.copy()
    
    if genres:
        genre_list = [g.strip() for g in genres.split(',') if g.strip()]
        genre_list = [normalize_text(g) for g in genre_list]
        mask = df.apply(
            lambda row: any(
                g in normalize_text(row.get("playlist_genre", "")) or 
                g in normalize_text(row.get("playlist_subgenre", ""))
                for g in genre_list
            ),
            axis=1
        )
        df = df[mask]
    
    if len(df) < 5:
        df = music_data.df.copy()
    
    sample_df = df.sample(n=min(5, len(df)), random_state=None)
    tracks = []
    for _, row in sample_df.iterrows():
        preview_url = fetch_itunes_preview(row["track_name"], row["track_artist"])
        tracks.append({
            "title": str(row["track_name"]),
            "artist": str(row["track_artist"]),
            "preview_url": preview_url,
            "duration_ms": int(row["duration_ms"]),
        })
    return {"tracks": tracks}


@app.post("/api/recommend", response_model=RecommendationResponse)
def recommend(payload: RecommendationRequest):
    popularity_label_text = popularity_label(payload.popularity)
    genre_choice = None
    if payload.selected_genres:
        genre_choice = payload.selected_genres[0]
    elif payload.genre:
        genre_choice = payload.genre
    else:
        genre_choice = "Mixed"

    recommendations = recommender.recommend(
        popularity=payload.popularity,
        genre=genre_choice,
        target_valence=payload.valence or 0.5,
        target_energy=payload.energy or 0.5,
        k=10,
        ratings=payload.ratings,
        decade=payload.decade,
    )

    decorated = []
    for rec in recommendations:
        rec_copy = rec.copy()
        rec_copy["preview_url"] = fetch_itunes_preview(rec["title"], rec["artist"])
        decorated.append(rec_copy)

    return RecommendationResponse(
        name=payload.name or "Listener",
        mood=payload.mood,
        genre=genre_choice,
        popularity=payload.popularity,
        popularity_label=popularity_label_text,
        recommendations=decorated,
    )
