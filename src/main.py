
"""VibeMatch | Futuristic Music Discovery Interface."""

from pathlib import Path

import streamlit as st

from src.recommender import load_songs, recommend_songs


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "songs.csv"
MAX_SCORE = 4.5


st.set_page_config(
    page_title="VibeMatch | Sonic Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_songs():
    """Load the validated song catalog."""
    return load_songs(str(DATA_PATH))


def apply_custom_styles():
    """Create an animated, futuristic cosmic interface."""
    st.markdown(
        """
        <style>
        /* ================================
           GLOBAL THEME
        ================================= */

        :root {
            --void: #050716;
            --navy: #0c1230;
            --violet: #9362ff;
            --cyan: #68e5ff;
            --pink: #ef8aff;
            --white: #f5f4ff;
            --muted: #a8accb;
            --glass: rgba(17, 22, 51, 0.72);
        }

        html, body, [class*="css"] {
            font-family:
                "Segoe UI Variable",
                "Inter",
                "Segoe UI",
                sans-serif;
        }

        .stApp {
            background:
                radial-gradient(
                    ellipse at 17% 20%,
                    rgba(102, 34, 176, 0.30),
                    transparent 43%
                ),
                radial-gradient(
                    ellipse at 85% 85%,
                    rgba(31, 97, 177, 0.30),
                    transparent 45%
                ),
                linear-gradient(
                    145deg,
                    #050716 0%,
                    #130d2b 48%,
                    #08152e 100%
                );
            color: var(--white);
            isolation: isolate;
        }

        /* Remove the white header strip */
        header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            background: transparent !important;
        }

        .block-container {
            position: relative;
            padding-top: 1.2rem !important;
            padding-bottom: 4rem;
            max-width: 1250px;
        }

        /* ================================
           ANIMATED COSMIC ENVIRONMENT
        ================================= */

        .stApp::before {
            content: "";
            position: fixed;
            inset: -20%;
            pointer-events: none;
            z-index: -1;

            background-image:
                radial-gradient(
                    1px 1px at 12% 18%,
                    #ffffff,
                    transparent
                ),
                radial-gradient(
                    2px 2px at 34% 64%,
                    #a5c9ff,
                    transparent
                ),
                radial-gradient(
                    1px 1px at 72% 26%,
                    #ffffff,
                    transparent
                ),
                radial-gradient(
                    2px 2px at 86% 80%,
                    #c48aff,
                    transparent
                ),
                radial-gradient(
                    1px 1px at 49% 42%,
                    #ffffff,
                    transparent
                );

            background-size: 370px 370px;
            opacity: 0.55;
            animation:
                starTravel 75s linear infinite,
                starFade 6s ease-in-out infinite alternate;
        }

        .stApp::after {
            content: "";
            position: fixed;
            inset: -25%;
            pointer-events: none;
            z-index: -1;

            background:
                radial-gradient(
                    ellipse at 28% 35%,
                    rgba(129, 43, 232, 0.22),
                    transparent 38%
                ),
                radial-gradient(
                    ellipse at 70% 65%,
                    rgba(25, 131, 255, 0.19),
                    transparent 40%
                ),
                radial-gradient(
                    ellipse at 55% 48%,
                    rgba(218, 57, 203, 0.12),
                    transparent 42%
                );

            filter: blur(35px);
            animation: nebulaMotion 30s ease-in-out infinite alternate;
        }

        @keyframes starTravel {
            from {
                transform: translate3d(0, 0, 0);
            }
            to {
                transform: translate3d(-120px, 90px, 0);
            }
        }

        @keyframes starFade {
            from { opacity: 0.25; }
            to { opacity: 0.75; }
        }

        @keyframes nebulaMotion {
            0% {
                transform: rotate(-8deg) scale(1);
            }
            50% {
                transform: rotate(7deg) scale(1.12);
            }
            100% {
                transform: rotate(-4deg) scale(1.05);
            }
        }

        /* ================================
           TYPOGRAPHY
        ================================= */

        h1, h2, h3 {
            color: var(--white) !important;
            font-weight: 500 !important;
            letter-spacing: -0.035em !important;
        }

        .stApp p,
        .stApp label {
            color: #e5e6fb;
        }

        .vm-eyebrow {
            color: var(--cyan);
            font-size: 0.69rem;
            font-weight: 600;
            letter-spacing: 0.28em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .vm-title {
            font-size: clamp(3rem, 6vw, 5.2rem);
            font-weight: 300;
            line-height: 1.12;
            letter-spacing: -0.065em;
            background: linear-gradient(
                100deg,
                #ffffff 10%,
                #d8c5ff 52%,
                #7de6ff 100%
            );
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        .vm-subtitle {
            margin-top: 0.85rem;
            max-width: 610px;
            color: #bdc2de;
            font-size: 0.96rem;
            line-height: 1.85;
            font-weight: 300;
        }

        .vm-section {
            font-size: 1.35rem;
            font-weight: 400;
            letter-spacing: -0.025em;
            color: var(--white);
            margin: 0.5rem 0 1rem;
        }

        .vm-footer {
            color: #8d95bd;
            font-size: 0.75rem;
            line-height: 1.8;
            text-align: center;
            margin-top: 2rem;
        }

        /* ================================
           SIDEBAR
        ================================= */

        section[data-testid="stSidebar"] {
            background: rgba(6, 9, 28, 0.96);
            border-right: 1px solid rgba(166, 128, 255, 0.16);
        }

        section[data-testid="stSidebar"] > div {
            background: transparent;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: #e9e8fa !important;
        }

        section[data-testid="stSidebar"] h2 {
            font-weight: 500;
            letter-spacing: -0.025em;
        }

        [data-baseweb="select"] > div {
            background: #141936 !important;
            border: 1px solid #3e456d !important;
            border-radius: 10px !important;
        }

        [data-baseweb="select"] * {
            color: #f3efff !important;
        }

        [data-baseweb="slider"] {
            color: #a77bff;
        }

        /* ================================
           GLASS PANELS
        ================================= */

        [data-testid="stMetric"] {
            padding: 1.1rem 1.3rem;
            border: 1px solid rgba(150, 129, 255, 0.20);
            border-radius: 16px;
            background: var(--glass);
            backdrop-filter: blur(14px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        [data-testid="stMetricValue"] {
            color: #f4f1ff;
            font-weight: 300;
            letter-spacing: -0.04em;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid rgba(154, 132, 255, 0.22);
            border-radius: 17px;
            background: rgba(13, 18, 43, 0.78);
            backdrop-filter: blur(14px);
            transition:
                border-color 0.25s ease,
                box-shadow 0.25s ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(160, 122, 255, 0.50);
            box-shadow: 0 0 30px rgba(108, 59, 217, 0.12);
        }

        /* ================================
           FUTURISTIC BUTTON
        ================================= */

        .stButton > button[kind="primary"] {
            width: 100%;
            border: 1px solid rgba(210, 174, 255, 0.28);
            border-radius: 12px;
            color: #ffffff !important;
            background: linear-gradient(
                110deg,
                #6224bd,
                #a449db,
                #347ce0,
                #6224bd
            );
            background-size: 300% 100%;
            box-shadow: 0 0 22px rgba(128, 64, 235, 0.24);
            font-weight: 500;
            letter-spacing: 0.025em;
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
            animation: glowTravel 9s linear infinite;
        }

        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(146, 81, 245, 0.45);
        }

        @keyframes glowTravel {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }

        /* ================================
           HOLOGRAPHIC ORB
        ================================= */

        .vm-orb-stage {
            height: 290px;
            display: flex;
            justify-content: center;
            align-items: center;
            perspective: 850px;
            overflow: visible;
        }

        .vm-orb-system {
            position: relative;
            width: 190px;
            height: 190px;
            transform-style: preserve-3d;
            animation: systemFloat 7s ease-in-out infinite;
        }

        .vm-orb-core {
            position: absolute;
            inset: 14px;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle at 30% 25%,
                    rgba(255, 255, 255, 0.95) 0%,
                    rgba(211, 157, 255, 0.9) 9%,
                    rgba(121, 67, 229, 0.85) 30%,
                    rgba(42, 35, 121, 0.95) 65%,
                    #071126 100%
                );
            box-shadow:
                0 0 35px rgba(164, 88, 255, 0.55),
                0 0 90px rgba(55, 129, 255, 0.28),
                inset -20px -24px 35px rgba(2, 5, 28, 0.7);
            animation: corePulse var(--pulse, 4s)
                       ease-in-out infinite;
        }

        .vm-orb-core::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle at 70% 75%,
                    rgba(48, 169, 255, 0.21),
                    transparent 52%
                );
            animation: shimmer 9s ease-in-out infinite alternate;
        }

        .vm-orbit {
            position: absolute;
            inset: -19px;
            border: 1px solid rgba(185, 151, 255, 0.48);
            border-radius: 50%;
            box-shadow: 0 0 15px rgba(126, 84, 255, 0.2);
            transform-style: preserve-3d;
        }

        .vm-orbit.one {
            animation: orbitOne 12s linear infinite;
        }

        .vm-orbit.two {
            inset: -38px;
            border-color: rgba(103, 211, 255, 0.35);
            animation: orbitTwo 18s linear infinite;
        }

        .vm-orbit.three {
            inset: -8px;
            border-color: rgba(230, 125, 255, 0.28);
            animation: orbitThree 9s linear infinite;
        }

        .vm-orb-halo {
            position: absolute;
            inset: -65px;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                rgba(113, 62, 233, 0.14),
                transparent 68%
            );
            filter: blur(12px);
            z-index: -1;
        }

        @keyframes systemFloat {
            0%, 100% {
                transform: translateY(0) rotate(-5deg);
            }
            50% {
                transform: translateY(-17px) rotate(5deg);
            }
        }

        @keyframes corePulse {
            0%, 100% {
                filter: brightness(0.92);
                transform: scale(1);
            }
            50% {
                filter: brightness(1.22);
                transform: scale(1.035);
            }
        }

        @keyframes shimmer {
            from { opacity: 0.45; }
            to { opacity: 1; }
        }

        @keyframes orbitOne {
            from {
                transform: rotateZ(0deg) rotateX(67deg);
            }
            to {
                transform: rotateZ(360deg) rotateX(67deg);
            }
        }

        @keyframes orbitTwo {
            from {
                transform: rotateZ(100deg) rotateY(65deg);
            }
            to {
                transform: rotateZ(460deg) rotateY(65deg);
            }
        }

        @keyframes orbitThree {
            from {
                transform: rotateZ(45deg) rotateX(40deg);
            }
            to {
                transform: rotateZ(-315deg) rotateX(40deg);
            }
        }

        /* ================================
           ADDITIONAL UI DETAILS
        ================================= */

        [data-testid="stAlert"] {
            background: rgba(42, 43, 92, 0.38);
            border: 1px solid rgba(144, 151, 255, 0.20);
            border-radius: 12px;
        }

        [data-testid="stExpander"] {
            background: rgba(12, 17, 39, 0.55);
            border-radius: 12px;
        }

        hr {
            border-color: rgba(170, 171, 221, 0.13);
        }

        /* Accessibility */
        @media (prefers-reduced-motion: reduce) {
            .stApp::before,
            .stApp::after,
            .vm-orb-system,
            .vm-orb-core,
            .vm-orb-core::after,
            .vm-orbit,
            .stButton > button {
                animation: none !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_orb(energy: float):
    """Render a 3D-inspired hologram driven by energy preference."""
    pulse = 5.0 - (energy * 3.0)

    st.markdown(
        f"""
        <div class="vm-orb-stage">
            <div
                class="vm-orb-system"
                style="--pulse: {pulse:.2f}s;"
                role="img"
                aria-label="Animated holographic music energy orb"
            >
                <div class="vm-orb-halo"></div>
                <div class="vm-orb-core"></div>
                <div class="vm-orbit one"></div>
                <div class="vm-orbit two"></div>
                <div class="vm-orbit three"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Display the futuristic VibeMatch branding."""
    st.markdown(
        """
        <div class="vm-eyebrow">
            SONIC INTELLIGENCE / PERSONALIZED DISCOVERY
        </div>

        <h1 class="vm-title">VibeMatch</h1>

        <div class="vm-subtitle">
            A new dimension of music discovery.
            Explore personalized recommendations through
            intelligent feature matching and transparent scoring.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(recommendations):
    """Display ranked recommendations with transparent scores."""
    st.markdown(
        '<div class="vm-section">Your Sonic Matches</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Content-based recommendations ranked by relevance. "
        "Match scores are not probabilities."
    )

    for rank, (song, score, reasons) in enumerate(
        recommendations, start=1
    ):
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.markdown(f"### {rank:02d} / {song['title']}")
                st.write(f"**Artist:** {song['artist']}")
                st.write(
                    f"**Genre:** {song['genre']}  |  "
                    f"**Mood:** {song['mood']}"
                )

            with right:
                st.metric(
                    "RELEVANCE",
                    f"{score:.2f}",
                )

            st.progress(
                min(max(score / MAX_SCORE, 0.0), 1.0)
            )

            with st.expander("Explore match analysis"):
                for reason in reasons:
                    st.write(f"• {reason}")

                st.write(
                    f"Energy: {song['energy']:.2f}"
                )
                st.write(
                    f"Acousticness: {song['acousticness']:.2f}"
                )


def main():
    """Render the VibeMatch music discovery application."""
    apply_custom_styles()

    try:
        songs = get_songs()
    except (FileNotFoundError, ValueError, KeyError) as error:
        st.error(f"Unable to load music catalog: {error}")
        st.stop()

    if not songs:
        st.warning("The music catalog is empty.")
        st.stop()

    genres = sorted({song["genre"] for song in songs})
    moods = sorted({song["mood"] for song in songs})

    with st.sidebar:
        st.markdown("## VibeMatch")
        st.caption("PERSONALIZE YOUR FREQUENCY")
        st.divider()

        genre = st.selectbox(
            "Favorite Genre",
            genres,
        )

        mood = st.selectbox(
            "Favorite Mood",
            moods,
        )

        energy = st.slider(
            "Preferred Energy",
            min_value=0.0,
            max_value=1.0,
            value=0.70,
            step=0.05,
        )

        likes_acoustic = st.checkbox(
            "Prefer Acoustic Music",
            value=False,
        )

        limit = st.slider(
            "Number of Recommendations",
            min_value=1,
            max_value=min(10, len(songs)),
            value=min(5, len(songs)),
        )

        generate = st.button(
            "Discover My Music",
            type="primary",
            use_container_width=True,
        )

        st.divider()
        st.caption("VIBEMATCH / AI110 SYSTEM 2.0")

    render_header()

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("AVAILABLE TRACKS", len(songs))
    col2.metric("GENRE CHANNELS", len(genres))
    col3.metric("MOOD PROFILES", len(moods))

    render_orb(energy)

    if not generate:
        st.info(
            "Adjust your preferences and select "
            "'Discover My Music' to generate recommendations."
        )
        return

    preferences = {
        "favorite_genre": genre,
        "favorite_mood": mood,
        "target_energy": energy,
        "likes_acoustic": likes_acoustic,
    }

    try:
        recommendations = recommend_songs(
            preferences,
            songs,
            k=limit,
        )
    except (ValueError, TypeError, KeyError) as error:
        st.error(f"Recommendation error: {error}")
        return

    if not recommendations:
        st.warning("No recommendations are available.")
        return

    render_recommendations(recommendations)

    st.markdown(
        """
        <div class="vm-footer">
            VIBEMATCH / CONTENT-BASED RECOMMENDATION ENGINE
            <br>
            Transparent scoring · Validated inputs ·
            Automated reliability evaluation
            <br>
            Educational AI system — no live audio analysis
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
