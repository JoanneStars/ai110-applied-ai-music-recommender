
"""Tests for the Music Recommender Simulation."""

from src.recommender import Song, UserProfile, Recommender


def make_small_recommender() -> Recommender:
    """Create a small catalog for testing recommendations."""
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    """Verify the best matching song ranks first."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )

    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].title == "Test Pop Track"
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    """Verify that recommendations include explanations."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )

    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)

    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "Genre match" in explanation
    assert "Mood match" in explanation


def test_recommend_respects_k_limit():
    """Verify the recommender returns only the requested number."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )

    rec = make_small_recommender()
    results = rec.recommend(user, k=1)

    assert len(results) == 1


def test_recommend_with_zero_k():
    """Verify requesting zero songs returns an empty list."""
    user = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=True,
    )

    rec = make_small_recommender()
    results = rec.recommend(user, k=0)

    assert results == []
