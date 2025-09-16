"""Pytest configuration for the test suite."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the `src` directory is importable before individual tests run.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
SRC_PATH_STR = str(SRC_PATH)
if SRC_PATH_STR not in sys.path:
    sys.path.insert(0, SRC_PATH_STR)
