
"""VibeMatch Fusion | Portable Nearest-Neighbor Recommendation Engine.

Uses weighted feature vectors and Euclidean distance to recommend
similar songs without NumPy or scikit-learn.

Compatible with Python 3.13 and designed for future C++ integration.
"""

import math
from dataclasses import asdict
from typing import Sequence

from src.recommender import (
    MAX_SCORE,
    RecommendationResult,
    Song,
    UserProfile,
    validate_preferences,
    validate_song,
)


class MusicAIEngine:
    """Generate music recommendations using feature similarity."""

    def __init__(self, songs: Sequence[Song]):
        """Validate songs and construct the feature-vector index."""
        if not songs:
            raise ValueError("The music catalog must not be empty.")

        self.songs = list(songs)

        for song in self.songs:
            if not isinstance(song, Song):
                raise TypeError("Catalog entries must be Song objects.")
            validate_song(asdict(song))

        self.genres = sorted({
            song.genre.casefold().strip()
            for song in self.songs
        })

        self.moods = sorted({
            song.mood.casefold().strip()
            for song in self.songs
        })

        self.genre_index = {
            value: index
            for index, value in enumerate(self.genres)
        }

        self.mood_index = {
            value: index
            for index, value in enumerate(self.moods)
        }

        self.catalog_vectors = [
            self._song_vector(song)
            for song in self.songs
        ]

    def _vector(
        self,
        genre: str,
        mood: str,
        energy: float,
        acoustic: float,
    ) -> tuple[float, ...]:
        """Encode categorical and numerical music features."""
        vector = [
            0.0
            for _ in range(
                len(self.genres) + len(self.moods) + 2
            )
        ]

        genre_index = self.genre_index.get(
            genre.casefold().strip()
        )

        mood_index = self.mood_index.get(
            mood.casefold().strip()
        )

        if genre_index is not None:
            vector[genre_index] = math.sqrt(2.0)

        if mood_index is not None:
            vector[len(self.genres) + mood_index] = 1.0

        vector[-2] = energy
        vector[-1] = math.sqrt(0.5) * acoustic

        return tuple(vector)

    def _song_vector(
        self,
        song: Song,
    ) -> tuple[float, ...]:
        """Encode the features of one song."""
        return self._vector(
            song.genre,
            song.mood,
            song.energy,
            song.acousticness,
        )

    @staticmethod
    def _distance(
        first: tuple[float, ...],
        second: tuple[float, ...],
    ) -> float:
        """Calculate Euclidean distance between two feature vectors."""
        if len(first) != len(second):
            raise ValueError("Feature vector dimensions must match.")

        return math.sqrt(
            sum(
                (a - b) ** 2
                for a, b in zip(first, second)
            )
        )

    def recommend(
        self,
        user: UserProfile,
        k: int = 5,
    ) -> list[RecommendationResult]:
        """Return ranked song matches with transparent explanations."""
        if not isinstance(user, UserProfile):
            raise TypeError("user must be a UserProfile instance.")

        validate_preferences(asdict(user))

        if isinstance(k, bool) or not isinstance(k, int):
            raise TypeError("k must be an integer.")

        if k <= 0:
            return []

        query = self._vector(
            user.favorite_genre,
            user.favorite_mood,
            user.target_energy,
            1.0 if user.likes_acoustic else 0.0,
        )

        ranked = []

        for song, vector in zip(
            self.songs,
            self.catalog_vectors,
        ):
            distance = self._distance(query, vector)
            ranked.append((distance, song))

        ranked.sort(
            key=lambda entry: (entry[0], entry[1].id)
        )

        results = []

        for distance, song in ranked[:k]:
            score = round(
                MAX_SCORE / (1.0 + distance),
                4,
            )

            reasons = [
                "Nearest-neighbor feature matching",
                f"Feature distance: {distance:.3f} (lower is closer)",
                (
                    "Genre matched"
                    if song.genre.casefold()
                    == user.favorite_genre.casefold()
                    else "Genre differs"
                ),
                (
                    "Mood matched"
                    if song.mood.casefold()
                    == user.favorite_mood.casefold()
                    else "Mood differs"
                ),
                (
                    "Energy difference: "
                    f"{abs(song.energy - user.target_energy):.2f}"
                ),
            ]

            results.append(
                RecommendationResult(
                    song=song,
                    score=score,
                    reasons=reasons,
                )
            )

        return results
