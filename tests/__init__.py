"""
Tests for DemoLLM package.

This module contains all tests for the demo LLM implementation.
Tests follow TDD principles with pseudo-BDD naming (given/when/then).
"""

import sys
from pathlib import Path

# Add src directory to path so that pytest can find demo_llm module
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
