
# AI Interactions Log

**Project:** VibeMatch Applied AI Music Recommender
**Version:** 2.0
**Developer:** Joanne Jongeling
**Course:** CodePath AI110

---

## 1. AI-Assisted Development Overview

AI assistance was used throughout the development of VibeMatch to support programming, debugging, system design, testing, and documentation.

The project began as a Module 3 content-based music recommender and was extended into a more reliable applied AI system.

AI assisted with:

- Recommendation algorithm design
- Feature-weighting experiments
- Python code organization
- Syntax and import debugging
- Automated reliability evaluation
- Input validation and error handling
- Streamlit interface development
- System architecture documentation
- Responsible AI analysis

All AI-assisted changes were reviewed and tested during development.

AI functioned as a development assistant, not as an autonomous agent operating within the recommendation application.

---

## 2. Development Workflow

### Task Given to AI

I asked AI to help improve an existing Python music recommendation system while preserving its original functionality.

My goals were to:

1. Improve code readability and maintainability.
2. Add automated reliability evaluation.
3. Validate user preferences and song data.
4. Resolve Python and Git errors.
5. Create an interactive music recommendation dashboard.
6. Document the system professionally.

### Representative Prompts

The following prompts reflect requests made during development:

- "Help me create a scoring system for a music recommender."
- "Give me the full updated code."
- "Make sure the code is good, condensed, easy to read, professional and updated."
- "What code do I put in tests/test_evaluator.py?"
- "Let's add input validation and reliability guardrails."
- "What do we put in architecture.mmd?"
- "Update the README to explain what we encountered, how we fixed it, and how it works."
- "Make the dashboard more futuristic with galaxy and aura colors."

These interactions guided the project's development and revisions.

---

## 3. Recommendation System Design

### AI Contribution

AI helped organize the recommendation engine around three data structures:

- `Song`
- `UserProfile`
- `Recommender`

It also helped develop a shared scoring function for comparing user preferences with song features.

### My Contribution

I reviewed the scoring rules, compared recommendation results, and experimented with feature weights.

During Module 3, I tested the effect of reducing genre importance and increasing energy importance.

This demonstrated that feature weights influence which songs appear in the highest rankings.

### Final Decision

The final system uses a transparent content-based scoring algorithm.

Its current maximum scoring contributions are:

| Feature | Maximum Points |
|---|---:|
| Genre | 2.0 |
| Mood | 1.0 |
| Energy similarity | 1.0 |
| Acoustic preference | 0.5 |

The system ranks songs according to these scores and provides explanations.

---

## 4. Reliability Evaluation Development

### Problem

The original project had limited automated testing and did not provide a dedicated reliability evaluation report.

### AI Suggestion

AI recommended creating a separate evaluation module to measure recommendation behavior.

### Implementation

I added:

`src/evaluator.py`

The evaluator checks:

1. Pop recommendation ranking
2. Lofi recommendation ranking
3. Rock recommendation ranking
4. Zero-result handling
5. Recommendation limits
6. Explanation generation

Each evaluation produces a pass/fail result and a diagnostic message.

### Verification

I executed the evaluator locally using:

`python -m src.evaluator`

This provided a reproducible method for examining expected recommendation behavior.

The evaluator uses deterministic scoring and predefined test cases. It does not use an autonomous agent or a generative AI model.

---

## 5. Automated Testing

### Task Given to AI

Help develop a professional testing structure for the recommendation engine and evaluation system.

### AI Contribution

AI assisted with writing automated tests for:

- Recommendation ranking
- Recommendation explanations
- Recommendation limits
- Controlled evaluation profiles
- Evaluation reports
- Input validation
- Invalid numerical values
- Malformed song attributes

### Files Developed

- `tests/test_recommender.py`
- `tests/test_evaluator.py`
- `tests/test_guardrails.py`

### Test Results

During local development, I confirmed that 20 automated tests passed.

| Test Category | Passed |
|---|---:|
| Recommendation tests | 4 |
| Evaluator tests | 8 |
| Guardrail tests | 8 |
| **Total** | **20** |

Command:

`python -m pytest -v`

The result demonstrates successful execution of the defined tests, not perfect recommendation accuracy.

---

## 6. Debugging and Error Resolution

AI assistance was useful in identifying errors and proposing corrections.

### Issue 1: Python Syntax Errors

**Error:** `SyntaxError`

**Cause:** Malformed type annotations and indentation problems.

**Resolution:** Corrected annotations, indentation, and function definitions.

### Issue 2: Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'src'`

**Cause:** Python files were being executed directly without the expected package context.

**Resolution:** Executed tests and evaluator modules from the repository root.

Commands:

`python -m pytest -v`

`python -m src.evaluator`

### Issue 3: Incorrect File Organization

**Problem:** Some tests and diagrams were created inside nested folders.

**Resolution:** Reorganized files into dedicated `src`, `tests`, and `diagrams` directories.

### Issue 4: Git Push Failure

**Error:** `src refspec HEAD does not match any`

**Cause:** The initial new repository did not contain a commit.

**Resolution:** Cloned the original project, configured the new remote, and pushed the existing commit history.

### Issue 5: Streamlit Import Failure

**Error:** `ImportError: attempted relative import with no known parent package`

**Resolution:** Changed the application to use an absolute package import:

`from src.recommender import load_songs, recommend_songs`

### Issue 6: Streamlit Indentation Error

**Error:** `IndentationError`

**Cause:** An incomplete `if __name__ == "__main__":` block.

**Resolution:** Corrected the application entry point and updated the Streamlit implementation.

### Verification Method

I tested solutions using actual terminal commands and reviewed the resulting error messages before proceeding.

This process demonstrated why AI-generated suggestions must be verified rather than accepted automatically.

---

## 7. Input Validation and Guardrails

### AI Contribution

AI suggested validating user preferences and song data before allowing them to influence recommendation scores.

### Implementation

The recommendation engine now checks:

- Missing genre or mood values
- Invalid energy values
- Non-finite numerical values
- Incorrect acoustic preference types
- Invalid song metadata
- Malformed CSV numerical fields

Validation failures produce descriptive errors.

Python logging records relevant validation failures for debugging.

### Verification

I added automated guardrail tests and executed them using pytest.

These tests confirm expected behavior for the cases covered by the test suite.

---

## 8. Streamlit Dashboard Development

### Task Given to AI

Help transform the original music recommendation application into a professional, interactive dashboard.

### Implementation

The interface was developed using Streamlit.

It includes:

- Genre and mood selection
- Energy preference controls
- Acoustic preference selection
- Adjustable recommendation limits
- Ranked recommendation cards
- Match scores
- Expandable explanations
- Dataset summary metrics

### Visual Design

I requested a futuristic galaxy-inspired interface with a dark navy background and purple, violet, and cyan aura colors.

AI assisted with custom CSS for:

- Animated starfield effects
- Moving nebula gradients
- Glass-style panels
- Glowing controls
- Sleek typography
- Holographic orbital animations
- Energy-responsive visual effects

### Manual Verification

I launched the Streamlit application in a browser and confirmed that the dashboard displayed correctly.

I also confirmed that the recommendation interface functioned after the code and design revisions.

The holographic orb is a visual representation of the selected energy preference. It does not perform audio analysis or influence the recommendation algorithm.

---

## 9. Object-Oriented Design Pattern (SF10)

### Which Design Pattern Did I Use?

Object-oriented design using `Song`, `UserProfile`, and `Recommender`.

### How Did AI Help?

AI helped explain how responsibilities could be separated into dedicated classes and functions.

This improved the organization and readability of the code.

### How Does the Pattern Appear in the Final Application?

**Song**

Represents music metadata and numerical audio attributes.

**UserProfile**

Represents the listener's music preferences.

**Recommender**

Provides an object-oriented interface for ranking and explaining song recommendations.

The application also separates user-interface rendering, validation, scoring, and reliability evaluation.

### Why This Pattern Was Appropriate

Object-oriented design made the recommendation engine easier to organize and test without combining every responsibility into one large function.

---

## 10. Agentic Workflow Discussion (SF8)

### Did the Final Application Implement an Autonomous Agent?

No.

AI assistance was used during software development, but the deployed music recommender does not contain an autonomous planning or tool-calling agent.

The final application uses deterministic scoring and a separate reliability evaluation workflow.

### How Did AI Support the Development Workflow?

AI assisted with a repeated development process:

1. Identify a problem or improvement.
2. Suggest a code change.
3. Implement the change.
4. Run tests or launch the application.
5. Review errors or unexpected behavior.
6. Revise the implementation.

This was a human-directed development workflow rather than an autonomous agent integrated into the application.

### Future Agentic Enhancement

A future version could include a recommendation evaluation agent that:

1. Generates test profiles.
2. Runs recommendation experiments.
3. Checks output against validation rules.
4. Records failures.
5. Suggests improvements for human review.

Such an enhancement would require its own implementation and testing before being claimed as an application feature.

---

## 11. AI Suggestions Accepted and Revised

### Accepted Suggestion: Reliability Evaluator

I accepted the suggestion to create a dedicated reliability evaluation module.

This improved the application by providing repeatable checks for recommendation behavior and edge cases.

The evaluator was integrated into the project as `src/evaluator.py`.

### Revised Suggestion: Running Python Files Directly

I revised the suggested approach of executing individual test files directly through the VS Code debugger.

That approach caused package import errors.

Instead, I used module-based commands from the repository root.

This was easier to reproduce and worked with the project's package structure.

### Key Lesson

AI assistance accelerated development, but successful results depended on testing, reviewing errors, and making informed engineering decisions.

---

## 12. Final Reflection

Building VibeMatch helped me understand how recommendation algorithms use feature weighting, similarity scoring, and ranking to generate personalized suggestions.

Extending the original application introduced additional responsibilities involving validation, reliability evaluation, software testing, debugging, and user-interface development.

I learned that AI assistance is most useful when its suggestions are reviewed critically and verified against actual system behavior.

The final project reflects an iterative development process in which technical problems were identified, investigated, corrected, and tested.

---

**Repository:** https://github.com/JoanneStars/ai110-applied-ai-music-recommender

**Developer:** Joanne Jongeling  
**Course:** CodePath AI110  
**Project:** VibeMatch Applied AI Music Recommender
