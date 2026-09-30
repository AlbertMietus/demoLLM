"""
BDD tests for demoLLM_find_first_sentence CLI.

These tests define the expected behavior of the find_first_sentence CLI.
All tests are marked as xfail until the rekenmodule is implemented.
"""

import subprocess
import sys
from pathlib import Path

CLI_PATH = Path(__file__).parent.parent.parent / "src" / "demo_llm" / "cli" / "demoLLM_find_first_sentence.py"


def run_cli(input_text: str) -> subprocess.CompletedProcess:
    """Run the CLI script with the given input."""
    return subprocess.run(
        [sys.executable, str(CLI_PATH)],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=5
    )


class TestFindFirstSentenceValidInput:
    """Tests for valid input containing complete sentences."""

    
    def test_given_i_love_computers_when_run_then_prints_sentence(self):
        """
        Given: Input "I love computers"
        When: CLI is run
        Then: Prints "I LOVE COMPUTERS"
        """
        result = run_cli("I love computers")
        assert result.returncode == 0
        assert "I LOVE COMPUTERS" in result.stdout

    
    def test_given_you_love_computers_when_run_then_prints_sentence(self):
        """
        Given: Input "You love computers"
        When: CLI is run
        Then: Prints "YOU LOVE COMPUTERS"
        """
        result = run_cli("You love computers")
        assert result.returncode == 0
        assert "YOU LOVE COMPUTERS" in result.stdout

    
    def test_given_i_love_you_when_run_then_prints_sentence(self):
        """
        Given: Input "I love you"
        When: CLI is run
        Then: Prints "I LOVE YOU"
        """
        result = run_cli("I love you")
        assert result.returncode == 0
        assert "I LOVE YOU" in result.stdout


class TestFindFirstSentenceWithPrefix:
    """Tests for input with text before the valid sentence."""

    
    def test_given_unknown_before_sentence_when_run_then_prints_sentence(self):
        """
        Given: Input "hello I love computers"
        When: CLI is run
        Then: Ignores "hello", prints "I LOVE COMPUTERS"
        """
        result = run_cli("hello I love computers")
        assert result.returncode == 0
        assert "I LOVE COMPUTERS" in result.stdout

    
    def test_given_punctuation_before_sentence_when_run_then_prints_sentence(self):
        """
        Given: Input ", I love computers"
        When: CLI is run
        Then: Ignores ",", prints "I LOVE COMPUTERS"
        """
        result = run_cli(", I love computers")
        assert result.returncode == 0
        assert "I LOVE COMPUTERS" in result.stdout


class TestFindFirstSentenceNoValidInput:
    """Tests for input with no valid sentences."""

    
    def test_given_only_unknown_when_run_then_no_output(self):
        """
        Given: Input "hello world"
        When: CLI is run
        Then: No output, exit code 0
        """
        result = run_cli("hello world")
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    
    def test_given_empty_input_when_run_then_no_output(self):
        """
        Given: Empty input
        When: CLI is run
        Then: No output, exit code 0
        """
        result = run_cli("")
        assert result.returncode == 0
        assert result.stdout.strip() == ""
