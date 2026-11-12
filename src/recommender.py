
"""Content-based music recommendation engine."""

import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple


@dataclass
class Song:
    """A song and its audio characteristics."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A listener's music preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file."""
    numeric_fields = (
        "energy", "tempo_bpm", "valence",
        "danceability", "acousticness"
    )

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        songs = list(csv.DictReader(file))

    for song in songs:
        song["id"] = int(song["id"])
        for field in numeric_fields:
            song[field] = float(song[field])

    return songs


def score_song(
    user_prefs: Dict, song: Dict
) -> Tuple[float, List[str]]:
    """Calculate relevance and explain each scoring component."""
    score = 0.0
    reasons = []

    genre = user_prefs.get(
        "genre", user_prefs.get("favorite_genre", "")
    )
    mood = user_prefs.get(
        "mood", user_prefs.get("favorite_mood", "")
    )
    energy = float(user_prefs.get(
        "energy", user_prefs.get("target_energy", 0.5)
    ))

    if song["genre"].lower() == genre.lower():
        score += 2.0
        reasons.append("Genre match (+2.0)")

    if song["mood"].lower() == mood.lower():
        score += 1.0
        reasons.append("Mood match (+1.0)")

    energy_points = max(
        0.0, 1.0 - abs(float(song["energy"]) - energy)
    )
    score += energy_points
    reasons.append(f"Energy similarity (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        acousticness = float(song["acousticness"])
        acoustic_points = 0.5 * (
            acousticness if user_prefs["likes_acoustic"]
            else 1.0 - acousticness
        )
        score += acoustic_points
        reasons.append(
            f"Acoustic preference (+{acoustic_points:.2f})"
        )

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5
) -> List[Tuple[Dict, float, List[str]]]:
    """Return the top-ranked songs with scores and explanations."""
    if k <= 0:
        return []

    ranked = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    return sorted(
        ranked, key=lambda item: item[1], reverse=True
    )[:k]


class Recommender:
    """Object-oriented interface for personalized recommendations."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _preferences(user: UserProfile) -> Dict:
        return asdict(user)

    def _score(
        self, user: UserProfile, song: Song
    ) -> Tuple[float, List[str]]:
        return score_song(self._preferences(user), asdict(song))

    def recommend(
        self, user: UserProfile, k: int = 5
    ) -> List[Song]:
        """Return up to k songs ordered by relevance."""
        if k <= 0:
            return []

        return sorted(
            self.songs,
            key=lambda song: self._score(user, song)[0],
            reverse=True
        )[:k]

    def explain_recommendation(
        self, user: UserProfile, song: Song
    ) -> str:
        """Explain a recommendation using its scoring factors."""
        score, reasons = self._score(user, song)
        explanation = "; ".join(reasons) or "No matching factors"

        return (
            f"{song.title} scored {score:.2f} points: "
            f"{explanation}"
        )
