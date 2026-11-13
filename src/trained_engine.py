"""VibeMatch Fusion: fitted, unsupervised k-means music recommender.

This *trains* cluster centroids on the catalog's energy and acousticness,
then uses centroid proximity plus genre/mood constraints to rank songs.
No listener feedback is used. With 15 songs the learned clusters are only
an educational demonstration, not evidence of real-world recommendation quality.
"""

from __future__ import annotations

from dataclasses import asdict
from math import isfinite
from typing import Sequence

from src.native_distance import DistanceBackend, python_distance
from src.recommender import (
    MAX_SCORE, RecommendationResult, Song, UserProfile,
    validate_preferences, validate_song,
)


class TrainedClusterEngine:
    """Fit deterministic k-means centroids on two audio dimensions."""

    def __init__(self, songs: Sequence[Song], clusters: int = 3,
                 backend: DistanceBackend | None = None):
        if not songs:
            raise ValueError("Music catalog cannot be empty.")
        self.songs = list(songs)
        for song in self.songs:
            if not isinstance(song, Song):
                raise TypeError("Catalog entries must be Song objects.")
            validate_song(asdict(song))
        if isinstance(clusters, bool) or not isinstance(clusters, int) or clusters < 1:
            raise ValueError("clusters must be a positive integer.")
        self.backend = backend or DistanceBackend()
        self.points = [
            (float(song.energy), float(song.acousticness))
            for song in self.songs
        ]
        self.k = min(clusters, len(self.points))
        self.centroids, self.assignments = self._fit()

    def _nearest_center(self, point, centroids):
        return min(
            range(len(centroids)),
            key=lambda index: (python_distance(point, centroids[index]), index),
        )

    def _fit(self):
        """Farthest-first initialized, batch k-means; deterministic and bounded."""
        centroids = [self.points[0]]
        while len(centroids) < self.k:
            candidate = max(
                self.points,
                key=lambda point: min(
                    python_distance(point, center) for center in centroids
                ),
            )
            if candidate in centroids:
                candidate = next((p for p in self.points if p not in centroids),
                                 centroids[-1])
            centroids.append(candidate)

        assignments = []
        for _ in range(50):
            new_assignments = [
                self._nearest_center(point, centroids) for point in self.points
            ]
            updated = list(centroids)
            for cluster_id in range(self.k):
                members = [
                    point for point, label in zip(self.points, new_assignments)
                    if label == cluster_id
                ]
                if members:
                    updated[cluster_id] = tuple(
                        sum(point[d] for point in members) / len(members)
                        for d in range(2)
                    )
            if new_assignments == assignments and all(
                python_distance(a, b) < 1e-12
                for a, b in zip(centroids, updated)
            ):
                break
            assignments = new_assignments
            centroids = updated
        return tuple(centroids), tuple(assignments)

    def recommend(self, user: UserProfile, k: int = 5) -> list[RecommendationResult]:
        if not isinstance(user, UserProfile):
            raise TypeError("user must be a UserProfile instance.")
        validate_preferences(asdict(user))
        if isinstance(k, bool) or not isinstance(k, int):
            raise TypeError("k must be an integer.")
        if k <= 0:
            return []

        target = (user.target_energy, 1.0 if user.likes_acoustic else 0.0)
        ranked = []
        for song, point, group in zip(self.songs, self.points, self.assignments):
            direct = self.backend.distance(target, point)
            learned = self.backend.distance(target, self.centroids[group])
            genre_penalty = 1.4 if song.genre.casefold() != user.favorite_genre.casefold() else 0.0
            mood_penalty = 0.8 if song.mood.casefold() != user.favorite_mood.casefold() else 0.0
            distance = 0.7 * direct + 0.3 * learned + genre_penalty + mood_penalty
            score = round(MAX_SCORE / (1.0 + distance), 4)
            reasons = [
                "Fitted k-means cluster model (unsupervised)",
                f"Learned cluster: {group + 1} of {self.k}",
                f"Song feature distance: {direct:.3f}",
                f"Cluster centroid distance: {learned:.3f}",
                "Genre matched" if genre_penalty == 0 else "Genre differs",
                "Mood matched" if mood_penalty == 0 else "Mood differs",
                f"Computation backend: {self.backend.backend}",
            ]
            ranked.append((distance, song.id, RecommendationResult(song, score, reasons)))
        ranked.sort(key=lambda item: (item[0], item[1]))
        return [result for _, _, result in ranked[:k]]
