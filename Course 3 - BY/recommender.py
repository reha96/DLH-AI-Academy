import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any

MOOD_VALENCE = {
    "Depressed": 0.10,
    "Sad": 0.20,
    "Anxious": 0.30,
    "Tired": 0.35,
    "Neutral": 0.50,
    "Calm": 0.60,
    "Content": 0.70,
    "Happy": 0.80,
    "Energetic": 0.90,
    "Euphoric": 0.95,
}

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

    def _get_emoji(self, genre: str, row: dict) -> str:
        genre_key = normalize_text(genre)
        if genre_key in GENRE_EMOJIS:
            return GENRE_EMOJIS[genre_key]
        for key, emoji in GENRE_EMOJIS.items():
            if key in normalize_text(row.get("playlist_genre", "")) or key in normalize_text(row.get("playlist_subgenre", "")):
                return emoji
        return "🎵"

    def _build_user_vector(self, mood_val: float) -> np.ndarray:
        valence = self.df["valence"].astype(float).fillna(0.5).values
        mood_mask = np.abs(valence - mood_val) <= 0.20
        indices = np.flatnonzero(mood_mask)
        if len(indices) < 10:
            indices = np.argsort(np.abs(valence - mood_val))[:40]
        return self.embeddings[indices].mean(axis=0, keepdims=True)

    def _format_duration(self, duration_ms: int) -> str:
        seconds = int(duration_ms / 1000)
        minutes = seconds // 60
        remaining = seconds % 60
        return f"{minutes}:{remaining:02d}"

    def recommend(self, mood: str, popularity: int, genre: str, k: int = 8) -> List[Dict[str, Any]]:
        mood_val = MOOD_VALENCE.get(mood, 0.50)
        popularity = max(1, min(10, int(popularity)))
        popularity_norm = popularity / 10.0

        user_vec = self._build_user_vector(mood_val)
        similarity = cosine_similarity(user_vec, self.embeddings)[0]

        valence = self.df["valence"].astype(float).fillna(0.5).values
        valence_score = 1.0 - np.abs(valence - mood_val)
        pop_score = np.clip(self.df["track_popularity"].astype(float).fillna(50) / 100.0, 0.0, 1.0)

        genre_match = np.array([self._genre_matches(genre, row) for _, row in self.df.iterrows()])

        score = (
            0.45 * similarity
            + 0.25 * valence_score
            + 0.20 * pop_score
            + 0.10 * genre_match
        )

        order = np.argsort(score)[::-1][:k]
        recommendations = []
        for idx in order:
            row = self.df.iloc[idx]
            recommendation = {
                "track_id": str(row["track_id"]),
                "title": str(row["track_name"]),
                "artist": str(row["track_artist"]),
                "duration": self._format_duration(int(row["duration_ms"])),
                "match": f"{int(score[idx] * 100)}%",
                "genre": row.get("playlist_genre", "Mixed") or "Mixed",
                "emoji": self._get_emoji(genre, row.to_dict()),
            }
            recommendations.append(recommendation)
        return recommendations
