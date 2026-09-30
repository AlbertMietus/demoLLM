"""
BDD tests for demoLLM_find_all_sentences CLI.

These tests define the expected behavior of the find_all_sentences CLI.
All tests are marked as xfail until the rekenmodule is implemented.
"""

import subprocess
import sys
from pathlib import Path

CLI_PATH = Path(__file__).parent.parent.parent / "src" / "demo_llm" / "cli" / "demoLLM_find_all_sentences.py"


def run_cli(input_text: str) -> subprocess.CompletedProcess:
    """Run the CLI script with the given input."""
    return subprocess.run(
        [sys.executable, str(CLI_PATH)],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=5
    )


class TestFindAllSentencesMultipleSentences:
    """Tests for input containing multiple valid sentences."""

    
    def test_given_two_sentences_when_run_then_prints_both(self):
        """
        Given: Input "I love computers I love you"
        When: CLI is run
        Then: Prints both "I LOVE COMPUTERS" and "I LOVE YOU"
        """
        result = run_cli("I love computers I love you")
        assert result.returncode == 0
        assert "I LOVE COMPUTERS" in result.stdout
        assert "I LOVE YOU" in result.stdout


class TestFindAllSentencesSummary:
    """Tests for the summary output."""

    
    def test_given_two_sentences_when_run_then_summary_shows_both(self):
        """
        Given: Input "I love computers I love you"
        When: CLI is run
        Then: Summary shows both sentences with count 1
        """
        result = run_cli("I love computers I love you")
        assert result.returncode == 0
        assert "I LOVE COMPUTERS: 1" in result.stdout
        assert "I LOVE YOU: 1" in result.stdout


class TestFindAllSentencesWithUnknown:
    """Tests for input with unknown words."""

    
    def test_given_unknown_before_sentence_when_run_then_prints_sentence(self):
        """
        Given: Input "hello I love computers"
        When: CLI is run
        Then: Ignores "hello", prints "I LOVE COMPUTERS" and summary
        """
        result = run_cli("hello I love computers")
        assert result.returncode == 0
        assert "I LOVE COMPUTERS" in result.stdout
        assert "I LOVE COMPUTERS: 1" in result.stdout


class TestFindAllSentencesNoValidInput:
    """Tests for input with no valid sentences."""

    
    def test_given_only_unknown_when_run_then_no_output(self):
        """
        Given: Input "hello world"
        When: CLI is run
        Then: No sentences printed, no summary
        """
        result = run_cli("hello world")
        assert result.returncode == 0
        lines = [l for l in result.stdout.strip().split('\n') if l.strip()]
        assert len(lines) == 0
