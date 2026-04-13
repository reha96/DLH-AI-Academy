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
        mood=payload.mood,
        popularity=payload.popularity,
        genre=genre_choice,
        k=10,
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
