
"""Automated tests for VibeMatch Fusion reliability evaluation."""

import pytest

from src.evaluator import (
    EvaluationResult,
    create_test_catalog,
    evaluate_recommender,
    main,
)
from src.recommender import (
    Recommender,
    Song,
    UserProfile,
)


def test_catalog_contains_valid_songs():
    """Verify the evaluation catalog contains valid songs."""
    songs = create_test_catalog()

    assert len(songs) == 3
    assert all(isinstance(song, Song) for song in songs)
    assert {song.id for song in songs} == {1, 2, 3}


def test_evaluator_returns_ten_results():
    """Verify all ten reliability checks execute."""
    results = evaluate_recommender()

    assert len(results) == 10
    assert all(
        isinstance(result, EvaluationResult)
        for result in results
    )


def test_evaluator_checks_pass():
    """Verify every reliability evaluation passes."""
    results = evaluate_recommender()

    assert all(result.passed for result in results), [
        result.details
        for result in results
        if not result.passed
    ]


@pytest.mark.parametrize(
    "genre,mood,energy,expected_id",
    [
        ("pop", "happy", 0.9, 1),
        ("lofi", "chill", 0.3, 2),
        ("rock", "intense", 0.95, 3),
    ],
)
def test_recommendation_ranking(
    genre,
    mood,
    energy,
    expected_id,
):
    """Verify recommendation rankings for three profiles."""
    recommender = Recommender(create_test_catalog())

    user = UserProfile(
        favorite_genre=genre,
        favorite_mood=mood,
        target_energy=energy,
        likes_acoustic=False,
    )

    recommendations = recommender.recommend(user, k=1)

    assert len(recommendations) == 1
    assert recommendations[0].id == expected_id


def test_evaluator_prints_summary(capsys):
    """Verify the evaluation report contains correct metrics."""
    main()

    output = capsys.readouterr().out

    assert "VIBEMATCH FUSION" in output
    assert "RELIABILITY REPORT" in output
    assert "Checks passed: 10/10" in output
    assert "Pass rate: 100%" in output


def test_evaluator_handles_zero_recommendations():
    """Verify requesting zero recommendations returns an empty list."""
    recommender = Recommender(create_test_catalog())

    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.9,
        likes_acoustic=False,
    )

    recommendations = recommender.recommend(user, k=0)

    assert recommendations == []
