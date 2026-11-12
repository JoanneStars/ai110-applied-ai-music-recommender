
"""Unit tests for the music recommendation evaluator."""

import pytest

from src.evaluator import (
    EvaluationResult,
    create_test_catalog,
    evaluate_recommender,
    main,
)
from src.recommender import Recommender, UserProfile


def test_catalog_contains_valid_songs():
    """Verify that evaluation songs have valid attributes."""
    songs = create_test_catalog()

    assert len(songs) == 3
    assert len({song.id for song in songs}) == len(songs)
    assert all(0 <= song.energy <= 1 for song in songs)
    assert all(0 <= song.acousticness <= 1 for song in songs)


def test_evaluator_returns_six_results():
    """Verify all evaluation checks execute."""
    results = evaluate_recommender()

    assert len(results) == 6
    assert all(isinstance(r, EvaluationResult) for r in results)


def test_evaluator_checks_pass():
    """Verify the recommender passes the baseline checks."""
    results = evaluate_recommender()

    failures = [r for r in results if not r.passed]

    assert not failures, (
        "Evaluation failures: "
        + ", ".join(f"{r.name}: {r.details}" for r in failures)
    )


@pytest.mark.parametrize(
    "genre,mood,energy,expected_id",
    [
        ("pop", "happy", 0.9, 1),
        ("lofi", "chill", 0.3, 2),
        ("rock", "intense", 0.95, 3),
    ],
)
def test_recommendation_ranking(
    genre, mood, energy, expected_id
):
    """Verify the top result matches the expected profile."""
    recommender = Recommender(create_test_catalog())
    user = UserProfile(genre, mood, energy, False)

    results = recommender.recommend(user, k=1)

    assert len(results) == 1
    assert results[0].id == expected_id


def test_evaluator_prints_summary(capsys):
    """Verify the evaluation report contains useful metrics."""
    main()
    output = capsys.readouterr().out

    assert "RELIABILITY REPORT" in output
    assert "Tests passed:" in output
    assert "Pass rate:" in output


def test_evaluator_handles_zero_recommendations():
    """Verify zero requested recommendations return no songs."""
    recommender = Recommender(create_test_catalog())
    user = UserProfile("pop", "happy", 0.9, False)

    assert recommender.recommend(user, k=0) == []
