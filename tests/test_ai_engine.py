
"""Tests for VibeMatch's fitted nearest-neighbor engine."""

import pytest

from src.ai_engine import MusicAIEngine
from src.recommender import Song, UserProfile


@pytest.fixture
def engine():
    songs = [
        Song(1, "Pop", "A", "pop", "happy", 0.90, 125, 0.8, 0.9, 0.1),
        Song(2, "Lofi", "B", "lofi", "chill", 0.25, 80, 0.4, 0.4, 0.9),
        Song(3, "Rock", "C", "rock", "intense", 0.95, 145, 0.3, 0.6, 0.1),
    ]
    return MusicAIEngine(songs)


def test_pop_profile_prefers_pop(engine):
    result = engine.recommend(
        UserProfile("pop", "happy", 0.9, False), k=1
    )
    assert result[0].song.id == 1


def test_acoustic_lofi_profile_prefers_lofi(engine):
    result = engine.recommend(
        UserProfile("lofi", "chill", 0.25, True), k=1
    )
    assert result[0].song.id == 2


def test_results_include_explanations(engine):
    results = engine.recommend(
        UserProfile("rock", "intense", 0.95, False), k=2
    )
    assert len(results) == 2
    assert all(
        r.reasons and 0.0 <= r.relevance <= 1.0
        for r in results
    )


def test_invalid_energy_is_rejected(engine):
    with pytest.raises(ValueError):
        engine.recommend(
            UserProfile("pop", "happy", 2.0, False)
        )


def test_zero_limit(engine):
    assert engine.recommend(
        UserProfile("pop", "happy", 0.9, False), 0
    ) == []


def test_empty_catalog_is_rejected():
    with pytest.raises(ValueError):
        MusicAIEngine([])
