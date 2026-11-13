
"""VibeMatch Fusion | Dual-Engine Music Discovery Dashboard.

Cross-platform-ready Streamlit interface with:
- Validated content-based recommendation engine
- Portable nearest-neighbor similarity engine
- Explainable song rankings
- Interactive feature telemetry
- Futuristic galaxy-inspired interface

The nearest-neighbor engine uses pure Python, not scikit-learn.
"""

from dataclasses import asdict
from pathlib import Path

import streamlit as st

from src.ai_engine import MusicAIEngine
from src.recommender import (
    MAX_SCORE,
    Recommender,
    Song,
    UserProfile,
    extract_features,
    load_songs,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "songs.csv"

BASELINE = "Python Baseline"
FUSION = "Fusion Nearest Neighbor"


st.set_page_config(
    page_title="VibeMatch Fusion | Sonic Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def get_songs():
    """Load the validated local song catalog."""
    return load_songs(str(DATA_PATH))


def apply_styles():
    """Apply the futuristic galaxy dashboard theme."""

    st.markdown(
        """
        <style>
        :root {
            --violet: #a883ff;
            --cyan: #69e7ff;
            --pink: #ec8cff;
            --white: #f4f2ff;
            --muted: #b8bfdc;
        }

        html, body, [class*="css"] {
            font-family:
                "Segoe UI Variable",
                "Inter",
                "Segoe UI",
                sans-serif;
        }

        .stApp {
            isolation: isolate;
            color: #f4f2ff;
            background:
                radial-gradient(
                    ellipse at 20% 15%,
                    rgba(95, 38, 153, 0.42),
                    transparent 40%
                ),
                radial-gradient(
                    ellipse at 85% 75%,
                    rgba(19, 84, 155, 0.37),
                    transparent 45%
                ),
                linear-gradient(
                    135deg,
                    #050713,
                    #100d28 55%,
                    #07172b
                );
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }

        .block-container {
            position: relative;
            max-width: 1250px;
            padding-top: 1.2rem !important;
            padding-bottom: 3rem;
        }

        /* GALAXY BACKGROUND */

        .stApp::before {
            content: "";
            position: fixed;
            inset: -18%;
            z-index: -1;
            pointer-events: none;
            opacity: 0.65;

            background-image:
                radial-gradient(
                    1px 1px at 15% 20%,
                    #ffffff,
                    transparent
                ),
                radial-gradient(
                    2px 2px at 40% 68%,
                    #b9a2ff,
                    transparent
                ),
                radial-gradient(
                    1px 1px at 75% 32%,
                    #ffffff,
                    transparent
                ),
                radial-gradient(
                    2px 2px at 87% 81%,
                    #86eaff,
                    transparent
                );

            background-size: 325px 325px;
            animation: starMotion 75s linear infinite;
        }

        .stApp::after {
            content: "";
            position: fixed;
            inset: -25%;
            z-index: -1;
            pointer-events: none;
            filter: blur(42px);

            background:
                radial-gradient(
                    ellipse at 30% 35%,
                    rgba(158, 61, 221, 0.22),
                    transparent 42%
                ),
                radial-gradient(
                    ellipse at 72% 66%,
                    rgba(29, 152, 215, 0.20),
                    transparent 40%
                );

            animation:
                nebulaMotion 27s ease-in-out infinite alternate;
        }

        @keyframes starMotion {
            to {
                transform: translate3d(-110px, 90px, 0);
            }
        }

        @keyframes nebulaMotion {
            to {
                transform: rotate(9deg) scale(1.13);
            }
        }

        /* HEADER */

        .vm-eyebrow {
            color: #86e9ff;
            letter-spacing: 0.24em;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .vm-title {
            font-size: clamp(3rem, 6vw, 5rem);
            font-weight: 300;
            line-height: 1.16;
            letter-spacing: -0.06em;
            margin: 0.5rem 0;

            background: linear-gradient(
                100deg,
                #ffffff,
                #d2baff 55%,
                #81eaff
            );

            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .vm-lede {
            color: #c4c7df;
            max-width: 700px;
            line-height: 1.8;
            font-size: 0.96rem;
            font-weight: 300;
        }

        .vm-engine-label {
            color: #8be8ff;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-size: 0.73rem;
            font-weight: 600;
        }

        /* SIDEBAR */

        section[data-testid="stSidebar"] {
            background: rgba(8, 13, 34, 0.97);
            border-right: 1px solid rgba(167, 132, 255, 0.20);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: #eeeaff !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2 {
            color: #ffffff !important;
        }

        [data-baseweb="select"] > div {
            background: #151b38 !important;
            border: 1px solid #554c86 !important;
            border-radius: 10px !important;
        }

        [data-baseweb="select"] * {
            color: #f2eeff !important;
        }

        /* SLIDERS */

        [data-testid="stSlider"] div[role="slider"] {
            background-color: #ae83ff !important;
            border-color: #ae83ff !important;
        }

        /* CARDS */

        [data-testid="stMetric"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(17, 23, 44, 0.76);
            border: 1px solid rgba(160, 139, 255, 0.26);
            border-radius: 16px;
            backdrop-filter: blur(14px);
        }

        [data-testid="stMetric"] {
            padding: 1rem;
        }

        [data-testid="stMetricLabel"] {
            color: #c4c6e7 !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 350;
        }

        /* BUTTON */

        .stButton button[kind="primary"] {
            color: #ffffff !important;
            border: 1px solid rgba(196, 160, 255, 0.4);
            border-radius: 12px;
            font-weight: 600;

            background: linear-gradient(
                105deg,
                #5829b8,
                #aa45d6,
                #2982c7,
                #5829b8
            );

            background-size: 300% 100%;
            animation: buttonGlow 9s linear infinite;
            box-shadow: 0 0 22px rgba(138, 80, 232, 0.30);
        }

        @keyframes buttonGlow {
            to {
                background-position: 100% 0;
            }
        }

        /* HOLOGRAPHIC ORB */

        .vm-orb-stage {
            height: 270px;
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

            background:
                radial-gradient(
                    circle at 29% 23%,
                    #ffffff 0%,
                    #d9a7ff 11%,
                    #7f42de 34%,
                    #252e78 65%,
                    #071127 100%
                );

            box-shadow:
                0 0 42px rgba(164, 86, 255, 0.55),
                0 0 95px rgba(37, 139, 216, 0.28),
                inset -20px -24px 35px rgba(2, 5, 29, 0.75);

            animation:
                orbFloat 6s ease-in-out infinite,
                orbPulse var(--pulse) ease-in-out infinite;
        }

        .vm-ring {
            position: absolute;
            inset: -22px;
            border-radius: 50%;
            border: 1px solid rgba(195, 154, 255, 0.7);
            transform-style: preserve-3d;
            animation: orbit 13s linear infinite;
        }

        .vm-ring.second {
            inset: -38px;
            border-color: rgba(131, 233, 255, 0.55);
            animation-duration: 19s;
            animation-direction: reverse;
        }

        .vm-ring.third {
            inset: -10px;
            border-color: rgba(239, 138, 255, 0.55);
            animation-duration: 10s;
        }

        @keyframes orbFloat {
            50% {
                translate: 0 -12px;
            }
        }

        @keyframes orbPulse {
            50% {
                filter: brightness(1.35);
            }
        }

        @keyframes orbit {
            from {
                transform: rotateZ(0deg) rotateX(67deg);
            }
            to {
                transform: rotateZ(360deg) rotateX(67deg);
            }
        }

        /* TEXT */

        .vm-footer {
            font-size: 0.76rem;
            color: #aab3d5;
            text-align: center;
            margin-top: 2rem;
            line-height: 1.8;
        }

        /* ACCESSIBILITY */

        @media (prefers-reduced-motion: reduce) {
            .stApp::before,
            .stApp::after,
            .vm-orb,
            .vm-ring,
            .stButton button {
                animation: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Display the VibeMatch Fusion title."""

    st.markdown(
        """
        <div class="vm-eyebrow">
            SONIC INTELLIGENCE / DUAL-ENGINE DISCOVERY
        </div>

        <h1 class="vm-title">
            VibeMatch Fusion
        </h1>

        <p class="vm-lede">
            Explore music through transparent content-based
            scoring and numerical nearest-neighbor similarity.
            Two recommendation engines. One intelligent
            discovery interface.
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_orb(energy):
    """Display an energy-responsive holographic sphere."""

    pulse = 5.0 - energy * 3.0

    st.markdown(
        f"""
        <div class="vm-orb-stage">
            <div
                class="vm-orb"
                style="--pulse: {pulse:.2f}s;"
                role="img"
                aria-label="Animated music energy hologram"
            >
                <div class="vm-ring"></div>
                <div class="vm-ring second"></div>
                <div class="vm-ring third"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(
    results,
    engine_name,
    show_vectors,
):
    """Render ranked recommendations for either engine."""

    st.subheader("Your Sonic Matches")

    st.markdown(
        f'<div class="vm-engine-label">'
        f'ACTIVE ENGINE / {engine_name}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Scores represent algorithmic relevance, "
        "not statistical confidence or probabilities. "
        "Scores from different engines are not directly comparable."
    )

    for rank, result in enumerate(results, start=1):
        song = result.song

        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.markdown(
                    f"### {rank:02d} / {song.title}"
                )

                st.write(
                    f"**Artist:** {song.artist}"
                )

                st.write(
                    f"**Genre:** {song.genre} · "
                    f"**Mood:** {song.mood}"
                )

            with right:
                st.metric(
                    "RELEVANCE",
                    f"{result.score:.2f} / {MAX_SCORE:.2f}",
                )

            st.progress(
                min(max(result.relevance, 0.0), 1.0)
            )

            with st.expander("Explore match analysis"):
                for reason in result.reasons:
                    st.write(f"• {reason}")

                st.write(
                    f"Energy: {song.energy:.2f}"
                )

                st.write(
                    f"Acousticness: {song.acousticness:.2f}"
                )

                if show_vectors:
                    features = extract_features(
                        asdict(song)
                    )

                    st.caption(
                        "NUMERICAL FEATURE TELEMETRY"
                    )

                    st.code(
                        "Energy · Valence · Danceability "
                        "· Acousticness\n"
                        + str(
                            tuple(
                                round(value, 3)
                                for value in features
                            )
                        ),
                        language="text",
                    )


def main():
    """Run the dual-engine Streamlit application."""

    apply_styles()
    render_header()

    try:
        catalog = get_songs()

        songs = [
            Song(**record)
            for record in catalog
        ]

        baseline_engine = Recommender(songs)
        fusion_engine = MusicAIEngine(songs)

    except (OSError, KeyError, TypeError, ValueError) as error:
        st.error(
            f"Unable to initialize VibeMatch Fusion: {error}"
        )
        st.stop()

    if not songs:
        st.warning("The music catalog is empty.")
        st.stop()

    with st.sidebar:
        st.title("VibeMatch")

        st.caption(
            "PERSONALIZE YOUR FREQUENCY"
        )

        st.divider()

        engine_mode = st.radio(
            "Recommendation Engine",
            options=[
                BASELINE,
                FUSION,
            ],
            index=0,
            help=(
                "Choose between fixed content-based scoring "
                "and portable nearest-neighbor similarity."
            ),
        )

        st.divider()

        genre = st.selectbox(
            "Favorite Genre",
            sorted({song.genre for song in songs}),
        )

        mood = st.selectbox(
            "Favorite Mood",
            sorted({song.mood for song in songs}),
        )

        energy = st.slider(
            "Preferred Energy",
            min_value=0.0,
            max_value=1.0,
            value=0.70,
            step=0.05,
        )

        acoustic = st.checkbox(
            "Prefer Acoustic Music",
            value=False,
        )

        limit = st.slider(
            "Number of Recommendations",
            min_value=1,
            max_value=min(10, len(songs)),
            value=min(5, len(songs)),
        )

        show_vectors = st.checkbox(
            "Show Feature Telemetry",
            value=False,
        )

        generate = st.button(
            "Discover My Music",
            type="primary",
            use_container_width=True,
        )

        st.divider()

        st.caption(
            f"ACTIVE ENGINE · {engine_mode.upper()}"
        )

        st.caption(
            "Portable Python computation. "
            "Native C++ acceleration is not enabled."
        )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "AVAILABLE TRACKS",
        len(songs),
    )

    col2.metric(
        "GENRE CHANNELS",
        len({song.genre for song in songs}),
    )

    col3.metric(
        "MOOD PROFILES",
        len({song.mood for song in songs}),
    )

    render_orb(energy)

    # Preserve the latest results during ordinary Streamlit reruns.
    profile = UserProfile(
        favorite_genre=genre,
        favorite_mood=mood,
        target_energy=energy,
        likes_acoustic=acoustic,
    )

    selection = (
        engine_mode,
        genre,
        mood,
        energy,
        acoustic,
        limit,
    )

    if generate:
        st.session_state["vm_selection"] = selection

    if st.session_state.get("vm_selection") != selection:
        st.info(
            "Select your preferences and click "
            "'Discover My Music' to generate recommendations."
        )
        return

    try:
        if engine_mode == FUSION:
            results = fusion_engine.recommend(
                profile,
                k=limit,
            )
        else:
            results = baseline_engine.recommend_detailed(
                profile,
                k=limit,
            )

    except (TypeError, ValueError) as error:
        st.error(
            f"Recommendation error: {error}"
        )
        return

    if not results:
        st.warning(
            "No recommendations are available."
        )
        return

    render_recommendations(
        results,
        engine_mode,
        show_vectors,
    )

    st.markdown(
        """
        <div class="vm-footer">
            VIBEMATCH FUSION / SONIC INTELLIGENCE
            <br>
            Explainable ranking · Validated inputs ·
            Portable similarity computation
            <br>
            Educational recommendation system ·
            No live audio analysis
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
