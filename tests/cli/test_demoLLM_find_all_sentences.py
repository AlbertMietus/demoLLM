"""
BDD tests for demoLLM_find_all_sentences CLI.

These tests verify that the CLI correctly finds and prints all valid sentences
from input, and prints a summary at the end.
"""

import subprocess
from subprocess import CompletedProcess


class TestDemoLLMFindAllSentences:
    """BDD tests for the find_all_sentences CLI."""

    def test_given_valid_sentence_when_run_then_prints_sentence(self) -> None:
        """
        Given: Input containing a valid sentence
        When: CLI is run
        Then: The valid sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="I love you",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout

    def test_given_multiple_valid_sentences_when_run_then_prints_all(self) -> None:
        """
        Given: Input containing multiple valid sentences
        When: CLI is run
        Then: All valid sentences are printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="I love you I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout
        assert "I LOVE COMPUTERS" in result.stdout

    def test_given_sentence_with_invalid_prefix_when_run_then_ignores_prefix(self) -> None:
        """
        Given: Input with invalid words before valid sentence
        When: CLI is run
        Then: Invalid words are ignored and valid sentence is printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="hello world I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE COMPUTERS" in result.stdout
        assert "hello" not in result.stdout.lower()

    def test_given_sentence_with_invalid_infix_when_run_then_resets_on_invalid(self) -> None:
        """
        Given: Input with invalid words between valid sentences
        When: CLI is run
        Then: Each valid sentence is detected independently
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="I love you hello I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout
        assert "I LOVE COMPUTERS" in result.stdout

    def test_given_stop_token_when_run_then_stops_processing(self) -> None:
        """
        Given: Input containing STOP token
        When: CLI is run
        Then: Processing stops at STOP token
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="I love you STOP I love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout
        assert "I LOVE COMPUTERS" not in result.stdout

    def test_given_multiple_sentences_when_run_then_prints_summary(self) -> None:
        """
        Given: Input containing multiple valid sentences
        When: CLI is run
        Then: Summary with counts is printed at the end
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="I love computers I love computers",
            text=True,
            capture_output=True
        )

        # Check that summary contains the sentence and count (4 because each word sequence is detected)
        assert "I LOVE COMPUTERS: 4" in result.stdout

    def test_given_no_valid_sentences_when_run_then_no_output(self) -> None:
        """
        Given: Input with no valid sentences
        When: CLI is run
        Then: No sentences are printed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
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
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="",
            text=True,
            capture_output=True
        )

        assert result.stdout.strip() == ""

    def test_given_multiline_input_when_run_then_processes_all_lines(self) -> None:
        """
        Given: Multiline input
        When: CLI is run
        Then: All lines are processed
        """
        result: CompletedProcess = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_find_all_sentences"],
            input="I love you\nI love computers",
            text=True,
            capture_output=True
        )

        assert "I LOVE YOU" in result.stdout
        assert "I LOVE COMPUTERS" in result.stdout
