
"""Automated reliability evaluation for the music recommender."""

from dataclasses import dataclass
from src.recommender import Song, UserProfile, Recommender


@dataclass
class EvaluationResult:
    """Store the outcome of a single evaluation."""
    name: str
    passed: bool
    details: str


def create_test_catalog() -> list[Song]:
    """Create a reproducible catalog for evaluation."""
    return [
        Song(1, "Pop Energy", "Artist A", "pop", "happy",
             0.9, 125, 0.9, 0.9, 0.1),
        Song(2, "Lofi Evening", "Artist B", "lofi", "chill",
             0.3, 75, 0.5, 0.4, 0.9),
        Song(3, "Rock Anthem", "Artist C", "rock", "intense",
             0.95, 145, 0.4, 0.6, 0.1),
    ]


def evaluate_recommender() -> list[EvaluationResult]:
    """Run deterministic ranking and reliability checks."""
    recommender = Recommender(create_test_catalog())
    results = []

    profiles = [
        ("Pop preference", "pop", "happy", 0.9, 1),
        ("Lofi preference", "lofi", "chill", 0.3, 2),
        ("Rock preference", "rock", "intense", 0.95, 3),
    ]

    for name, genre, mood, energy, expected_id in profiles:
        user = UserProfile(genre, mood, energy, False)

        try:
            recommendations = recommender.recommend(user, k=1)
            passed = bool(
                recommendations
                and recommendations[0].id == expected_id
            )
            details = (
                "Correct top recommendation"
                if passed else "Unexpected recommendation"
            )
        except Exception as error:
            passed = False
            details = f"{type(error).__name__}: {error}"

        results.append(EvaluationResult(name, passed, details))

    user = UserProfile("pop", "happy", 0.9, False)

    checks = [
        (
            "Zero-result handling",
            lambda: recommender.recommend(user, k=0) == [],
        ),
        (
            "Recommendation limit",
            lambda: len(recommender.recommend(user, k=2)) == 2,
        ),
        (
            "Explanation quality",
            lambda: all(
                term in recommender.explain_recommendation(
                    user, recommender.songs[0]
                )
                for term in ("Genre match", "Mood match")
            ),
        ),
    ]

    for name, check in checks:
        try:
            passed = bool(check())
            details = "Check passed" if passed else "Check failed"
        except Exception as error:
            passed = False
            details = f"{type(error).__name__}: {error}"

        results.append(EvaluationResult(name, passed, details))

    return results


def main() -> None:
    """Print evaluation results and a reliability summary."""
    results = evaluate_recommender()
    passed = sum(result.passed for result in results)
    total = len(results)

    print("\nMUSIC RECOMMENDER - RELIABILITY REPORT")
    print("-" * 45)

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.details}")

    print("-" * 45)
    print(f"Tests passed: {passed}/{total}")
    print(f"Pass rate: {passed / total:.0%}" if total else "No tests")

    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
