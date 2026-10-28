# (C) 2026 Albert Mietus -- mostly made by codeAI=mistral-medium-3-5

"""
BDD tests for demoLLM_validate_tokens_with_punctuation CLI (CLI3b).

These tests verify that the CLI correctly validates input tokens
with PSEUDO_PUNCTUATION allowed.
"""

from pytst.cli.base import BaseCLITest


class TestDemoLLMValidateTokensWithPunctuation(BaseCLITest):
    """BDD tests for the validate_tokens_with_punctuation CLI."""

    def test_given_all_valid_tokens_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with all valid tokens
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "I YOU LOVE COMPUTERS")

        assert result.returncode == 0

    def test_given_punctuation_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with punctuation
        When: CLI is run
        Then: Exit code is 0 (True - punctuation is valid in CLI3b)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "I love computers .")

        assert result.returncode == 0

    def test_given_word_with_punctuation_when_run_then_exits_one(self) -> None:
        """
        Given: Input with word containing punctuation
        When: CLI is run
        Then: Exit code is 1 (False - words with punctuation are UNKNOWN)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "I love, computers")

        assert result.returncode == 1

    def test_given_unknown_word_when_run_then_exits_one(self) -> None:
        """
        Given: Input with an unknown word
        When: CLI is run
        Then: Exit code is 1 (False)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "I love hello")

        assert result.returncode == 1

    def test_given_empty_input_when_run_then_exits_zero(self) -> None:
        """
        Given: Empty input
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "")

        assert result.returncode == 0

    def test_given_punctuation_only_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with only punctuation
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", " . , ! ?")

        assert result.returncode == 0

    def test_given_mixed_valid_and_punctuation_when_run_then_exits_zero(self) -> None:
        """
        Given: Input with valid tokens and punctuation
        When: CLI is run
        Then: Exit code is 0 (True)
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "I love computers . I love you !")

        assert result.returncode == 0

    def test_given_no_output_when_run_then_prints_nothing(self) -> None:
        """
        Given: Any input
        When: CLI is run
        Then: Nothing is printed to stdout or stderr
        """
        result = self.run_cli("demoLLM.cli.demoLLM_validate_tokens_with_punctuation", "I love computers .")

        assert result.stdout == ""
        assert result.stderr == ""
