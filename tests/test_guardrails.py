
"""Tests for recommendation input validation and guardrails."""

import pytest

from src.recommender import (
    UserProfile,
    score_song,
    validate_number,
    validate_preferences,
)
from src.evaluator import create_test_catalog


def test_valid_profile():
    """Valid listener preferences should be accepted."""
    profile = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.8,
        "likes_acoustic": False,
    }
    validate_preferences(profile)


@pytest.mark.parametrize("energy", [-0.1, 1.5, float("nan")])
def test_invalid_energy(energy):
    """Out-of-range and non-finite energy values are rejected."""
    with pytest.raises(ValueError):
        validate_number(energy, "energy")


def test_missing_genre():
    """A missing genre should produce a clear error."""
    with pytest.raises(ValueError, match="genre"):
        validate_preferences({
            "mood": "happy",
            "energy": 0.5,
        })


def test_invalid_song_data():
    """Malformed song data must not be scored."""
    song = vars(create_test_catalog()[0]).copy()
    song["energy"] = -1.0

    with pytest.raises(ValueError, match="energy"):
        score_song(
            {"genre": "pop", "mood": "happy", "energy": 0.8},
            song,
        )


def test_invalid_acoustic_preference():
    """Acoustic preference must be a boolean."""
    with pytest.raises(ValueError, match="likes_acoustic"):
        validate_preferences({
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "likes_acoustic": "yes",
        })


def test_negative_recommendation_limit():
    """Negative recommendation limits return no songs."""
    from src.recommender import Recommender

    recommender = Recommender(create_test_catalog())
    user = UserProfile("pop", "happy", 0.8, False)

    assert recommender.recommend(user, k=-1) == []
