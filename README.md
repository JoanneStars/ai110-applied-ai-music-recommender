# Applied AI Music Recommender

**CodePath AI110 | Final Project**  
**Developer:** Joanne Jongeling  
**Language:** Python 3.13  
**Technologies:** Python, Streamlit, pytest, CSV, Mermaid

## Project Overview

The Applied AI Music Recommender is a content-based recommendation system designed to generate personalized song suggestions based on listener preferences and musical attributes.

This project extends my original CodePath AI110 Module 3 Music Recommender Simulation by introducing automated reliability evaluation, input validation, error handling, and diagnostic logging.

The objective is not simply to generate recommendations, but to develop a system whose decisions can be explained, tested, and reproduced.

The application uses deterministic feature-based scoring rather than a trained machine-learning model or generative AI service. Reliability evaluation is the primary advanced AI-system component introduced for this final project.

## 1. Original Project and Development Goals

**Original project:** [AI110 Module 3 Music Recommender Simulation](https://github.com/JoanneStars/ai110-module3show-musicrecommendersimulation-starter)

My original application used content-based filtering to rank songs according to user preferences, including genre, mood, energy, and acoustic characteristics. It allowed me to experiment with recommendation weights, compare results across different listener profiles, and examine why individual songs appeared in the rankings.

For the final project, I extended this foundation with three main objectives:

1. Improve code reliability and maintainability.
2. Validate recommendation inputs and handle invalid data safely.
3. Evaluate recommendation behavior through automated, reproducible tests.

## 2. Dataset Development

I expanded the original dataset from 10 songs to 15 songs.

The five additional songs were:

- Velvet Nights
- Wildfire Heart
- Golden Fields
- Neon Bounce
- Ocean Dreams

This expansion introduced additional combinations of genres, moods, and numerical audio characteristics.

Each song contains the following attributes:

| Attribute | Description |
|---|---|
| ID | Unique song identifier |
| Title | Song title |
| Artist | Performing artist |
| Genre | Musical category |
| Mood | Descriptive mood |
| Energy | Intensity represented on a 0–1 scale |
| Tempo | Beats per minute |
| Valence | Musical positivity on a 0–1 scale |
| Danceability | Dance-oriented characteristics |
| Acousticness | Acoustic characteristics on a 0–1 scale |

The expanded catalog provides more variety for comparing recommendation behavior. However, 15 songs remain a small experimental dataset and are not representative of a production music catalog.

## 3. Recommendation Algorithm

The recommendation engine compares listener preferences with song attributes and calculates a numerical relevance score.

The current implementation uses the following scoring factors:

| Factor | Maximum contribution |
|---|---:|
| Genre match | 2.0 |
| Mood match | 1.0 |
| Energy similarity | 1.0 |
| Acoustic preference | 0.5 |
| **Total** | **4.5** |

Energy similarity is calculated as:

`1 - abs(song_energy - target_energy)`

The acoustic contribution rewards higher acousticness when a listener prefers acoustic music and lower acousticness otherwise.

Songs are sorted by their calculated scores, and the system returns the highest-ranked results according to the requested recommendation limit.

**Design clarification:** Valence, danceability, and tempo are stored as song attributes, but they do not currently contribute directly to the final ranking score. They remain available for future feature development.

### Explainable Recommendations

The system also generates human-readable explanations of the scoring factors.

For example, an explanation can identify whether a recommendation received points for matching genre, matching mood, energy similarity, or acoustic preference.

This makes the system's ranking behavior more transparent and allows developers to examine why certain songs rank above others.

## 4. Feature-Weight Experiments

During Module 3, I experimented with changing the relative importance of genre and energy.

| Feature | Original experiment baseline | Modified experiment |
|---|---:|---:|
| Genre | 2.0 | 1.0 |
| Energy | 1.5 | 3.0 |

The experiment demonstrated that changing feature weights can substantially alter recommendation rankings.

When energy received greater emphasis, songs with energy values close to the listener's target became more competitive, even when their genres did not match.

For example, **Storm Runner**, a rock song, appeared in recommendations for the High-Energy Pop profile because its energy characteristics were close to the requested preference.

This demonstrated a key trade-off: increasing the influence of one feature can improve matching on that dimension while reducing the relative importance of other preferences.

**Current implementation:** The final refactored engine uses genre 2.0, mood 1.0, energy similarity up to 1.0, and acoustic preference up to 0.5. The experimental weights above are documented as earlier development work, not the current production configuration.

## 5. Recommendation Profile Experiments

I created three listener profiles to compare recommendation behavior.

| User profile | Top recommendation observed during Module 3 |
|---|---|
| High-Energy Pop | Sunrise City |
| Chill Lofi | Library Rain |
| Deep Intense Rock | Storm Runner |

These results were obtained during the original Module 3 experiments and are not presented as freshly verified outputs from the refactored final engine.

The experiments demonstrated that different preference combinations generated different recommendation rankings.

I also observed that individual songs could appear in multiple recommendation lists. For example, Neon Bounce appeared across several profiles because its numerical audio characteristics were compatible with different listener preferences.

This highlighted the importance of evaluating multiple attributes rather than relying exclusively on musical genre.

## 6. Final Project Architecture

The final system separates recommendation logic, reliability evaluation, and automated testing.

### Core Components

**`src/recommender.py`**

Contains the song and user-profile data structures, CSV loading, input validation, recommendation scoring, ranking, and explanation generation.

**`src/evaluator.py`**

Evaluates recommendation behavior against a controlled three-song catalog and predefined listener profiles. It produces individual pass/fail results and a summary report.

**`tests/test_recommender.py`**

Tests core recommendation functionality, including sorting, explanation generation, recommendation limits, and zero-result behavior.

**`tests/test_evaluator.py`**

Tests the evaluation system and verifies that it produces structured results, expected rankings, and a readable summary.

**`tests/test_guardrails.py`**

Tests invalid input handling, including missing preferences, out-of-range values, invalid song attributes, and incorrect preference types.

**`diagrams/architecture.mmd`**

Contains the system architecture diagram in Mermaid source format.

### Data Flow

1. The user provides music preferences.
2. The system validates the supplied information.
3. Song data is loaded and validated.
4. The recommendation engine calculates relevance scores.
5. Songs are ranked by score.
6. The system returns recommendations and explanations.
7. Automated tests and the separate evaluator examine system behavior.
8. Developers review the evaluation results and investigate failures.

The architecture diagram documents these relationships and distinguishes the recommendation workflow from the evaluation workflow.

## 7. Technical Challenges and Resolutions

Throughout development, I encountered several issues involving Python syntax, project structure, testing, and Git version control.

### Challenge 1: Python Syntax Errors

**Problem**

Some functions contained malformed type annotations and incorrectly combined statements.

One example was:

`List[Song\]`

The extra backslash caused Python to raise a `SyntaxError`.

**Resolution**

I corrected the type annotations, fixed indentation, and refactored the recommendation engine into smaller functions with clearly defined responsibilities.

I also removed incomplete experimental code that was interfering with normal execution.

**Result**

The recommendation module could be imported successfully, allowing automated testing and evaluation to continue.

### Challenge 2: Python Module Imports

**Problem**

Executing individual Python files through the VS Code debugger produced errors such as:

`ModuleNotFoundError: No module named 'src'`

**Resolution**

I organized the project as a Python package and executed the application components from the repository root using module-based commands.

For example:

`python -m pytest -v`

`python -m src.evaluator`

The package structure includes `src/__init__.py`.

**Result**

Python could resolve the project imports correctly when the commands were executed from the project root.

### Challenge 3: Incorrect File Locations

**Problem**

During development, some test and architecture files were accidentally created inside nested directories, including `src/tests`.

This created confusion when running Git commands and locating project components.

**Resolution**

I reorganized the files into their intended locations:

- `src/` for application logic
- `tests/` for automated tests
- `diagrams/` for Mermaid architecture source files

**Result**

The final directory structure became more consistent and easier to navigate.

### Challenge 4: Git Repository Configuration

**Problem**

My initial attempt to push the final project failed because the new local repository did not contain any commits.

Git displayed:

`error: src refspec HEAD does not match any`

I also encountered errors when attempting to stage files using incorrect paths.

**Resolution**

I cloned the original Module 3 repository into a separate final-project directory, changed its remote URL, and pushed the existing commit history to the new GitHub repository.

I subsequently corrected file paths before staging and committing additional changes.

**Result**

The final project was separated from the original Module 3 submission, allowing continued development without overwriting the original project.

### Challenge 5: Recommendation Weight Bias

**Problem**

Increasing the energy weight caused songs from other genres to compete more strongly with genre-matching songs.

**Resolution**

I compared multiple listener profiles, examined the resulting rankings, and returned to a more balanced scoring configuration for the refactored implementation.

**Result**

The experiment demonstrated that recommendation quality depends on how individual features are prioritized.

A system can be mathematically consistent while still producing recommendations that differ from user expectations.

## 8. Input Validation and Reliability Guardrails

I introduced validation functions to reduce errors caused by invalid user preferences and malformed song data.

The implemented checks include:

| Validation | Expected behavior |
|---|---|
| Missing genre or mood | Reject the input |
| Energy below 0 or above 1 | Raise a validation error |
| Non-finite numerical values | Reject the value |
| Invalid acoustic preference type | Reject the input |
| Invalid song metadata | Raise a descriptive error |
| Invalid CSV numerical data | Identify the affected row |
| Zero or negative recommendation limit | Return an empty recommendation list |

Invalid scoring inputs raise errors instead of being silently accepted.

The system uses Python's `logging` module to record validation failures and invalid CSV rows. Logging provides diagnostic information, although persistent log storage is not configured by default.

These safeguards help developers detect incorrect input before it influences recommendation results.

## 9. Reliability Evaluation

A dedicated evaluation component was added to measure whether the recommendation engine behaves as expected.

The evaluator uses a controlled catalog containing three synthetic songs and checks six behaviors:

1. Pop profile ranking
2. Lofi profile ranking
3. Rock profile ranking
4. Zero-result handling
5. Recommendation limits
6. Explanation generation

The evaluator records a pass/fail result and diagnostic description for each check.

### Automated Testing

The final project also includes automated tests covering the recommendation engine, evaluation system, and input guardrails.

During local development, I successfully ran **20 automated tests**, with all 20 passing.

| Test category | Passed |
|---|---:|
| Original recommendation tests | 4 |
| Evaluation tests | 8 |
| Input guardrail tests | 8 |
| **Total** | **20** |

Reported local development result:

```text
20 passed
```

This summarizes the successful local test run. A complete fresh terminal log should be captured when preparing the final submission.

**Interpretation:** A 100% automated test pass rate means all defined tests passed. It does not establish 100% recommendation accuracy or user satisfaction.

## 10. Setup and Execution

### Requirements

- Python 3.13
- pip
- Dependencies listed in `requirements.txt`

### Installation

Clone the project:

```powershell
git clone https://github.com/JoanneStars/ai110-applied-ai-music-recommender.git
cd ai110-applied-ai-music-recommender
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

### Run Automated Tests

```powershell
python -m pytest -v
```

### Run the Reliability Evaluator

```powershell
python -m src.evaluator
```

The evaluator displays individual checks and an overall pass rate.

### Run the Streamlit Interface

The project also contains a Streamlit application entry point.

```powershell
streamlit run src/main.py
```

The application provides a user-facing interface for exploring music recommendations. The final end-to-end interface should be checked separately from the automated unit tests.

## 11. Reproducible Recommendation Examples

The following command runs the recommendation engine against the evaluator's fixed synthetic catalog, providing a reproducible demonstration without external music services.

Run from the repository root:

```python
from src.evaluator import create_test_catalog
from src.recommender import Recommender, UserProfile

recommender = Recommender(create_test_catalog())

profiles = [
    ("Pop", UserProfile("pop", "happy", 0.9, False)),
    ("Lofi", UserProfile("lofi", "chill", 0.3, False)),
    ("Rock", UserProfile("rock", "intense", 0.95, False)),
]

for name, user in profiles:
    top_song = recommender.recommend(user, k=1)[0]
    print(f"{name}: {top_song.title}")
```

Expected output for the defined synthetic catalog:

```text
Pop: Pop Energy
Lofi: Lofi Evening
Rock: Rock Anthem
```

These examples demonstrate three distinct inputs and their expected recommendation outputs.

For final grading, the code should be executed locally and the resulting console output pasted into this section as actual execution evidence.

The evaluator also demonstrates error-handling and reliability behavior. Its full output can be captured with:

```powershell
python -m src.evaluator
```

## 12. Design Decisions and Trade-Offs

I chose a content-based scoring approach because it is understandable, deterministic, and straightforward to evaluate.

Unlike a trained recommendation model, the system does not require a large historical user-interaction dataset.

This design makes it easier to inspect individual scores and identify unexpected behavior.

However, fixed weights are also a limitation. They reflect predefined assumptions about how important genre, mood, energy, and acoustic characteristics should be.

The final design prioritizes transparency and reliable execution over complex personalization.

## 13. Limitations

The current system has several limitations:

- The dataset contains only 15 songs.
- Scoring weights are manually defined rather than learned from user feedback.
- Recommendation quality is evaluated using a small synthetic test catalog.
- The system does not incorporate listening history or real-time feedback.
- Valence, danceability, and tempo are stored but not directly used in ranking.
- The system does not retrieve live music information.
- Passing deterministic tests does not establish real-world recommendation quality.

Future improvements could include a larger dataset, additional scoring features, user-feedback evaluation, and comparison with a learned recommendation model.

## 14. What I Learned

This project demonstrated that building a recommendation system requires more than producing plausible suggestions.

My initial experiments focused on how feature weighting affects ranking behavior. As the project developed, I encountered software engineering challenges involving syntax, imports, code organization, and version control.

Fixing these issues reinforced the importance of maintainable code, reproducible execution, and automated testing.

The final project also helped me distinguish between recommendation performance and system reliability.

A recommendation can produce a valid numerical score without necessarily being the best choice for a listener. Automated testing verifies expected behavior, while meaningful recommendation quality requires broader evaluation and human feedback.

## 15. AI Collaboration and Responsible Development

AI assistance was used to review code, identify syntax issues, improve project organization, and develop testing and evaluation components.

Suggested solutions were evaluated against the existing project requirements and tested locally before being retained.

The most important development decision was to preserve the original content-based recommendation approach rather than replace it with an unnecessarily complex system.

Responsible-AI considerations, including limitations, possible bias, misuse, testing observations, and specific examples of accepted and revised AI suggestions, are documented separately in `model_card.md`.

## 16. Portfolio Reflection

This project demonstrates my ability to extend an existing Python application into a more reliable, testable, and explainable system.

It reflects my interest in applying software engineering principles to AI-related applications, particularly validation, systematic testing, algorithmic decision-making, and transparent system behavior.

**Repository:** https://github.com/JoanneStars/ai110-applied-ai-music-recommender

**Developer:** Joanne Jongeling  
**Course:** CodePath AI110
