import os
import pickle
from dataclasses import dataclass
from typing import Any, Optional

import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
LOCAL_DATA_PATH = os.path.join(DATA_DIR, "spotify_songs.csv")
EMBEDDING_PATH = os.path.join(BASE_DIR, "embeddings", "all-MiniLM-L6-v2.pkl")
DATA_URL = (
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/"
    "data/2020/2020-01-21/spotify_songs.csv"
)


@dataclass
class MusicData:
    df: pd.DataFrame
    embeddings: Any


def _load_embeddings(path: Optional[str] = None):
    if path is None:
        path = EMBEDDING_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing embedding file: {path}")
    with open(path, "rb") as f:
        payload = pickle.load(f)
    if isinstance(payload, dict) and "embeddings" in payload:
        return payload["embeddings"]
    return payload


def _load_dataset() -> pd.DataFrame:
    if os.path.exists(LOCAL_DATA_PATH):
        df = pd.read_csv(LOCAL_DATA_PATH)
    else:
        df = pd.read_csv(DATA_URL)

    df = df.reset_index(drop=True)
    required_columns = [
        "track_id",
        "track_name",
        "track_artist",
        "track_popularity",
        "playlist_genre",
        "playlist_subgenre",
        "valence",
        "energy",
        "duration_ms",
    ]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required dataset column: {col}")

    df["valence"] = pd.to_numeric(df["valence"], errors="coerce").fillna(0.5)
    df["track_popularity"] = pd.to_numeric(df["track_popularity"], errors="coerce").fillna(50)
    df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce").fillna(0).astype(int)

    return df


def load_music_data() -> MusicData:
    df = _load_dataset()
    embeddings = _load_embeddings()
    if hasattr(embeddings, "shape") and len(df) != embeddings.shape[0]:
        df = df.head(embeddings.shape[0]).reset_index(drop=True)
        embeddings = embeddings[: len(df)]
    return MusicData(df=df, embeddings=embeddings)
