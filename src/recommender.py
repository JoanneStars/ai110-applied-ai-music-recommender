
"""Content-based music recommendation engine with input guardrails."""

import csv
import logging
import math
from dataclasses import asdict, dataclass
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class Song:
    """Song metadata and audio characteristics."""
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
    """Listener preferences used for recommendations."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def validate_number(value, name: str, low=0.0, high=1.0) -> None:
    """Require a finite numeric value within the permitted range."""
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not low <= value <= high
    ):
        raise ValueError(f"{name} must be between {low} and {high}.")


def validate_preferences(prefs: Dict) -> None:
    """Validate required listener preferences."""
    for primary, alternate in (
        ("genre", "favorite_genre"),
        ("mood", "favorite_mood"),
    ):
        value = prefs.get(primary, prefs.get(alternate))
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{primary} must be a non-empty string.")

    energy = prefs.get("energy", prefs.get("target_energy"))
    validate_number(energy, "target_energy")

    if "likes_acoustic" in prefs and not isinstance(
        prefs["likes_acoustic"], bool
    ):
        raise ValueError("likes_acoustic must be a boolean.")


def validate_song(song: Dict) -> None:
    """Validate song metadata and numerical features."""
    for field in ("title", "artist", "genre", "mood"):
        value = song.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Song {field} must be a non-empty string.")

    for field in ("energy", "valence", "danceability", "acousticness"):
        validate_number(song.get(field), field)

    tempo = song.get("tempo_bpm")
    if (
        isinstance(tempo, bool)
        or not isinstance(tempo, (int, float))
        or not math.isfinite(tempo)
        or tempo <= 0
    ):
        raise ValueError("tempo_bpm must be a positive number.")


def load_songs(csv_path: str) -> List[Dict]:
    """Load song data and convert numeric fields."""
    numeric_fields = (
        "energy", "tempo_bpm", "valence",
        "danceability", "acousticness"
    )

    songs = []
    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        for row_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                row["id"] = int(row["id"])
                for field in numeric_fields:
                    row[field] = float(row[field])
                validate_song(row)
            except (KeyError, TypeError, ValueError) as error:
                logger.warning("Invalid CSV row %s: %s", row_number, error)
                raise ValueError(
                    f"Invalid song data on CSV row {row_number}"
                ) from error

            songs.append(row)

    return songs


def score_song(
    user_prefs: Dict, song: Dict
) -> Tuple[float, List[str]]:
    """Calculate a content-based score with explanations."""
    try:
        validate_preferences(user_prefs)
        validate_song(song)
    except (TypeError, ValueError) as error:
        logger.warning("Recommendation validation failed: %s", error)
        raise

    genre = user_prefs.get(
        "genre", user_prefs.get("favorite_genre")
    )
    mood = user_prefs.get(
        "mood", user_prefs.get("favorite_mood")
    )
    energy = user_prefs.get(
        "energy", user_prefs.get("target_energy")
    )

    score = 0.0
    reasons = []

    if song["genre"].lower() == genre.lower():
        score += 2.0
        reasons.append("Genre match (+2.0)")

    if song["mood"].lower() == mood.lower():
        score += 1.0
        reasons.append("Mood match (+1.0)")

    energy_points = max(0.0, 1.0 - abs(song["energy"] - energy))
    score += energy_points
    reasons.append(f"Energy similarity (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        acousticness = song["acousticness"]
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
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, List[str]]]:
    """Return the top-ranked songs and their explanations."""
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
    """Object-oriented interface for song recommendations."""

    def __init__(self, songs: List[Song]):
        self.songs = songs
        for song in songs:
            validate_song(asdict(song))

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
        """Rank songs using the shared scoring algorithm."""
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
        """Explain the factors behind a recommendation."""
        score, reasons = self._score(user, song)
        explanation = "; ".join(reasons) or "No matching factors"

        return f"{song.title} scored {score:.2f} points: {explanation}"
