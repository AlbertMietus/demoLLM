"""
BDD tests for demoLLM_find_first_sentence CLI.

These tests verify that the CLI correctly finds and prints the first valid
sentence from input, then exits.
"""

import subprocess
from subprocess import CompletedProcess


class TestDemoLLMFindFirstSentence:
    """BDD tests for the find_first_sentence CLI."""

    def test_given_valid_sentence_when_run_then_prints_sentence(self) -> None:
        """
        Given: Input containing a valid sentence
        When: CLI is run
        Then: The first valid sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="I love you",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout

    def test_given_multiple_sentences_when_run_then_prints_first_only(self) -> None:
        """
        Given: Input containing multiple valid sentences
        When: CLI is run
        Then: Only the first valid sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="I love you I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout
        assert "I LOVE COMPUTERS" not in result.stdout

    def test_given_sentence_with_invalid_prefix_when_run_then_prints_sentence(self) -> None:
        """
        Given: Input with invalid words before valid sentence
        When: CLI is run
        Then: Invalid words are ignored and first valid sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="hello world I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE COMPUTERS" in result.stdout
        assert "hello" not in result.stdout.lower()

    def test_given_sentence_with_invalid_infix_when_run_then_prints_first(self) -> None:
        """
        Given: Input with invalid words between valid sentences
        When: CLI is run
        Then: First valid sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="I love you hello I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout

    def test_given_no_valid_sentences_when_run_then_no_output(self) -> None:
        """
        Given: Input with no valid sentences
        When: CLI is run
        Then: No output is produced
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="hello world test",
            text=True,
            capture_output=True
        )

        assert result.stdout.strip() == ""

    def test_given_empty_input_when_run_then_no_output(self) -> None:
        """
        Given: Empty input
        When: CLI is run
        Then: No output is produced
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="",
            text=True,
            capture_output=True
        )

        assert result.stdout.strip() == ""

    def test_given_multiline_input_when_run_then_processes_all_lines(self) -> None:
        """
        Given: Multiline input
        When: CLI is run
        Then: All lines are processed until first sentence found
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="hello\nI love you",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout

    def test_given_valid_sentence_at_start_when_run_then_prints_immediately(self) -> None:
        """
        Given: Valid sentence at the start of input
        When: CLI is run
        Then: Sentence is printed immediately
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="I love computers more text",
            text=True,
            capture_output=True
        )

        assert "I LOVE COMPUTERS" in result.stdout

    def test_given_partial_sentence_when_run_then_no_output(self) -> None:
        """
        Given: Input with only part of a sentence
        When: CLI is run
        Then: No output is produced
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="I love",
            text=True,
            capture_output=True
        )

        assert result.stdout.strip() == ""

    def test_given_exact_sentence_when_run_then_prints_sentence(self) -> None:
        """
        Given: Input with exact valid sentence
        When: CLI is run
        Then: The sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_first_sentence"],
            input="You love computers",
            text=True,
            capture_output=True
        )

        assert "YOU LOVE COMPUTERS" in result.stdout
