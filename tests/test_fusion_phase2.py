"""Regression tests for fitted clusters and optional native C++ parity."""

import math

import pytest

from src.native_distance import DistanceBackend, python_distance
from src.trained_engine import TrainedClusterEngine
from src.recommender import Song, UserProfile


def catalog():
    return [
        Song(1, "Pop Energy", "Artist A", "pop", "happy", 0.9, 125, 0.9, 0.9, 0.1),
        Song(2, "Lofi Evening", "Artist B", "lofi", "chill", 0.3, 75, 0.5, 0.4, 0.9),
        Song(3, "Rock Anthem", "Artist C", "rock", "intense", 0.95, 145, 0.4, 0.6, 0.1),
        Song(4, "Pop Afternoon", "Artist D", "pop", "happy", 0.7, 110, 0.8, 0.8, 0.2),
    ]


def test_fitted_model_has_centroids_and_assignments():
    model = TrainedClusterEngine(catalog(), clusters=3)
    assert len(model.centroids) == 3
    assert len(model.assignments) == 4
    assert all(0 <= cluster < 3 for cluster in model.assignments)


def test_model_recommendations_are_explainable():
    model = TrainedClusterEngine(catalog())
    results = model.recommend(UserProfile("lofi", "chill", 0.3, True), k=2)
    assert results[0].song.id == 2
    assert len(results) == 2
    assert "Fitted k-means" in results[0].reasons[0]
    assert all(0 <= item.relevance <= 1 for item in results)


def test_training_is_reproducible():
    first = TrainedClusterEngine(catalog())
    second = TrainedClusterEngine(catalog())
    assert first.centroids == second.centroids
    assert first.assignments == second.assignments


def test_invalid_cluster_count():
    with pytest.raises(ValueError):
        TrainedClusterEngine(catalog(), clusters=0)


def test_zero_limit():
    model = TrainedClusterEngine(catalog())
    assert model.recommend(UserProfile("pop", "happy", 0.9, False), k=0) == []


@pytest.mark.parametrize("left,right", [
    ((0.0, 0.0), (3.0, 4.0)),
    ((0.1, 0.8), (0.2, 0.3)),
    ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])
def test_native_python_distance_parity(left, right):
    backend = DistanceBackend()
    assert backend.distance(left, right) == pytest.approx(
        python_distance(left, right), abs=1e-12
    )


def test_distance_invalid_dimensions():
    with pytest.raises(ValueError):
        DistanceBackend().distance((1.0,), (1.0, 2.0))


def test_distance_rejects_nan():
    with pytest.raises(ValueError):
        DistanceBackend().distance((math.nan,), (1.0,))
