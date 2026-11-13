"""Optional C++17 Euclidean distance backend with safe Python fallback.

The C++ shared library is locally built, and may be blocked by Windows
application-control policy. The backend never bypasses OS security controls.
"""

from __future__ import annotations

import ctypes
import math
import os
import sys
from pathlib import Path
from typing import Sequence


def python_distance(left: Sequence[float], right: Sequence[float]) -> float:
    """Reference implementation used for fallback and parity testing."""
    if not left or len(left) != len(right):
        raise ValueError("Feature vectors must be nonempty and equal length.")
    if any(not math.isfinite(float(x)) for x in (*left, *right)):
        raise ValueError("Feature vectors must contain finite values.")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


class DistanceBackend:
    """Load the optional native backend; fall back cleanly to Python."""

    def __init__(self, library_path: str | Path | None = None):
        self.backend = "Python fallback"
        self._function = None
        root = Path(__file__).resolve().parents[1]
        if sys.platform == "win32":
            names = ("vibematch_distance.dll",)
        elif sys.platform == "darwin":
            names = ("libvibematch_distance.dylib",)
        else:
            names = ("libvibematch_distance.so",)

        configured = library_path or os.environ.get("VIBEMATCH_NATIVE_LIB")
        candidates = [Path(configured)] if configured else []
        for name in names:
            candidates.extend((
                root / "cpp" / "build" / name,
                root / "cpp" / "build" / "Release" / name,
                root / "cpp" / "build" / "Debug" / name,
            ))

        for candidate in candidates:
            if not candidate.is_file():
                continue
            try:
                library = ctypes.CDLL(str(candidate.resolve()))
                function = library.vm_euclidean_distance
                function.argtypes = (
                    ctypes.POINTER(ctypes.c_double),
                    ctypes.POINTER(ctypes.c_double),
                    ctypes.c_size_t,
                )
                function.restype = ctypes.c_double
                self._library = library  # keep DLL handle alive
                self._function = function
                self.backend = "C++17 native"
                self.library_path = str(candidate.resolve())
                break
            except (OSError, AttributeError):
                # Includes Windows application-control blocks. Never bypass.
                continue

    def distance(self, left: Sequence[float], right: Sequence[float]) -> float:
        """Validate inputs and calculate distance using the available backend."""
        values_left = tuple(float(x) for x in left)
        values_right = tuple(float(x) for x in right)
        if not values_left or len(values_left) != len(values_right):
            raise ValueError("Feature vectors must be nonempty and equal length.")
        if not all(math.isfinite(x) for x in (*values_left, *values_right)):
            raise ValueError("Feature vectors must contain finite values.")
        if self._function is None:
            return python_distance(values_left, values_right)
        n = len(values_left)
        c_left = (ctypes.c_double * n)(*values_left)
        c_right = (ctypes.c_double * n)(*values_right)
        answer = self._function(c_left, c_right, n)
        if not math.isfinite(answer):
            raise ValueError("Native distance returned an invalid result.")
        return float(answer)
