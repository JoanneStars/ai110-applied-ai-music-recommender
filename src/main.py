"""VibeMatch Fusion | Dual-engine music discovery dashboard.

Runs two portable Python recommenders: weighted baseline and nearest-neighbor.
Neither requires a compiled ML library. The similarity engine is not trained on
listener feedback, and both scores are relevance indicators, not probabilities.
"""

from pathlib import Path

import streamlit as st

from src.ai_engine import MusicAIEngine
from src.trained_engine import TrainedClusterEngine
from src.recommender import (
    MAX_SCORE,
    Recommender,
    Song,
    UserProfile,
    extract_features,
    load_songs,
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "songs.csv"

st.set_page_config(
    page_title="VibeMatch Fusion | Sonic Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_catalog() -> list[dict]:
    """Read and validate the music catalog."""
    return load_songs(str(DATA_PATH))


def apply_styles() -> None:
    """Apply the existing galaxy design to the Streamlit dashboard."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
            --violet: #a883ff;
            --cyan: #69e7ff;
        }
        html, body, [class*="css"] {
            font-family: "Segoe UI Variable", "Inter", "Segoe UI", sans-serif;
        }
        .stApp {
            isolation: isolate;
            color: #f2efff;
            background:
                radial-gradient(ellipse at 20% 15%, #38205a 0%, transparent 38%),
                radial-gradient(ellipse at 85% 75%, #123b6b 0%, transparent 43%),
                linear-gradient(135deg, #050713, #100d28 55%, #07172b);
        }
        header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
        }
        [data-testid="stDecoration"] { display: none !important; }
        .block-container {
            position: relative;
            max-width: 1250px;
            padding-top: 1.25rem !important;
            padding-bottom: 3rem;
        }
        .stApp::before {
            content: "";
            position: fixed;
            inset: -18%;
            z-index: -1;
            pointer-events: none;
            opacity: .65;
            background-image:
                radial-gradient(1px 1px at 15% 20%, white, transparent),
                radial-gradient(2px 2px at 40% 68%, #b9a2ff, transparent),
                radial-gradient(1px 1px at 75% 32%, white, transparent),
                radial-gradient(2px 2px at 87% 81%, #86eaff, transparent);
            background-size: 325px 325px;
            animation: stars 75s linear infinite;
        }
        .stApp::after {
            content: "";
            position: fixed;
            inset: -25%;
            z-index: -1;
            pointer-events: none;
            filter: blur(42px);
            background:
                radial-gradient(ellipse at 30% 35%, #9e3ddd35, transparent 42%),
                radial-gradient(ellipse at 72% 66%, #1d98d72e, transparent 40%);
            animation: nebula 27s ease-in-out infinite alternate;
        }
        @keyframes stars {
            to { transform: translate3d(-110px, 90px, 0); }
        }
        @keyframes nebula {
            to { transform: rotate(9deg) scale(1.13); }
        }
        .vm-eyebrow {
            color: #86e9ff;
            letter-spacing: .24em;
            font-size: .7rem;
            font-weight: 600;
        }
        .vm-title {
            font-size: clamp(3rem, 6vw, 5rem);
            font-weight: 300;
            line-height: 1.16;
            letter-spacing: -.06em;
            margin: .5rem 0;
            background: linear-gradient(100deg, #ffffff, #d2baff 55%, #81eaff);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .vm-lede {
            color: #c4c7df;
            max-width: 660px;
            line-height: 1.8;
            font-size: .96rem;
            font-weight: 300;
        }
        section[data-testid="stSidebar"] {
            background: #080d22f5;
            border-right: 1px solid #a784ff30;
        }
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: #eeeaff !important;
        }
        [data-baseweb="select"] > div {
            background: #151b38 !important;
            border: 1px solid #554c86 !important;
            border-radius: 10px !important;
        }
        [data-baseweb="select"] * { color: #f2eeff !important; }
        [data-testid="stSlider"] div[role="slider"] {
            background-color: #ae83ff !important;
            border-color: #ae83ff !important;
        }
        [data-testid="stMetric"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #11172cbd;
            border: 1px solid #a08bff42;
            border-radius: 16px;
            backdrop-filter: blur(14px);
        }
        [data-testid="stMetric"] { padding: 1rem; }
        [data-testid="stMetricLabel"] { color: #c1c5e8 !important; }
        [data-testid="stMetricValue"] {
            color: #ffffff;
            font-weight: 350;
        }
        .stButton button[kind="primary"] {
            color: #ffffff !important;
            border: 1px solid #c4a0ff66;
            border-radius: 12px;
            font-weight: 600;
            background: linear-gradient(105deg, #5829b8, #aa45d6, #2982c7, #5829b8);
            background-size: 300% 100%;
            animation: buttonGlow 9s linear infinite;
            box-shadow: 0 0 22px #8a50e84c;
        }
        .stButton button[kind="primary"]:hover {
            box-shadow: 0 0 32px #a36aff88;
        }
        @keyframes buttonGlow {
            to { background-position: 100% 0; }
        }
        .vm-orb-stage {
            height: 255px;
            display: flex;
            align-items: center;
            justify-content: center;
            perspective: 850px;
        }
        .vm-orb {
            position: relative;
            width: 160px;
            height: 160px;
            border-radius: 50%;
            transform-style: preserve-3d;
            background: radial-gradient(
                circle at 29% 23%, #ffffff 0%, #d9a7ff 11%,
                #7f42de 34%, #252e78 65%, #071127 100%
            );
            box-shadow:
                0 0 42px #a456ff88,
                0 0 95px #258bd844,
                inset -20px -24px 35px #02051dbb;
            animation: orbFloat 6s ease-in-out infinite,
                       orbPulse var(--pulse) ease-in-out infinite;
        }
        .vm-ring {
            position: absolute;
            inset: -22px;
            border-radius: 50%;
            border: 1px solid #c39affb0;
            transform-style: preserve-3d;
            animation: orbit 13s linear infinite;
        }
        .vm-ring.second {
            inset: -38px;
            border-color: #83e9ff88;
            animation-duration: 19s;
            animation-direction: reverse;
        }
        .vm-ring.third {
            inset: -10px;
            border-color: #ef8aff88;
            animation-duration: 10s;
        }
        @keyframes orbFloat { 50% { translate: 0 -12px; } }
        @keyframes orbPulse { 50% { filter: brightness(1.35); } }
        @keyframes orbit {
            from { transform: rotateZ(0deg) rotateX(67deg); }
            to { transform: rotateZ(360deg) rotateX(67deg); }
        }
        .vm-note {
            font-size: .76rem;
            color: #aab3d5;
            text-align: center;
            margin-top: 2rem;
        }
        @media (prefers-reduced-motion: reduce) {
            .stApp::before, .stApp::after, .vm-orb,
            .vm-ring, .stButton button { animation: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="vm-eyebrow">SONIC INTELLIGENCE / DUAL ENGINE</div>
        <h1 class="vm-title">VibeMatch Fusion</h1>
        <p class="vm-lede">
          Discover music through two transparent approaches:
          weighted content-based scoring and portable feature-vector similarity.
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_orb(energy: float) -> None:
    pulse_seconds = 5.0 - energy * 3.0
    st.markdown(
        f"""
        <div class="vm-orb-stage">
          <div class="vm-orb" style="--pulse: {pulse_seconds:.2f}s;"
               role="img" aria-label="Animated holographic music energy sphere">
            <div class="vm-ring"></div>
            <div class="vm-ring second"></div>
            <div class="vm-ring third"></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(results, show_vectors: bool, engine_mode: str) -> None:
    st.subheader("Your Sonic Matches")
    if engine_mode == "Python Baseline":
        st.caption(
            "Weighted content-based ranking. Scores add genre, mood, energy "
            "and acoustic contributions; they are not probabilities."
        )
    elif engine_mode == "Fusion Nearest Neighbor":
        st.caption(
            "Nearest-neighbor similarity. Scores map feature distance to a "
            "0–4.5 display scale, not probabilities."
        )
    else:
        st.caption(
            "Fitted unsupervised k-means model: learned audio-feature clusters. "
            "Small training catalog; relevance is not a probability."
        )

    for rank, result in enumerate(results, start=1):
        song = result.song
        with st.container(border=True):
            left, right = st.columns([4, 1])
            with left:
                st.markdown(f"### {rank:02d} / {song.title}")
                st.write(f"**Artist:** {song.artist}")
                st.write(f"**Genre:** {song.genre} · **Mood:** {song.mood}")
            with right:
                st.metric("RELEVANCE", f"{result.score:.2f} / {MAX_SCORE:.2f}")
            st.progress(result.relevance)
            with st.expander("Explore match analysis"):
                for reason in result.reasons:
                    st.write(f"• {reason}")
                st.write(
                    f"Energy: {song.energy:.2f} · "
                    f"Acousticness: {song.acousticness:.2f}"
                )
                if show_vectors:
                    vector = extract_features(vars(song))
                    st.caption("NUMERICAL FEATURE VECTOR")
                    st.code(
                        "[energy, valence, danceability, acousticness]\n"
                        + str(tuple(round(value, 3) for value in vector)),
                        language="text",
                    )


def main() -> None:
    apply_styles()
    render_header()

    try:
        catalog = load_catalog()
        songs = [Song(**record) for record in catalog]
        if not songs:
            st.warning("The music catalog is empty.")
            st.stop()
        baseline_engine = Recommender(songs)
    except (OSError, KeyError, TypeError, ValueError) as error:
        st.error(f"Unable to load the music catalog: {error}")
        st.stop()

    with st.sidebar:
        st.title("VibeMatch")
        st.caption("PERSONALIZE YOUR FREQUENCY")
        st.divider()

        engine_mode = st.radio(
            "Recommendation Engine",
            ("Python Baseline", "Fusion Nearest Neighbor", "Trained Cluster Model"),
            help="Compare rule-based scoring, nearest neighbors, and fitted k-means clustering.",
        )
        genre = st.selectbox(
            "Favorite Genre", sorted({song.genre for song in songs})
        )
        mood = st.selectbox(
            "Favorite Mood", sorted({song.mood for song in songs})
        )
        energy = st.slider(
            "Preferred Energy", 0.0, 1.0, value=0.70, step=0.05
        )
        acoustic = st.checkbox("Prefer Acoustic Music", value=False)
        limit = st.slider(
            "Number of Recommendations", 1, min(10, len(songs)),
            value=min(5, len(songs)),
        )
        show_vectors = st.checkbox(
            "Show Feature Telemetry", value=False,
            help="Display numerical features for future native C++ integration.",
        )
        generate = st.button(
            "Discover My Music", type="primary", use_container_width=True
        )
        st.divider()
        st.caption(f"ACTIVE ENGINE · {engine_mode.upper()}")
        st.caption("Fitted cluster model uses only Python and your song catalog.")
        from src.native_distance import DistanceBackend
        st.caption(f"COMPUTATION BACKEND · {DistanceBackend().backend}")

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("AVAILABLE TRACKS", len(songs))
    col2.metric("GENRE CHANNELS", len({song.genre for song in songs}))
    col3.metric("MOOD PROFILES", len({song.mood for song in songs}))
    render_orb(energy)

    # Persist output across Streamlit reruns such as opening an expander or
    # changing display-only preferences. Changed recommendation inputs require
    # clicking Discover again; old results are hidden until then.
    preferences = (genre, mood, energy, acoustic, limit, engine_mode)
    if generate:
        profile = UserProfile(
            favorite_genre=genre,
            favorite_mood=mood,
            target_energy=energy,
            likes_acoustic=acoustic,
        )
        try:
            if engine_mode == "Python Baseline":
                results = baseline_engine.recommend_detailed(profile, k=limit)
            elif engine_mode == "Fusion Nearest Neighbor":
                results = MusicAIEngine(songs).recommend(profile, k=limit)
            else:
                results = TrainedClusterEngine(songs).recommend(profile, k=limit)
        except (TypeError, ValueError) as error:
            st.error(f"Recommendation error: {error}")
            return
        st.session_state["vibematch_results"] = results
        st.session_state["vibematch_preferences"] = preferences

    if st.session_state.get("vibematch_preferences") != preferences:
        st.info("Select your preferences, then click 'Discover My Music'.")
        return

    results = st.session_state.get("vibematch_results", [])
    if not results:
        st.warning("No recommendations are available.")
        return
    render_recommendations(results, show_vectors, engine_mode)

    st.markdown(
        """
        <p class="vm-note">
          Three transparent recommendation modes ·
          Deterministic baseline · Fitted unsupervised clusters
          <br>
          Optional C++17 distance acceleration with Python fallback ·
          No live audio analysis.
        </p>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

