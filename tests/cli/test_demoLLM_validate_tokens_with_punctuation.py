"""
BDD tests for demoLLM_validate_tokens_with_punctuation CLI (CLI3b).

These tests verify that the CLI correctly validates input tokens
with PSEUDO_PUNCTUATION allowed.
"""

import subprocess
from subprocess import CompletedProcess


class TestDemoLLMValidateTokensWithPunctuation:
    """BDD tests for the validate_tokens_with_punctuation CLI."""

    def test_given_all_valid_tokens_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with all valid tokens
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="I YOU LOVE COMPUTERS",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_punctuation_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with punctuation
        When: CLI is run
        Then: Exit code is 0 (True - punctuation is valid in CLI3b)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="I love computers .",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_word_with_punctuation_when_run_then_exits_one(self) -> None:
        """
        Given: Input with word containing punctuation
        When: CLI is run
        Then: Exit code is 1 (False - words with punctuation are UNKNOWN)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="I love, computers",
            text=True,
            capture_output=True
        )

        assert result.returncode == 1

    def test_given_unknown_word_when_run_then_exits_one(self) -> None:
        """
        Given: Input with an unknown word
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="I love hello",
            text=True,
            capture_output=True
        )

        assert result.returncode == 1

    def test_given_empty_input_when_run_then_exits_zero(self) -> None:
        """
        Given: Empty input
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_punctuation_only_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with only punctuation
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input=" . , ! ?",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_mixed_valid_and_punctuation_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with valid tokens and punctuation
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="I love computers . I love you !",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_no_output_when_run_then_prints_nothing(self) -> None:
        """
        Given: Any input
        When: CLI is run
        Then: Nothing is printed to stdout or stderr
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens_with_punctuation"],
            input="I love computers .",
            text=True,
            capture_output=True
        )

        assert result.stdout == ""
        assert result.stderr == ""
