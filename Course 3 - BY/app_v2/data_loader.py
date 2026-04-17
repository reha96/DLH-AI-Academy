import os
import pickle
from dataclasses import dataclass
from typing import Any, Optional, Dict

import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
LOCAL_DATA_PATH = os.path.join(DATA_DIR, "spotify_songs.csv")

# Support multiple embedding paths for flexibility (local dev + Render deployment)
EMBEDDINGS_DIRS = [
    os.path.join(BASE_DIR, "embeddings"),  # Local copy in app_v2/embeddings
    os.path.join(BASE_DIR, "..", "embeddings"),  # Root embeddings folder
    os.path.join(BASE_DIR, "..", "..", "embeddings"),  # Two levels up
    "/app/embeddings",  # Render mounted disk
]

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
    """
    Holds multiple embedding models with lazy-loading support.
    
    Embeddings are loaded on-demand when get_embeddings() is called,
    then cached for subsequent requests.
    """
    df: pd.DataFrame
    embeddings_dict: Dict[str, Dict[str, Any]]  # model_name -> metadata dict

    def get_embeddings(self, model_name: str) -> Any:
        """
        Get embeddings for a specific model, loading on-demand if needed.
        
        Args:
            model_name: Display name of the embedding model (e.g., 'MiniLM', 'MPNet')
        
        Returns:
            The embedding array/matrix for the requested model
        """
        if model_name not in self.embeddings_dict:
            # Fallback to first available model
            if self.embeddings_dict:
                first_model = next(iter(self.embeddings_dict))
                print(f"Model '{model_name}' not found, using '{first_model}' instead")
                return self.get_embeddings(first_model)
            raise ValueError(f"No embeddings available for model: {model_name}")
        
        model_meta = self.embeddings_dict[model_name]
        
        # Already loaded, return cached data
        if model_meta.get("loaded", False):
            return model_meta["data"]
        
        # Load on-demand
        path = model_meta["path"]
        print(f"Loading embedding model: {model_name} from {path}")
        
        with open(path, "rb") as f:
            payload = pickle.load(f)

        if isinstance(payload, dict) and "embeddings" in payload:
            embeddings = payload["embeddings"]
        else:
            embeddings = payload

        # Ensure embeddings match dataframe length
        if hasattr(embeddings, "shape") and len(self.df) != embeddings.shape[0]:
            embeddings = embeddings[:len(self.df)]
        
        # Cache for subsequent requests
        model_meta["data"] = embeddings
        model_meta["loaded"] = True
        
        print(f"Loaded {model_name}: {embeddings.shape}, dtype={embeddings.dtype}")
        return embeddings


def _find_embeddings_dir():
    """Find the first available embeddings directory."""
    for dir_path in EMBEDDINGS_DIRS:
        if os.path.exists(dir_path):
            return dir_path
    return None


def load_all_embeddings() -> EmbeddingLibrary:
    """
    Load dataset and embedding metadata (file paths), but NOT the actual embedding vectors.
    
    Memory optimization: This function now only loads the dataset and discovers
    available embedding models. The actual embedding vectors are loaded on-demand
    by the ModelManager when a specific model is requested.
    """
    df = _load_dataset()
    embeddings_dict = {}

    # Find the embeddings directory
    embeddings_dir = _find_embeddings_dir()
    if embeddings_dir is None:
        raise FileNotFoundError(
            f"No embeddings directory found. Searched: {EMBEDDINGS_DIRS}"
        )

    # Only store metadata (file paths), not the actual embeddings
    available_models = get_embedding_models(embeddings_dir)
    
    for display_name, file_prefix in available_models.items():
        path = os.path.join(embeddings_dir, f"{file_prefix}.pkl")
        # Store path metadata, load actual embeddings on-demand
        embeddings_dict[display_name] = {
            "file_prefix": file_prefix,
            "path": path,
            "loaded": False,
            "data": None
        }
        print(f"Registered embedding model: {display_name} ({file_prefix})")

    if not embeddings_dict:
        raise FileNotFoundError(
            f"No embedding models found in {embeddings_dir}. Searched: {EMBEDDINGS_DIRS}"
        )

    return EmbeddingLibrary(df=df, embeddings_dict=embeddings_dict)


def get_embedding_models(embeddings_dir: Optional[str] = None) -> Dict[str, str]:
    """Return available embedding models (display_name -> file_prefix)."""
    if embeddings_dir is None:
        embeddings_dir = _find_embeddings_dir()
    
    if embeddings_dir is None:
        return {}

    available = {}
    for display_name, file_prefix in EMBEDDING_MODELS.items():
        embedding_path = os.path.join(embeddings_dir, f"{file_prefix}.pkl")
        if os.path.exists(embedding_path):
            available[display_name] = file_prefix

    return available


def _load_dataset() -> pd.DataFrame:
    """
    Load dataset with optimized column selection and dtypes.
    
    Memory optimizations:
    - Only load required columns (reduces CSV parsing overhead)
    - Use efficient dtypes: int32 instead of int64, float32 instead of float64
    - Use categorical types for repeated string columns
    """
    # Only load required columns to reduce memory
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
        "track_album_release_date",
    ]
    
    if os.path.exists(LOCAL_DATA_PATH):
        df = pd.read_csv(LOCAL_DATA_PATH, usecols=required_columns)
    else:
        df = pd.read_csv(DATA_URL, usecols=required_columns)

    df = df.reset_index(drop=True)
    
    # Validate required columns
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

    # Optimize dtypes for memory efficiency
    # int32 saves 50% vs int64, float32 saves 50% vs float64
    # Note: track_id may be string (UUID), keep as object
    df["track_popularity"] = pd.to_numeric(df["track_popularity"], errors="coerce").fillna(50).astype("int8")
    df["valence"] = pd.to_numeric(df["valence"], errors="coerce").fillna(0.5).astype("float32")
    df["energy"] = pd.to_numeric(df["energy"], errors="coerce").fillna(0.5).astype("float32")
    df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce").fillna(0).astype("int32")
    
    # Convert genre columns to categorical (saves ~80% memory on string columns)
    df["playlist_genre"] = df["playlist_genre"].astype("category")
    df["playlist_subgenre"] = df["playlist_subgenre"].astype("category")
    
    # Keep text columns as object (needed for string operations)
    df["track_name"] = df["track_name"].astype("object")
    df["track_artist"] = df["track_artist"].astype("object")
    # track_id may be string (UUID), keep as object

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
    df["decade"] = df["decade"].astype("category")

    # Log memory optimization results
    print(f"Dataset loaded: {len(df)} tracks, {len(df.columns)} columns")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    return df


def load_music_data() -> MusicData:
    df = _load_dataset()
    embeddings = _load_embeddings()
    if hasattr(embeddings, "shape") and len(df) != embeddings.shape[0]:
        df = df.head(embeddings.shape[0]).reset_index(drop=True)
        embeddings = embeddings[: len(df)]
    return MusicData(df=df, embeddings=embeddings)
