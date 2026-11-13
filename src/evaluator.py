
"""VibeMatch Fusion | Automated Reliability Evaluation.

Evaluates deterministic ranking, recommendation explanations,
feature extraction, and consistency between recommendation APIs.

Future ML and C++ backends require separate integration tests.
"""

from dataclasses import dataclass

from src.recommender import (
    MAX_SCORE,
    Recommender,
    Song,
    UserProfile,
    extract_features,
)


@dataclass
class EvaluationResult:
    """Store the outcome of a single evaluation."""

    name: str
    passed: bool
    details: str


def create_test_catalog() -> list[Song]:
    """Create a reproducible music catalog."""

    return [
        Song(
            1, "Pop Energy", "Artist A",
            "pop", "happy", 0.9, 125,
            0.9, 0.9, 0.1,
        ),
        Song(
            2, "Lofi Evening", "Artist B",
            "lofi", "chill", 0.3, 75,
            0.5, 0.4, 0.9,
        ),
        Song(
            3, "Rock Anthem", "Artist C",
            "rock", "intense", 0.95, 145,
            0.4, 0.6, 0.1,
        ),
    ]


def run_check(name, check) -> EvaluationResult:
    """Run one check and capture its outcome."""

    try:
        passed = bool(check())

        details = (
            "Check passed"
            if passed
            else "Check failed"
        )

    except Exception as error:
        passed = False
        details = f"{type(error).__name__}: {error}"

    return EvaluationResult(name, passed, details)


def evaluate_recommender() -> list[EvaluationResult]:
    """Run the original and Fusion reliability checks."""

    recommender = Recommender(create_test_catalog())
    results = []

    profiles = [
        ("Pop preference", "pop", "happy", 0.9, 1),
        ("Lofi preference", "lofi", "chill", 0.3, 2),
        ("Rock preference", "rock", "intense", 0.95, 3),
    ]

    # Original ranking checks
    for name, genre, mood, energy, expected_id in profiles:
        user = UserProfile(genre, mood, energy, False)

        results.append(
            run_check(
                name,
                lambda user=user, expected_id=expected_id: (
                    bool(recommender.recommend(user, k=1))
                    and recommender.recommend(user, k=1)[0].id
                    == expected_id
                ),
            )
        )

    user = UserProfile("pop", "happy", 0.9, False)

    # Original reliability checks
    checks = [
        (
            "Zero-result handling",
            lambda: recommender.recommend(user, k=0) == [],
        ),
        (
            "Recommendation limit",
            lambda: len(
                recommender.recommend(user, k=2)
            ) == 2,
        ),
        (
            "Explanation quality",
            lambda: all(
                term in recommender.explain_recommendation(
                    user,
                    recommender.songs[0],
                )
                for term in (
                    "Genre match",
                    "Mood match",
                )
            ),
        ),

        # New Fusion-specific checks
        (
            "Feature-vector extraction",
            lambda: extract_features(
                vars(recommender.songs[0])
            ) == (0.9, 0.9, 0.9, 0.1),
        ),
        (
            "Detailed ranking consistency",
            lambda: [
                result.song.id
                for result in recommender.recommend_detailed(
                    user, k=3
                )
            ] == [
                song.id
                for song in recommender.recommend(
                    user, k=3
                )
            ],
        ),
        (
            "Normalized relevance bounds",
            lambda: all(
                0.0 <= result.relevance <= 1.0
                and 0.0 <= result.score <= MAX_SCORE
                for result in recommender.recommend_detailed(
                    user, k=3
                )
            ),
        ),
        (
            "Deterministic recommendations",
            lambda: [
                song.id
                for song in recommender.recommend(user, k=3)
            ] == [
                song.id
                for song in recommender.recommend(user, k=3)
            ],
        ),
    ]

    for name, check in checks:
        results.append(run_check(name, check))

    return results


def main() -> None:
    """Print evaluation results and fail on any failed check."""

    results = evaluate_recommender()
    passed = sum(result.passed for result in results)
    total = len(results)

    print("\nVIBEMATCH FUSION - RELIABILITY REPORT")
    print("-" * 50)

    for result in results:
        status = "PASS" if result.passed else "FAIL"

        print(
            f"[{status}] {result.name}: {result.details}"
        )

    print("-" * 50)
    print(f"Checks passed: {passed}/{total}")
    print(
        f"Pass rate: {passed / total:.0%}"
        if total else "No checks"
    )

    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
