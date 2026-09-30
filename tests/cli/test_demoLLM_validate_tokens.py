"""
BDD tests for demoLLM_validate_tokens CLI.

These tests verify that the CLI correctly validates input tokens.
"""

import subprocess
from subprocess import CompletedProcess


class TestDemoLLMValidateTokens:
    """BDD tests for the validate_tokens CLI."""

    def test_given_all_valid_tokens_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with all valid tokens
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I YOU LOVE COMPUTERS",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_valid_sentence_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with a valid sentence
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love computers",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_unknown_word_when_run_then_exits_one(self) -> None:
        """
        Given: Input with an unknown word
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love hello",
            text=True,
            capture_output=True
        )

        assert result.returncode == 1

    def test_given_punctuation_when_run_then_exits_one(self) -> None:
        """
        Given: Input with punctuation
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love computers.",
            text=True,
            capture_output=True
        )

        assert result.returncode == 1

    def test_given_word_with_punctuation_when_run_then_exits_one(self) -> None:
        """
        Given: Input with word containing punctuation
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love, computers",
            text=True,
            capture_output=True
        )

        assert result.returncode == 1

    def test_given_empty_input_when_run_then_exits_zero(self) -> None:
        """
        Given: Empty input
        When: CLI is run
        Then: Exit code is 0 (True - no invalid tokens)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_mixed_valid_and_invalid_when_run_then_exits_one(self) -> None:
        """
        Given: Input with both valid and invalid tokens
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love hello computers",
            text=True,
            capture_output=True
        )

        assert result.returncode == 1

    def test_given_only_valid_no_invalid_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with only valid tokens and no invalid ones
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I YOU LOVE COMPUTERS I",
            text=True,
            capture_output=True
        )

        assert result.returncode == 0

    def test_given_case_insensitive_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with valid tokens in different cases
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="i you love computers",
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
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love computers",
            text=True,
            capture_output=True
        )

        assert result.stdout == ""
        assert result.stderr == ""
