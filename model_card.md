
# Model Card: VibeMatch Music Recommender

**Project:** Applied AI Music Recommender  
**Version:** 2.0 — Galaxy Interface  
**Developer:** Joanne Jongeling  
**Course:** CodePath AI110  
**Technologies:** Python 3.13, Streamlit, pytest, CSV, Mermaid

## 1. System Overview

VibeMatch is a content-based music recommendation system that generates personalized song suggestions using listener preferences and musical attributes.

Originally developed during CodePath AI110 Module 3, the application was extended into a more reliable, testable, and interactive applied AI system.

The final project includes:

- Content-based recommendation scoring
- Personalized song ranking
- Explainable recommendations
- Input validation and error handling
- Diagnostic logging
- Automated reliability evaluation
- Unit testing with pytest
- Interactive Streamlit dashboard
- Animated galaxy-inspired interface

VibeMatch is a deterministic, rule-based recommender rather than a trained machine-learning or generative AI model.

## 2. Intended Use

VibeMatch demonstrates how recommendation systems transform user preferences into numerical scores and ranked results.

Users can select:

- Favorite music genre
- Preferred mood
- Target energy level
- Acoustic music preference
- Number of recommendations

The system is intended for education, software engineering demonstrations, and experimentation with recommendation algorithms.

It is not designed for production streaming services, behavioral profiling, or high-stakes decision-making.

## 3. Recommendation Algorithm

The recommendation engine is implemented in `src/recommender.py`.

It compares listener preferences against song characteristics and assigns relevance scores.

### Current Scoring Weights

| Feature | Maximum Points |
|---|---:|
| Genre match | 2.0 |
| Mood match | 1.0 |
| Energy similarity | 1.0 |
| Acoustic preference | 0.5 |
| **Maximum Score** | **4.5** |

Energy similarity is calculated using:

`max(0, 1 - abs(song_energy - target_energy))`

Acoustic preference scoring rewards higher acousticness when the listener prefers acoustic music and lower acousticness otherwise.

The recommender calculates scores, sorts songs by relevance, and returns the highest-ranked results.

Scores represent relevance, not statistical probabilities or measured recommendation accuracy.

Tempo, valence, and danceability are stored in the dataset but do not currently contribute directly to the ranking formula.

## 4. Dataset

The dataset contains 15 songs with different musical attributes.

During Module 3, I expanded the original catalog from 10 songs to 15 songs.

### Songs Added

| Song | Genre | Mood |
|---|---|---|
| Velvet Nights | R&B | Romantic |
| Wildfire Heart | Metal | Intense |
| Golden Fields | Folk | Peaceful |
| Neon Bounce | Hip-Hop | Confident |
| Ocean Dreams | Reggae | Relaxed |

Each song contains:

- ID
- Title
- Artist
- Genre
- Mood
- Energy
- Tempo
- Valence
- Danceability
- Acousticness

The dataset is intentionally small for controlled experimentation.

It does not include listening history, personal information, or real-time streaming data.

## 5. Previous Scoring Experiments

During Module 3, I experimented with feature weights to examine how they affected recommendations.

| Feature | Original Experimental Weight | Modified Weight |
|---|---:|---:|
| Genre | 2.0 | 1.0 |
| Energy | 1.5 | 3.0 |

Increasing energy importance made songs with similar energy levels more competitive, even when their genres differed from user preferences.

For example, Storm Runner appeared in High-Energy Pop recommendations despite being classified as rock.

This demonstrated how changes to feature weights influence recommendation rankings.

These experimental weights are historical and are not the weights used in the current refactored system.

## 6. Interactive Streamlit Dashboard

The final project includes an interactive application implemented in `src/main.py`.

The dashboard provides a user-friendly interface for selecting preferences and reviewing personalized recommendations.

### Interface Features

- Genre and mood dropdown menus
- Adjustable energy slider
- Acoustic preference checkbox
- Recommendation count control
- Interactive recommendation generation
- Song relevance scores
- Ranked recommendation cards
- Expandable scoring explanations
- Dataset statistics

The application displays 15 songs, 12 genre categories, and 9 mood categories based on the current catalog.

### Galaxy-Inspired Visualization

I redesigned the application with a futuristic, space-inspired interface.

The visual system includes:

- Dark navy and violet gradients
- Animated starfield layers
- Moving nebula effects
- Translucent recommendation panels
- Violet and cyan accents
- Holographic orbital rings
- Energy-responsive glowing sphere
- Reduced-motion CSS support

The holographic orb responds visually to the selected energy preference.

Higher energy settings produce faster pulsing animations.

This is a 3D-inspired visual effect animated over time, not a literal four-dimensional simulation.

The orb does not analyze live audio or change recommendation scores.

### Interface Design Decisions

I prioritized readable typography, consistent colors, simple navigation, and visual separation between controls and results.

The galaxy theme supports the application's identity without replacing the underlying recommendation functionality.

## 7. System Architecture

VibeMatch separates the recommendation engine, user interface, evaluation system, and automated tests.

### Main Components

**src/main.py**

Provides the interactive Streamlit dashboard.

**src/recommender.py**

Handles song data, preference validation, scoring, ranking, and explanations.

**src/evaluator.py**

Executes controlled reliability evaluations.

**tests/test_recommender.py**

Tests the recommendation engine.

**tests/test_evaluator.py**

Tests evaluation behavior.

**tests/test_guardrails.py**

Tests input validation and edge cases.

**diagrams/architecture.mmd**

Contains the system architecture in Mermaid source format.

### Data Flow

1. The user selects music preferences.
2. Input validation checks the supplied values.
3. The recommendation engine compares preferences with songs.
4. Scores are calculated using predefined weights.
5. Songs are ranked by relevance.
6. The dashboard displays recommendations.
7. Users can examine scoring explanations.
8. Automated tests and the evaluator verify expected system behavior.

## 8. Reliability Evaluation

The final project introduces a dedicated reliability evaluation system.

The evaluator checks six predefined behaviors:

1. Pop recommendation ranking
2. Lofi recommendation ranking
3. Rock recommendation ranking
4. Zero-result handling
5. Recommendation limit handling
6. Explanation generation

### Automated Testing Results

During local development, 20 automated tests passed.

| Test Category | Passed |
|---|---:|
| Recommendation tests | 4 |
| Evaluator tests | 8 |
| Guardrail tests | 8 |
| **Total** | **20** |

**Previously verified local result: 20 of 20 tests passed.**

These results demonstrate expected functionality across the defined tests.

They do not establish perfect recommendation accuracy or guarantee that the application is free from defects.

### Commands

Run the automated tests:

```powershell
python -m pytest -v
```

Run the reliability evaluator:

```powershell
python -m src.evaluator
```

Launch the application:

```powershell
python -m streamlit run src/main.py
```

The Streamlit dashboard was also manually tested and confirmed to display personalized recommendations.

## 9. Input Validation and Guardrails

The recommender includes validation to prevent malformed information from being used in scoring.

Implemented checks include:

- Missing genre and mood values
- Invalid numerical energy values
- Non-finite numerical values
- Incorrect acoustic preference types
- Invalid song metadata
- Malformed CSV numerical data
- Zero and negative recommendation limits

Invalid values generate descriptive errors.

Python logging records validation failures for debugging.

Persistent log storage is not currently implemented.

## 10. Technical Challenges and Solutions

### Challenge 1: Python Syntax Errors

Some source files contained malformed type annotations and indentation problems.

An example was:

`List[Song\]`

The extra backslash prevented Python from compiling the file.

**Solution:** I corrected the annotations, repaired indentation, and refactored the recommendation logic into smaller functions.

### Challenge 2: Python Imports

Running individual test files directly through VS Code produced:

`ModuleNotFoundError: No module named 'src'`

**Solution:** I used package-based commands from the project root.

For example:

`python -m pytest -v`

This allowed Python to locate the source package correctly.

### Challenge 3: Project Organization

Some files were accidentally created inside nested directories such as `src/tests`.

**Solution:** I reorganized source files, automated tests, and architecture diagrams into dedicated folders.

This improved project structure and simplified Git version control.

### Challenge 4: Git Repository Setup

An initial push failed with:

`error: src refspec HEAD does not match any`

The new repository did not contain any commits.

**Solution:** I cloned the original Module 3 project, preserved its commit history, connected the new GitHub remote, and pushed the project successfully.

### Challenge 5: Streamlit Import Error

The initial Streamlit application failed with:

`ImportError: attempted relative import with no known parent package`

**Solution:** I updated the application to use an absolute package import:

`from src.recommender import load_songs, recommend_songs`

I also launched Streamlit from the project root.

### Challenge 6: Streamlit Indentation Error

The application contained an incomplete execution block:

`if __name__ == "__main__":`

**Solution:** I completed the application entry point and refactored the original command-line application into an interactive Streamlit dashboard.

### Challenge 7: Dashboard Appearance

The initial Streamlit dashboard included a white header gap and inconsistent interface colors.

**Solution:** I introduced custom CSS, adjusted the header styling, and developed a consistent galaxy-inspired interface.

### Key Engineering Lesson

Correct recommendation logic alone does not guarantee reliable execution.

Project organization, imports, testing, deployment configuration, and user-interface behavior are also important.

## 11. Strengths

### Explainability

Recommendations include descriptions of the factors contributing to their scores.

### Deterministic Behavior

Identical inputs and an unchanged catalog produce consistent rankings.

### Modular Design

Recommendation logic, testing, evaluation, and presentation are separated into dedicated files.

### Validation

Invalid user preferences and song attributes are rejected before scoring.

### Reproducibility

The evaluation framework uses controlled datasets and predefined test cases.

### Interactive Interface

The Streamlit dashboard provides a visual and accessible way to explore recommendation behavior.

## 12. Limitations and Potential Biases

### Dataset Representation Bias

The dataset contains only 15 songs.

Some genres and moods have fewer examples than others, affecting the variety of available recommendations.

### Feature Weighting Bias

The scoring weights are selected manually.

They reflect developer priorities rather than preferences learned from users.

### Limited Personalization

The application does not learn from listening history, skips, playlists, or repeated user interactions.

### Missing Musical Context

The algorithm does not understand lyrics, personal memories, cultural context, or emotional associations.

### Limited Evaluation Scope

The evaluator uses a synthetic three-song catalog.

Passing the predefined tests does not establish performance across large music catalogs or real-world listeners.

### No Trained Model

VibeMatch uses explicit scoring rules rather than machine learning, collaborative filtering, or generative AI.

Its primary advanced-system enhancement is reliability evaluation.

## 13. Potential Misuse and Prevention

Although music recommendation is relatively low risk, the system could be misused.

### Manipulated Rankings

A developer could secretly adjust weights to favor particular songs or musical genres.

**Prevention:** Maintain transparent scoring rules, document changes, and evaluate recommendations across different profiles.

### Misleading Accuracy Claims

A 100% automated test pass rate could be incorrectly interpreted as 100% recommendation accuracy.

**Prevention:** Clearly distinguish software testing from real-world recommendation effectiveness.

### Privacy Concerns

Future implementations incorporating listening history could expose personal behavioral information.

**Prevention:** Use consent, data minimization, limited retention, and appropriate access controls.

The current version does not collect personal listening histories.

## 14. Responsible AI Reflection

### What Are the Limitations or Biases in My System?

The biggest limitations are the small dataset, manually selected weights, and absence of real user feedback.

My earlier weighting experiment showed that increasing energy importance could cause songs from unrelated genres to rank more highly.

This demonstrated that a mathematically valid ranking does not always reflect individual listener preferences.

### Could My System Be Misused?

The scoring algorithm could be manipulated to favor selected genres or songs.

I would reduce this risk through transparent scoring, documented changes, and evaluation across different profiles.

I would also introduce privacy protections before collecting user behavior data.

### What Surprised Me During Reliability Testing?

One of my biggest discoveries was that technical failures were not always caused by the recommendation algorithm.

Several problems came from Python syntax, package imports, file organization, and Streamlit execution.

Correcting these issues demonstrated why reproducible execution and project structure are essential to software reliability.

### How Did I Collaborate With AI?

I used AI assistance to review code, troubleshoot errors, improve project organization, and build reliability evaluation components.

**One Suggestion I Accepted**

I accepted the recommendation to create a dedicated reliability evaluator.

This resulted in `src/evaluator.py`, which tests ranking behavior, explanations, and edge cases using a controlled dataset.

I accepted this suggestion because it made the system easier to evaluate and provided measurable test results.

**One Suggestion I Revised**

I revised the approach of executing Python test files individually through VS Code's debugging controls.

This approach caused package import failures.

Instead, I ran tests from the repository root using:

`python -m pytest -v`

I also ran the evaluator using:

`python -m src.evaluator`

These commands were more reliable and reproducible.

### What I Learned About AI-Assisted Development

AI-generated code and suggestions still require manual review.

I learned to verify proposed solutions against actual error messages, project requirements, and test results rather than assuming that generated code would work immediately.

## 15. Future Improvements

Potential future enhancements include:

- Expanding the song catalog
- Improving genre and mood representation
- Adding tempo, valence, and danceability weighting
- Allowing users to adjust scoring weights
- Collecting voluntary recommendation feedback
- Evaluating recommendation diversity
- Testing the Streamlit interface automatically
- Improving logging and error reporting
- Comparing rule-based recommendations with trained models

## 16. Personal Reflection

This project began as a simple experiment in personalized music recommendations.

As development progressed, I learned how recommendation algorithms depend on feature selection, weighting, and user preferences.

Extending the application taught me the importance of maintainable code, reliable execution, automated testing, input validation, and technical documentation.

Developing the futuristic Streamlit interface also allowed me to explore user-interface design while preserving the recommendation engine's functionality.

The most valuable lesson was learning to distinguish between a system that runs successfully, a system that passes automated tests, and a system whose recommendations users actually value.

This project strengthened my practical experience with Python, Git, Streamlit, software testing, debugging, and applied AI system design.

---

**Repository:** https://github.com/JoanneStars/ai110-applied-ai-music-recommender

**Developer:** Joanne Jongeling  
**Course:** CodePath AI110  
**Project:** VibeMatch Applied AI Music Recommender

