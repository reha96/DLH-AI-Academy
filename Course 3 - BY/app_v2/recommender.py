import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional

GENRE_ALIASES = {
    "rock": ["rock"],
    "hip-hop": ["hip hop", "hip-hop", "hiphop", "rap"],
    "electronic": ["electronic", "edm", "dance"],
    "jazz": ["jazz"],
    "pop": ["pop"],
    "classical": ["classical"],
    "country": ["country"],
    "r&b / soul": ["r&b", "rnb", "soul"],
}

GENRE_EMOJIS = {
    "rock": "🎸",
    "hip-hop": "🎤",
    "electronic": "🎹",
    "jazz": "🎷",
    "pop": "💫",
    "classical": "🎻",
    "country": "🤠",
    "r&b / soul": "🎤",
    "mixed": "🎵",
}

POPULARITY_LABELS = {
    1: "Deep Underground",
    2: "Underground",
    3: "Indie",
    4: "Niche",
    5: "Mid-Stream",
    6: "Rising",
    7: "Popular",
    8: "Trending",
    9: "Mainstream",
    10: "Chart-Topper",
}


def popularity_label(value: int) -> str:
    return POPULARITY_LABELS.get(value, "Mid-Stream")


def normalize_text(value: Any) -> str:
    return str(value).strip().lower()


class MusicRecommender:
    def __init__(self, df, embeddings):
        self.df = df.copy()
        self.embeddings = embeddings
        self._index_columns = ["playlist_genre", "playlist_subgenre"]
        self._normalize_columns()

    def _normalize_columns(self):
        for column in self._index_columns:
            if column in self.df.columns:
                self.df[column] = self.df[column].fillna("").astype(str).apply(normalize_text)

    def _genre_matches(self, genre: str, row: dict) -> float:
        genre_key = normalize_text(genre)
        if genre_key == "mixed" or genre_key == "default":
            return 0.0
        alias_list = GENRE_ALIASES.get(genre_key, [genre_key])
        text = " ".join([row.get("playlist_genre", ""), row.get("playlist_subgenre", "")])
        for alias in alias_list:
            if alias in text:
                return 1.0
        return 0.0

    def _decade_matches(self, decade: str) -> np.ndarray:
        """Return an array of decade match scores (1.0 if match, 0.5 otherwise)."""
        decade_key = decade.strip().lower() if decade else ""
        decade_map = {
            "1970s": (1970, 1979),
            "1980s": (1980, 1989),
            "1990s": (1990, 1999),
            "2000s": (2000, 2009),
            "2010s": (2010, 2019),
            "2020s": (2020, 2029),
        }

        if decade_key not in decade_map:
            return np.ones(len(self.df))

        start_year, end_year = decade_map[decade_key]
        
        # Try different date columns
        release_years = None
        for col in ["track_album_release_date", "release_date"]:
            if col in self.df.columns:
                release_years = pd.to_numeric(
                    self.df[col].astype(str).str[:4], 
                    errors="coerce"
                ).fillna(2000).values.astype(int)
                break
        
        if release_years is None:
            return np.ones(len(self.df))
            
        mask = (release_years >= start_year) & (release_years <= end_year)
        return np.where(mask, 1.0, 0.5)

    def _get_emoji(self, genre: str, row: dict) -> str:
        genre_key = normalize_text(genre)
        if genre_key in GENRE_EMOJIS:
            return GENRE_EMOJIS[genre_key]
        for key, emoji in GENRE_EMOJIS.items():
            if key in normalize_text(row.get("playlist_genre", "")) or key in normalize_text(row.get("playlist_subgenre", "")):
                return emoji
        return "🎵"

    def _build_user_vector(self, target_valence: float, target_energy: float, liked_indices: np.ndarray = None) -> np.ndarray:
        """Build user preference vector from mood or liked songs."""
        if liked_indices is not None and len(liked_indices) > 0:
            return self.embeddings[liked_indices].mean(axis=0, keepdims=True)

        valence = self.df["valence"].astype(float).fillna(0.5).values
        energy = self.df["energy"].astype(float).fillna(0.5).values
        mood_mask = (
            np.abs(valence - target_valence) <= 0.20
            ) & (
            np.abs(energy - target_energy) <= 0.20
        )
        indices = np.flatnonzero(mood_mask)
        if len(indices) < 10:
            combined_distance = np.abs(valence - target_valence) + np.abs(energy - target_energy)
            indices = np.argsort(combined_distance)[:40]
        return self.embeddings[indices].mean(axis=0, keepdims=True)

    def _format_duration(self, duration_ms: int) -> str:
        seconds = int(duration_ms / 1000)
        minutes = seconds // 60
        remaining = seconds % 60
        return f"{minutes}:{remaining:02d}"

    def recommend(
        self,
        popularity: int,
        genre: str,
        target_valence: float,
        target_energy: float,
        k: int = 8,
        ratings: List[int] = None,
        decade: str = None,
        model: str = "hybrid",
        oversample_factor: float = 3.0,
        history_match: float = 0.5,  # 0 = diverse (ignore history), 1 = familiar (only history)
    ) -> List[Dict[str, Any]]:
        """
        Get recommendations using different models.

        Args:
            popularity: 1-10 popularity scale
            genre: Selected genre
            target_valence: 0-1 valence target
            target_energy: 0-1 energy target
            k: Number of recommendations desired
            ratings: List of user ratings (1-5)
            decade: Selected decade filter
            model: Model type - 'hybrid', 'content', 'collaborative'
            oversample_factor: Return k * oversample_factor candidates for filtering
            history_match: 0-1 scale where 0 = diverse recommendations (ignore rating history),
                          1 = familiar recommendations (only use rating history)
        """
        popularity = max(1, min(10, int(popularity)))
        popularity_norm = popularity / 10.0

        target_valence = float(np.clip(target_valence, 0.0, 1.0))
        target_energy = float(np.clip(target_energy, 0.0, 1.0))

        # Build user vector from liked songs (ratings >= 4) or from mood preference
        liked_indices = None
        if ratings and len(ratings) > 0:
            liked_indices = np.array([i for i, rating in enumerate(ratings) if rating >= 4])
            if len(liked_indices) == 0:
                liked_indices = None

        user_vec = self._build_user_vector(target_valence, target_energy, liked_indices)
        similarity = cosine_similarity(user_vec, self.embeddings)[0]

        valence = self.df["valence"].astype(float).fillna(0.5).values
        energy = self.df["energy"].astype(float).fillna(0.5).values
        valence_score = 1.0 - np.abs(valence - target_valence)
        energy_score = 1.0 - np.abs(energy - target_energy)
        pop_score = np.clip(self.df["track_popularity"].astype(float).fillna(50) / 100.0, 0.0, 1.0)

        genre_match = np.array([self._genre_matches(genre, row) for _, row in self.df.iterrows()])

        # Decade filter
        decade_score = np.ones(len(self.df))
        if decade and decade != "Mixed":
            decade_match = self._decade_matches(decade)
            decade_score = decade_match

        # Different model strategies
        if model == "content":
            # Pure content-based (embedding similarity)
            score = similarity
        elif model == "collaborative":
            # Popularity-weighted (simulates collaborative signals)
            score = 0.5 * similarity + 0.5 * pop_score
        else:  # hybrid
            # Full hybrid model with history_match control
            # history_match = 1: mostly embedding similarity (from rated items)
            # history_match = 0: mostly feature-based (valence, energy, popularity, genre)
            embedding_weight = 0.38 * history_match + 0.1 * (1 - history_match)
            feature_weight = 1 - history_match
            
            score = (
                embedding_weight * similarity
                + (0.22 + 0.1 * feature_weight) * valence_score
                + (0.22 + 0.1 * feature_weight) * energy_score
                + (0.13 + 0.1 * feature_weight) * pop_score
                + (0.05 + 0.05 * feature_weight) * genre_match
            ) * decade_score

        # Return oversampled candidates for iTunes filtering
        k_oversampled = int(k * oversample_factor)
        order = np.argsort(score)[::-1][:k_oversampled]
        
        recommendations = []
        seen_track_ids = set()
        
        for idx in order:
            row = self.df.iloc[idx]
            track_id = str(row["track_id"])
            
            # Skip duplicates
            if track_id in seen_track_ids:
                continue
            seen_track_ids.add(track_id)
            
            recommendation = {
                "track_id": track_id,
                "title": str(row["track_name"]),
                "artist": str(row["track_artist"]),
                "duration": self._format_duration(int(row["duration_ms"])),
                "match": f"{int(score[idx] * 100)}%",
                "genre": row.get("playlist_genre", "Mixed") or "Mixed",
                "emoji": self._get_emoji(genre, row.to_dict()),
                "valence": float(row["valence"]),
                "energy": float(row["energy"]),
                "_score": float(score[idx]),  # Keep for re-ranking
            }
            recommendations.append(recommendation)
        
        return recommendations
