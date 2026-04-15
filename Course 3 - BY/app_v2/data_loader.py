import os
import pickle
from dataclasses import dataclass
from typing import Any, Optional, Dict

import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
LOCAL_DATA_PATH = os.path.join(DATA_DIR, "spotify_songs.csv")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "..", "embeddings")
DATA_URL = (
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/"
    "data/2020/2020-01-21/spotify_songs.csv"
)


# Mapping of display names to embedding file prefixes
EMBEDDING_MODELS = {
    "MiniLM": "all-MiniLM-L6-v2",
    "MPNet": "all-mpnet-base-v2",
    "BAAI": "BAAI-bge-m3",
    "ColBERT": "colbert-ir-colbertv2.0",
    "MxBAI": "mixedbread-ai-mxbai-embed-large-v1",
    "MultiQA": "multi-qa-MiniLM-L6-cos-v1",
    "SPLADE": "naver-splade-cocondenser-ensembledistil",
    "Snowflake": "Snowflake-snowflake-arctic-embed-l-v2.0",
    "GTE": "thenlper-gte-large",
}


@dataclass
class MusicData:
    df: pd.DataFrame
    embeddings: Any


@dataclass
class EmbeddingLibrary:
    """Holds multiple embedding models for selection at runtime."""
    df: pd.DataFrame
    embeddings_dict: Dict[str, Any]  # model_name -> embeddings
    
    def get_embeddings(self, model_name: str) -> Any:
        """Get embeddings for a specific model."""
        if model_name in self.embeddings_dict:
            return self.embeddings_dict[model_name]
        # Fallback to first available model
        if self.embeddings_dict:
            return next(iter(self.embeddings_dict.values()))
        raise ValueError(f"No embeddings available for model: {model_name}")


def load_all_embeddings() -> EmbeddingLibrary:
    """Load all available embedding models."""
    df = _load_dataset()
    embeddings_dict = {}
    
    available_models = get_embedding_models()
    for display_name, file_prefix in available_models.items():
        try:
            path = os.path.join(EMBEDDINGS_DIR, f"{file_prefix}.pkl")
            with open(path, "rb") as f:
                payload = pickle.load(f)
            
            if isinstance(payload, dict) and "embeddings" in payload:
                embeddings = payload["embeddings"]
            else:
                embeddings = payload
            
            # Ensure embeddings match dataframe length
            if hasattr(embeddings, "shape") and len(df) != embeddings.shape[0]:
                embeddings = embeddings[:len(df)]
            
            embeddings_dict[display_name] = embeddings
            print(f"Loaded embedding model: {display_name} ({file_prefix})")
        except Exception as e:
            print(f"Warning: Could not load embedding {display_name}: {e}")
    
    if not embeddings_dict:
        raise FileNotFoundError("No embedding models found in the embeddings directory")
    
    return EmbeddingLibrary(df=df, embeddings_dict=embeddings_dict)


def get_embedding_models() -> Dict[str, str]:
    """Return available embedding models (display_name -> file_prefix)."""
    available = {}
    if not os.path.exists(EMBEDDINGS_DIR):
        return available
    
    for display_name, file_prefix in EMBEDDING_MODELS.items():
        embedding_path = os.path.join(EMBEDDINGS_DIR, f"{file_prefix}.pkl")
        if os.path.exists(embedding_path):
            available[display_name] = file_prefix
    
    return available


def _load_embeddings(path: Optional[str] = None, model_name: str = "MiniLM"):
    if path is None:
        # Find the embedding file based on model name
        available = get_embedding_models()
        file_prefix = available.get(model_name, EMBEDDING_MODELS.get(model_name, "all-MiniLM-L6-v2"))
        path = os.path.join(EMBEDDINGS_DIR, f"{file_prefix}.pkl")
    
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

    # Drop tracks with missing track_name or track_artist
    original_count = len(df)
    df = df.dropna(subset=["track_name", "track_artist"])
    df = df[df["track_name"].astype(str).str.strip() != ""]
    df = df[df["track_artist"].astype(str).str.strip() != ""]
    dropped_count = original_count - len(df)
    if dropped_count > 0:
        print(f"Data cleaning: dropped {dropped_count} tracks with missing/empty track_name or track_artist")
        print(f"Remaining tracks: {len(df)}")

    df = df.reset_index(drop=True)

    df["valence"] = pd.to_numeric(df["valence"], errors="coerce").fillna(0.5)
    df["track_popularity"] = pd.to_numeric(df["track_popularity"], errors="coerce").fillna(50)
    df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce").fillna(0).astype(int)

    # Extract decade from track_album_release_date
    def extract_decade(date_str):
        if pd.isna(date_str):
            return None
        try:
            year = int(str(date_str)[:4])
            if 1900 <= year <= 2099:
                return str(year // 10 * 10) + "s"
        except (ValueError, TypeError):
            pass
        return None

    df["decade"] = df["track_album_release_date"].apply(extract_decade)

    return df


def load_music_data() -> MusicData:
    df = _load_dataset()
    embeddings = _load_embeddings()
    if hasattr(embeddings, "shape") and len(df) != embeddings.shape[0]:
        df = df.head(embeddings.shape[0]).reset_index(drop=True)
        embeddings = embeddings[: len(df)]
    return MusicData(df=df, embeddings=embeddings)
