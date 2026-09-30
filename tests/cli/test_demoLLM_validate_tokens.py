"""
BDD tests for demoLLM_validate_tokens CLI.

These tests define the expected behavior of the validate_tokens CLI.
All tests are marked as xfail until the rekenmodule is implemented.
"""

import subprocess
import sys
from pathlib import Path

CLI_PATH = Path(__file__).parent.parent.parent / "src" / "demo_llm" / "cli" / "demoLLM_validate_tokens.py"


def run_cli(input_text: str) -> subprocess.CompletedProcess:
    """Run the CLI script with the given input."""
    return subprocess.run(
        [sys.executable, str(CLI_PATH)],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=5
    )


class TestValidateTokensBasic:
    """Basic validation tests."""

    
    def test_given_valid_sentence_when_run_then_exit_0(self):
        """
        Given: Input "I love computers"
        When: CLI is run
        Then: Exit code is 0 (all tokens valid)
        """
        result = run_cli("I love computers")
        assert result.returncode == 0

    
    def test_given_unknown_word_when_run_then_exit_1(self):
        """
        Given: Input "hello"
        When: CLI is run
        Then: Exit code is 1 (contains UNKNOWN token)
        """
        result = run_cli("hello")
        assert result.returncode == 1


class TestValidateTokensPunctuation:
    """Tests for punctuation handling."""

    
    def test_given_word_with_punctuation_when_run_then_exit_1(self):
        """
        Given: Input "I love, computers"
        When: CLI is run
        Then: Exit code is 1 (contains PUNCTUATION or UNKNOWN token)
        
        TODO: Design decision needed - see bug_handling.rst
        - Option A: "love," = 1 token (PSEUDO_UNKNOWN)
        - Option B: "love," = 2 tokens (LOVE + PSEUDO_PUNCTUATION)
        Current assumption: Option A (1 token, UNKNOWN)
        """
        result = run_cli("I love, computers")
        assert result.returncode == 1

    
    def test_given_punctuation_only_when_run_then_exit_1(self):
        """
        Given: Input ","
        When: CLI is run
        Then: Exit code is 1 (PUNCTUATION token invalid in this CLI)
        """
        result = run_cli(",")
        assert result.returncode == 1


class TestValidateTokensNoOutput:
    """Tests that CLI prints nothing."""

    
    def test_given_any_input_when_run_then_no_output(self):
        """
        Given: Any input
        When: CLI is run
        Then: No output to stdout or stderr
        """
        result = run_cli("I love computers")
        assert result.stdout == ""
        assert result.stderr == ""
