"""
BDD tests for demoLLM_validate_tokens CLI.

These tests verify that the CLI correctly validates input tokens.
"""

from test.cli.base import BaseCLITest


class TestDemoLLMValidateTokens(BaseCLITest):
    """BDD tests for the validate_tokens CLI."""

    def test_given_all_valid_tokens_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with all valid tokens
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I YOU LOVE COMPUTERS")

        assert result.returncode == 0

    def test_given_valid_sentence_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with a valid sentence
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I love computers")

        assert result.returncode == 0

    def test_given_unknown_word_when_run_then_exits_one(self) -> None:
        """
        Given: Input with an unknown word
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I love hello")

        assert result.returncode == 1

    def test_given_punctuation_when_run_then_exits_one(self) -> None:
        """
        Given: Input with punctuation
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I love computers.")

        assert result.returncode == 1

    def test_given_word_with_punctuation_when_run_then_exits_one(self) -> None:
        """
        Given: Input with word containing punctuation
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I love, computers")

        assert result.returncode == 1

    def test_given_empty_input_when_run_then_exits_zero(self) -> None:
        """
        Given: Empty input
        When: CLI is run
        Then: Exit code is 0 (True - no invalid tokens)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "")

        assert result.returncode == 0

    def test_given_mixed_valid_and_invalid_when_run_then_exits_one(self) -> None:
        """
        Given: Input with both valid and invalid tokens
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I love hello computers")

        assert result.returncode == 1

    def test_given_only_valid_no_invalid_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with only valid tokens and no invalid ones
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I YOU LOVE COMPUTERS I")

        assert result.returncode == 0

    def test_given_case_insensitive_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with valid tokens in different cases
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "i you love computers")

        assert result.returncode == 0

    def test_given_no_output_when_run_then_prints_nothing(self) -> None:
        """
        Given: Any input
        When: CLI is run
        Then: Nothing is printed to stdout or stderr
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens", "I love computers")

        assert result.stdout == ""
        assert result.stderr == ""
