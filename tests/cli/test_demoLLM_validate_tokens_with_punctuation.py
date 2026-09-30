"""
BDD tests for demoLLM_validate_tokens_with_punctuation CLI (CLI3b).

These tests define the expected behavior of the validate_tokens_with_punctuation CLI.
All tests are marked as xfail until the rekenmodule is implemented.
"""

import subprocess
import sys
from pathlib import Path

CLI_PATH = Path(__file__).parent.parent.parent / "src" / "demo_llm" / "cli" / "demoLLM_validate_tokens_with_punctuation.py"


def run_cli(input_text: str) -> subprocess.CompletedProcess:
    """Run the CLI script with the given input."""
    return subprocess.run(
        [sys.executable, str(CLI_PATH)],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=5
    )


class TestValidateTokensWithPunctuationBasic:
    """Basic validation tests with punctuation allowed."""

    
    def test_given_valid_sentence_when_run_then_exit_0(self):
        """
        Given: Input "I love computers"
        When: CLI is run
        Then: Exit code is 0 (all tokens valid)
        """
        result = run_cli("I love computers")
        assert result.returncode == 0

    
    def test_given_punctuation_when_run_then_exit_0(self):
        """
        Given: Input ","
        When: CLI is run
        Then: Exit code is 0 (PUNCTUATION is valid in this CLI)
        """
        result = run_cli(",")
        assert result.returncode == 0

    
    def test_given_word_with_punctuation_when_run_then_exit_0(self):
        """
        Given: Input "I love, computers"
        When: CLI is run
        Then: Exit code is 0 (PUNCTUATION is valid in this CLI)
        
        TODO: Design decision - if "love," splits into [LOVE, PUNCTUATION],
        both are valid in this CLI.
        """
        result = run_cli("I love, computers")
        assert result.returncode == 0


class TestValidateTokensWithPunctuationInvalid:
    """Tests for invalid tokens (UNKNOWN only)."""

    
    def test_given_unknown_word_when_run_then_exit_1(self):
        """
        Given: Input "hello"
        When: CLI is run
        Then: Exit code is 1 (UNKNOWN token invalid)
        """
        result = run_cli("hello")
        assert result.returncode == 1


class TestValidateTokensWithPunctuationNoOutput:
    """Tests that CLI prints nothing."""

    @pytest.mark.xfail(reason="rekenmodule not implemented")
    def test_given_any_input_when_run_then_no_output(self):
        """
        Given: Any input
        When: CLI is run
        Then: No output to stdout or stderr
        """
        result = run_cli("I love computers")
        assert result.stdout == ""
        assert result.stderr == ""
