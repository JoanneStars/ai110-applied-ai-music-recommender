"""VibeMatch Fusion: portable, similarity-based music recommendation.

Uses Python's standard library, with no scikit-learn or native DLLs.
This is a nearest-neighbor algorithm, not a fitted predictive model.
"""

from dataclasses import asdict
from math import sqrt
from typing import Sequence

from src.native_distance import DistanceBackend

from src.recommender import (
    MAX_SCORE,
    RecommendationResult,
    Song,
    UserProfile,
    extract_features,
    validate_preferences,
    validate_song,
)


class MusicAIEngine:
    """Rank songs using weighted distances in a musical feature space."""

    def __init__(self, songs: Sequence[Song]):
        if not songs:
            raise ValueError("The music catalog cannot be empty.")

        self.songs = list(songs)
        self.backend = DistanceBackend()
        self.vectors = []
        for song in self.songs:
            data = asdict(song)
            validate_song(data)
            self.vectors.append(extract_features(data))

    def _distance(self, user: UserProfile, song: Song, vector: tuple) -> float:
        """Combine genre/mood mismatch and numerical feature distance."""
        energy, _valence, _danceability, acousticness = vector
        target_acousticness = 1.0 if user.likes_acoustic else 0.0

        genre_mismatch = (
            0.0 if song.genre.casefold() == user.favorite_genre.casefold()
            else 1.0
        )
        mood_mismatch = (
            0.0 if song.mood.casefold() == user.favorite_mood.casefold()
            else 1.0
        )

        # Only user-selected features influence numerical distance.
        # Valence and danceability are stored for future preference controls.
        return self.backend.distance(
            (
                2.0 * genre_mismatch,
                sqrt(2.0) * mood_mismatch,
                energy,
                0.5 * acousticness,
            ),
            (
                0.0,
                0.0,
                user.target_energy,
                0.5 * target_acousticness,
            ),
        )

    def recommend(
        self, user: UserProfile, k: int = 5
    ) -> list[RecommendationResult]:
        """Return k nearest songs with normalized relevance and explanations."""
        if not isinstance(k, int) or isinstance(k, bool):
            raise ValueError("k must be an integer.")
        if k <= 0:
            return []

        validate_preferences(asdict(user))
        ranked = []
        for song, vector in zip(self.songs, self.vectors):
            distance = self._distance(user, song, vector)
            relevance = 1.0 / (1.0 + distance)
            score = round(MAX_SCORE * relevance, 4)
            reasons = [
                f"Computation backend: {self.backend.backend}",
                f"Similarity distance: {distance:.3f}",
                f"Energy difference: {abs(song.energy - user.target_energy):.2f}",
            ]
            if song.genre.casefold() == user.favorite_genre.casefold():
                reasons.append("Genre match")
            if song.mood.casefold() == user.favorite_mood.casefold():
                reasons.append("Mood match")
            reasons.append(
                "Acoustic preference: "
                + ("acoustic" if user.likes_acoustic else "non-acoustic")
            )
            ranked.append((distance, RecommendationResult(song, score, reasons)))

        ranked.sort(key=lambda item: item[0])
        return [result for _, result in ranked[:k]]
