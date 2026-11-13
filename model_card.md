# Model Card: VibeMatch Fusion
### Hybrid Python & C++17 Music Recommendation System

**Developer:** Joanne Jongeling  
**Course:** CodePath AI110 — Final Project  
**Version:** 3.0  
**Programming Languages:** Python 3.13 and C++17  
**Technologies:** Streamlit, CMake, ctypes, pytest, GitHub Actions  
**Architecture:** Cross-platform Python application with native C++ computation and automatic Python fallback

## 1. System Overview

VibeMatch Fusion is a hybrid Python and C++17 music recommendation application that integrates content-based filtering, feature-vector similarity, and unsupervised machine learning.

The project originated from my original CodePath AI110 Module 3 Music Recommender Simulation, which I developed using Python and algorithmic recommendation techniques.

For my final project, I expanded the original application by introducing a fitted k-means clustering model and proposing a cross-platform architecture that combines Python's application and machine-learning capabilities with native C++17 computation.

**Python serves as the primary application and machine-learning layer**, handling the Streamlit interface, recommendation algorithms, clustering, input validation, and testing.

**C++17 serves as the native computation layer**, performing Euclidean distance calculations through a compiled library. Python communicates with this library using `ctypes`.

The system automatically uses a Python fallback when the native C++ library is unavailable.

This architecture allows the application to combine Python's flexibility with compiled C++ functionality while maintaining portability.

## 2. Python and C++17 Architecture

| Component | Language | Responsibility |
|---|---|---|
| Streamlit dashboard | Python | Interactive user interface |
| Content-based recommender | Python | Weighted scoring and ranking |
| Feature-vector engine | Python | Numerical similarity recommendations |
| Fitted k-means model | Python | Unsupervised machine learning |
| Native distance engine | C++17 | Compiled Euclidean distance calculations |
| Native integration | Python / C++17 | Communication through `ctypes` |
| Automated testing | Python | Unit and integration verification |
| Build configuration | CMake | Native library compilation |

### Verified Native Integration

The C++17 component was successfully compiled on Windows and loaded by the Python application.

```text
Backend: C++17 native
Distance: 5.0
```

The complete application also passed **36 automated tests**, with **10/10 reliability checks** passing.

The Windows integration is verified locally. Linux and macOS compatibility remains subject to separate cross-platform testing.
