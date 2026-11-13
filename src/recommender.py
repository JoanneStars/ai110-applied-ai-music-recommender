
"""VibeMatch Fusion | Music Recommendation Engine.

Provides validated content-based recommendations and
numerical feature extraction for future ML/C++ integration.
"""

import csv
import logging
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

MAX_SCORE = (
    GENRE_WEIGHT
    + MOOD_WEIGHT
    + ENERGY_WEIGHT
    + ACOUSTIC_WEIGHT
)

FEATURE_NAMES = (
    "energy",
    "valence",
    "danceability",
    "acousticness",
)


# --------------------------------------------------
# DATA MODELS
# --------------------------------------------------

@dataclass
class Song:
    """Represent a song and its audio characteristics."""

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
    """Represent listener preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


@dataclass
class RecommendationResult:
    """Store a ranked song, score, and explanation."""

    song: Song
    score: float
    reasons: List[str]

    @property
    def relevance(self) -> float:
        """Return normalized relevance between 0 and 1."""
        return round(
            min(max(self.score / MAX_SCORE, 0.0), 1.0),
            4,
        )


# --------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------

def validate_number(
    value,
    name: str,
    low: float = 0.0,
    high: float = 1.0,
) -> None:
    """Validate a finite numeric value within a range."""

    valid = (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(value)
        and low <= value <= high
    )

    if not valid:
        raise ValueError(
            f"{name} must be between {low} and {high}."
        )


def validate_preferences(prefs: Dict) -> None:
    """Validate user preferences before scoring."""

    if not isinstance(prefs, dict):
        raise ValueError("Preferences must be a dictionary.")

    for primary, alternative in (
        ("genre", "favorite_genre"),
        ("mood", "favorite_mood"),
    ):
        value = prefs.get(
            primary,
            prefs.get(alternative),
        )

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{primary} must be a non-empty string."
            )

    energy = prefs.get(
        "energy",
        prefs.get("target_energy"),
    )

    validate_number(energy, "target_energy")

    if (
        "likes_acoustic" in prefs
        and not isinstance(prefs["likes_acoustic"], bool)
    ):
        raise ValueError(
            "likes_acoustic must be a boolean."
        )


def validate_song(song: Dict) -> None:
    """Validate required song metadata and audio features."""

    if not isinstance(song, dict):
        raise ValueError("Song must be a dictionary.")

    for field in ("title", "artist", "genre", "mood"):
        value = song.get(field)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Song {field} must be a non-empty string."
            )

    for field in FEATURE_NAMES:
        validate_number(song.get(field), field)

    tempo = song.get("tempo_bpm")

    if (
        isinstance(tempo, bool)
        or not isinstance(tempo, (int, float))
        or not math.isfinite(tempo)
        or tempo <= 0
    ):
        raise ValueError(
            "tempo_bpm must be a positive number."
        )


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load and validate a CSV music catalog."""

    path = Path(csv_path)
    songs = []

    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                row["id"] = int(row["id"])
                row["tempo_bpm"] = float(row["tempo_bpm"])

                for field in FEATURE_NAMES:
                    row[field] = float(row[field])

                validate_song(row)

            except (KeyError, TypeError, ValueError) as error:
                logger.warning(
                    "Invalid CSV row %s: %s",
                    row_number,
                    error,
                )

                raise ValueError(
                    f"Invalid song data on CSV row {row_number}"
                ) from error

            songs.append(row)

    logger.info("Loaded %s songs", len(songs))
    return songs


# --------------------------------------------------
# FEATURE EXTRACTION
# --------------------------------------------------

def extract_features(song: Dict) -> Tuple[float, ...]:
    """Create a numeric vector for future AI/C++ engines.

    The vector uses a fixed feature order so that Python
    and native C++ implementations can share the same data.
    """

    validate_song(song)

    return tuple(
        float(song[field])
        for field in FEATURE_NAMES
    )


def extract_catalog_features(
    songs: List[Dict],
) -> List[Tuple[float, ...]]:
    """Convert a music catalog into feature vectors."""

    return [
        extract_features(song)
        for song in songs
    ]


# --------------------------------------------------
# RECOMMENDATION SCORING
# --------------------------------------------------

def score_song(
    user_prefs: Dict,
    song: Dict,
) -> Tuple[float, List[str]]:
    """Score a song using transparent content-based rules."""

    try:
        validate_preferences(user_prefs)
        validate_song(song)

    except (TypeError, ValueError) as error:
        logger.warning(
            "Recommendation validation failed: %s",
            error,
        )
        raise

    genre = user_prefs.get(
        "genre",
        user_prefs.get("favorite_genre"),
    )

    mood = user_prefs.get(
        "mood",
        user_prefs.get("favorite_mood"),
    )

    energy = user_prefs.get(
        "energy",
        user_prefs.get("target_energy"),
    )

    score = 0.0
    reasons = []

    # Genre matching
    if song["genre"].casefold() == genre.casefold():
        score += GENRE_WEIGHT
        reasons.append(
            f"Genre match (+{GENRE_WEIGHT:.1f})"
        )

    # Mood matching
    if song["mood"].casefold() == mood.casefold():
        score += MOOD_WEIGHT
        reasons.append(
            f"Mood match (+{MOOD_WEIGHT:.1f})"
        )

    # Energy similarity
    energy_similarity = max(
        0.0,
        1.0 - abs(song["energy"] - energy),
    )

    energy_points = ENERGY_WEIGHT * energy_similarity
    score += energy_points

    reasons.append(
        f"Energy similarity (+{energy_points:.2f})"
    )

    # Acoustic preference
    if "likes_acoustic" in user_prefs:
        acousticness = song["acousticness"]

        preference_match = (
            acousticness
            if user_prefs["likes_acoustic"]
            else 1.0 - acousticness
        )

        acoustic_points = (
            ACOUSTIC_WEIGHT * preference_match
        )

        score += acoustic_points

        reasons.append(
            f"Acoustic preference (+{acoustic_points:.2f})"
        )

    return round(score, 4), reasons


# --------------------------------------------------
# RECOMMENDATION RANKING
# --------------------------------------------------

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, List[str]]]:
    """Rank songs and return the top recommendations."""

    if k <= 0:
        return []

    validate_preferences(user_prefs)

    ranked = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    ranked.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked[:k]


# --------------------------------------------------
# OBJECT-ORIENTED RECOMMENDER
# --------------------------------------------------

class Recommender:
    """Provide a reusable recommendation interface."""

    def __init__(self, songs: List[Song]):
        self.songs = list(songs)

        for song in self.songs:
            validate_song(asdict(song))

    @staticmethod
    def _preferences(user: UserProfile) -> Dict:
        """Convert a profile into scoring preferences."""
        return asdict(user)

    def _score(
        self,
        user: UserProfile,
        song: Song,
    ) -> Tuple[float, List[str]]:
        """Score an individual song."""

        return score_song(
            self._preferences(user),
            asdict(song),
        )

    def recommend(
        self,
        user: UserProfile,
        k: int = 5,
    ) -> List[Song]:
        """Return the highest-ranked songs."""

        if k <= 0:
            return []

        prefs = self._preferences(user)
        validate_preferences(prefs)

        ranked = sorted(
            self.songs,
            key=lambda song: self._score(user, song)[0],
            reverse=True,
        )

        return ranked[:k]

    def recommend_detailed(
        self,
        user: UserProfile,
        k: int = 5,
    ) -> List[RecommendationResult]:
        """Return recommendations with scores and reasons."""

        if k <= 0:
            return []

        validate_preferences(self._preferences(user))
        results = []

        for song in self.songs:
            score, reasons = self._score(user, song)

            results.append(
                RecommendationResult(
                    song=song,
                    score=score,
                    reasons=reasons,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:k]

    def explain_recommendation(
        self,
        user: UserProfile,
        song: Song,
    ) -> str:
        """Explain why a recommendation was generated."""

        score, reasons = self._score(user, song)
        explanation = "; ".join(reasons)

        return (
            f"{song.title} scored {score:.2f} points: "
            f"{explanation}"
        )

    def feature_matrix(self) -> List[Tuple[float, ...]]:
        """Prepare song features for an ML or C++ backend."""

        return extract_catalog_features(
            [asdict(song) for song in self.songs]
        )
 