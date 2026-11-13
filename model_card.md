# Model Card: VibeMatch Music Recommender

**Project:** Applied AI Music Recommender  
**Version:** 2.0  
**Developer:** Joanne Jongeling  
**Course:** CodePath AI110  
**Language:** Python 3.13

---

## 1. Model Overview

VibeMatch is a content-based music recommendation system that generates personalized song recommendations using listener preferences and audio characteristics.

Originally developed during CodePath AI110 Module 3, the application was extended into a more reliable and testable applied AI system.

The current version includes:

- Content-based recommendation scoring
- Personalized song ranking
- Explainable recommendations
- Input validation and error handling
- Diagnostic logging
- Automated reliability evaluation
- Unit testing with pytest

VibeMatch is a deterministic, rule-based recommender rather than a trained machine-learning model. Its advanced system component focuses on reliability evaluation and validation.

## 2. Intended Use

VibeMatch is designed for educational demonstrations of recommendation algorithms, feature weighting, explainable decisions, and software reliability.

The system accepts listener preferences, compares them against a catalog of songs, calculates numerical relevance scores, and returns ranked recommendations.

**Intended users:** Students, educators, and developers studying applied AI systems.

**Not intended for:** Production music streaming services, behavioral profiling, or high-stakes automated decisions.

## 3. System Architecture

The application separates recommendation logic from evaluation and testing.

**Recommendation workflow:**

1. Receive listener preferences.
2. Validate preferences and song attributes.
3. Calculate content-based relevance scores.
4. Rank songs from highest to lowest score.
5. Return personalized recommendations.
6. Generate explanations for recommendation scores.

**Reliability workflow:**

1. Create controlled test profiles and song catalogs.
2. Execute recommendation and validation checks.
3. Compare results against expected behavior.
4. Record pass/fail outcomes.
5. Generate an evaluation summary.

The architecture is documented in `diagrams/architecture.mmd`.

### Current Scoring Weights

| Feature | Maximum points |
|---|---:|
| Genre match | 2.0 |
| Mood match | 1.0 |
| Energy similarity | 1.0 |
| Acoustic preference | 0.5 |
| **Maximum total** | **4.5** |

The engine uses fixed weighting rules.

Energy similarity is calculated from the difference between the song's energy and the listener's target energy.

The acoustic preference rewards higher or lower acousticness depending on the user's selected preference.

Although the song dataset also contains valence, danceability, and tempo values, these attributes do not currently influence ranking.

## 4. Dataset

The dataset contains 15 songs representing different genres, moods, and musical characteristics.

During Module 3, I expanded the original catalog from 10 to 15 songs by adding:

| Song | Genre | Mood |
|---|---|---|
| Velvet Nights | R&B | Romantic |
| Wildfire Heart | Metal | Intense |
| Golden Fields | Folk | Peaceful |
| Neon Bounce | Hip-Hop | Confident |
| Ocean Dreams | Reggae | Relaxed |

The data includes song titles, artists, genres, moods, energy, tempo, valence, danceability, and acousticness.

The catalog is small and intended for controlled experimentation rather than real-world recommendation accuracy.

It does not contain personal listening histories, behavioral tracking, or private user information.

## 5. Previous Experiments

During Module 3, I investigated how changes to scoring weights affected recommendation rankings.

| Feature | Original experimental baseline | Modified experiment |
|---|---:|---:|
| Genre | 2.0 | 1.0 |
| Energy | 1.5 | 3.0 |

Increasing the energy weight made songs with similar energy characteristics more competitive, even when their genres differed from the user's preference.

For example, Storm Runner, a rock song, appeared in High-Energy Pop recommendations because its energy level closely matched the target.

The experiment demonstrated that feature weighting can significantly influence recommendation outcomes.

These weights describe the earlier experiment, not the current refactored implementation.

The final engine uses the more balanced scoring configuration documented in Section 3.

## 6. Strengths

**Explainability**

Each recommendation can be accompanied by an explanation describing the factors contributing to its score.

**Deterministic behavior**

Identical inputs and an unchanged song catalog produce consistent rankings.

**Modular architecture**

The scoring engine, evaluator, and automated tests are maintained as separate components.

**Input validation**

Malformed preferences and invalid song attributes are rejected before being used in scoring.

**Reproducibility**

The application uses controlled datasets and predefined tests, allowing developers to repeat evaluations.

**Reliability reporting**

The evaluator produces structured results identifying whether predefined recommendation behaviors passed or failed.

## 7. Limitations and Potential Biases

### Dataset Representation Bias

With only 15 songs, some genres and moods have limited representation.

Categories with more available songs have more opportunities to appear in recommendations.

### Feature Weighting Bias

Genre receives a larger contribution than mood and energy similarity in the current scoring system.

These fixed weights reflect design decisions rather than preferences learned from actual listeners.

Consequently, the system may emphasize certain musical characteristics more strongly than an individual user would prefer.

### Limited Personalization

The application does not learn from listening history, repeated interactions, skipped songs, favorite artists, or user feedback.

### Missing Context

Music preferences are influenced by cultural background, personal experiences, lyrics, and emotional associations that cannot be adequately represented by the current numerical features.

### Evaluation Scope

The evaluation catalog contains only three synthetic songs.

Successful results demonstrate expected behavior on predefined cases, not generalization to thousands of songs or real listeners.

### No Learned Intelligence

The system uses explicit scoring rules rather than model training, collaborative filtering, or generative AI.

Its reliability evaluator is an engineering extension rather than a learned prediction component.

## 8. Reliability Evaluation and Results

The final project introduces an automated evaluation framework in `src/evaluator.py`.

The evaluator checks six behaviors:

1. Pop recommendation ranking
2. Lofi recommendation ranking
3. Rock recommendation ranking
4. Zero-result handling
5. Recommendation limit handling
6. Explanation generation

Additional pytest suites evaluate core recommendation behavior and input guardrails.

### Automated Test Results

The following results were confirmed during local development:

| Test category | Passed |
|---|---:|
| Recommendation tests | 4 |
| Evaluator tests | 8 |
| Guardrail tests | 8 |
| **Total** | **20** |

**Observed outcome: 20 of 20 automated tests passed.**

This establishes that the implemented behavior satisfied the tested conditions.

It does not demonstrate 100% real-world recommendation accuracy, user satisfaction, or freedom from defects.

### Reliability Observations

During initial development, syntax errors and incorrect package imports prevented the automated test suite from running.

These issues were corrected by restructuring the code, fixing Python annotations, organizing files into the appropriate directories, and executing tests from the project root.

After these corrections, the test suite executed successfully.

A key lesson was that system reliability depends on correct project configuration as well as correct recommendation logic.

## 9. Input Guardrails and Error Handling

The final application includes validation for user preferences and numerical song characteristics.

Examples include:

- Rejecting missing or empty genre and mood values
- Rejecting energy values outside the accepted range
- Rejecting invalid acoustic preference types
- Rejecting non-finite numerical values
- Checking required song metadata
- Validating numeric CSV fields
- Handling zero and negative recommendation limits
- Recording validation failures through Python logging

Invalid data produces descriptive errors instead of being silently accepted into the scoring process.

Logging is intended to assist debugging and reliability evaluation.

Persistent log storage and comprehensive application-wide exception handling are not currently implemented.

## 10. Potential Misuse and Prevention

Although music recommendations are relatively low risk, the system could still be misused or misrepresented.

**Manipulated rankings:** A developer could intentionally change scoring weights to favor particular genres or songs without telling users.

**Misleading accuracy claims:** A perfect automated test pass rate could be incorrectly presented as proof of perfect recommendation accuracy.

**Inappropriate profiling:** Future versions using listening history could collect or infer sensitive information without adequate user consent.

**Unvalidated external data:** Integrating untrusted music catalogs could introduce malformed records or misleading recommendations.

To reduce these risks, the current project uses transparent scoring rules, validation checks, deterministic evaluation, and documented limitations.

The system does not collect personal listening histories, and its evaluation results are described according to the specific conditions tested.

Future versions should incorporate user consent, data minimization, auditability, and appropriate access controls if personal information is introduced.

## 11. Responsible AI Reflection

### What are the limitations or biases in my system?

The most significant limitations are the small dataset, fixed feature weights, and lack of actual listening behavior.

Recommendation rankings depend on the characteristics and priorities selected by the developer.

My earlier experiment demonstrated how increasing the importance of energy could cause songs from different genres to rank more highly.

This showed me that mathematically valid scoring does not necessarily reflect an individual user's actual preferences.

### Could my AI system be misused, and how would I prevent it?

The recommender could be modified to favor selected songs, artists, or musical categories while appearing neutral.

I would reduce this risk through transparent scoring rules, documented changes, evaluation across different user profiles, and clear explanations of recommendation factors.

I would also avoid collecting unnecessary personal information and establish privacy protections before adding real user behavior data.

### What surprised me while testing reliability?

I was surprised by how much project configuration affected testing.

Several failures were caused by malformed Python syntax, incorrect file placement, and the way Python modules were executed, rather than by the recommendation algorithm itself.

For example, running individual test files through the VS Code debugger caused import errors, while executing pytest from the project root allowed the package imports to resolve.

The experience showed me that reliable software requires both correct algorithms and a properly configured development environment.

### How did I collaborate with AI?

I used AI assistance throughout development to review Python code, identify syntax problems, improve project organization, and develop automated evaluation and testing components.

**One suggestion I accepted:**

I accepted the recommendation to create a dedicated reliability evaluator rather than relying exclusively on basic recommendation tests.

This led to the implementation of `src/evaluator.py`, which evaluates ranking behavior, explanation generation, and edge cases using a controlled dataset.

I accepted this approach because it improved the project's reproducibility and provided measurable evidence of expected behavior.

**One suggestion I revised:**

I revised the recommendation to execute Python test files directly through VS Code's Run and Debug interface.

In practice, this caused `ModuleNotFoundError` exceptions because the project package was not being resolved correctly.

I switched to executing tests from the repository root using `python -m pytest -v` and running the evaluator with `python -m src.evaluator`.

This solution was more compatible with the project structure and easier to reproduce.

**What I learned about AI-assisted development:**

AI-generated suggestions still require technical review, execution, and verification.

I learned to evaluate suggestions against actual error messages, project requirements, and test results rather than assuming that generated code or instructions would work without modification.

## 12. Future Improvements

Potential enhancements include:

**Expanded datasets:** Increase genre coverage and the diversity of musical characteristics.

**Additional scoring features:** Experiment with tempo, valence, danceability, and other audio characteristics.

**User-adjustable weights:** Allow listeners to choose whether genre, mood, or energy is most important.

**Feedback-based recommendations:** Introduce explicit ratings or preference feedback.

**Recommendation diversity:** Reduce excessive repetition among recommended genres or artists.

**Human evaluation:** Ask listeners to assess relevance and satisfaction using documented criteria.

**Learning-based models:** Compare the current rules-based implementation with a trained recommendation model when sufficient data becomes available.

**Improved observability:** Add structured evaluation logs, consistent error reporting, and broader integration testing.

## 13. Personal Reflection

This project helped me understand how feature selection, weighting, and validation influence recommendation systems.

My initial focus was on generating personalized results. As development progressed, I recognized the importance of testing, debugging, maintaining clean code, and documenting system limitations.

The most valuable improvement was adding a reliability evaluation framework that checks expected behavior rather than relying on recommendations that simply appear reasonable.

I also gained practical experience with Git, Python package organization, exception handling, automated testing, and technical documentation.

Ultimately, this project reinforced an important principle: a useful AI-related application should not only produce results, but also explain its decisions, handle errors appropriately, and provide evidence that its behavior has been evaluated.

---

**Repository:** https://github.com/JoanneStars/ai110-applied-ai-music-recommender

**Developer:** Joanne Jongeling  
**Course:** CodePath AI110  
**Project:** Applied AI Music Recommender
