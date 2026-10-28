# (C) 2026 Albert Mietus -- mostly made by codeAI=mistral-medium-3-5

"""
Base test class for CLI tests.

This module provides a base class with helper methods to reduce code duplication
in CLI tests.
"""

import subprocess
from subprocess import CompletedProcess


class BaseCLITest:
    """Base class for CLI tests with helper methods."""

    @staticmethod
    def run_cli(module_path: str, input_text: str = "") -> CompletedProcess:
        """
        Run a CLI module with the given input.

        Args:
            module_path: The module path to run (e.g., "demoLLM.cli.demoLLM_find_all_sentences")
            input_text: The input text to pass to stdin

        Returns:
            CompletedProcess with stdout, stderr, and returncode
        """
        return subprocess.run(
            ["python", "-m", module_path],
            input=input_text,
            text=True,
            capture_output=True
        )
