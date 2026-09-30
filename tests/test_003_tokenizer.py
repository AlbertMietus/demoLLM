"""
TDD tests for the tokenizer function (test-003 series).

These tests define the requirements for the tokenize_word function.

Implementation follows Option A: words with punctuation are PSEUDO_UNKNOWN.
"""

import pytest


class TestTokenizerKnownWords:
    """Tests for tokenizing known words."""

    def test_given_word_i_when_tokenize_then_returns_i_token(self):
        """
        Given: Word "I"
        When: tokenize_word is called
        Then: Returns the I token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import I

        result = tokenize_word("I")
        assert result == I

    def test_given_word_you_when_tokenize_then_returns_you_token(self):
        """
        Given: Word "YOU"
        When: tokenize_word is called
        Then: Returns the YOU token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import YOU

        result = tokenize_word("YOU")
        assert result == YOU

    def test_given_word_love_when_tokenize_then_returns_love_token(self):
        """
        Given: Word "LOVE"
        When: tokenize_word is called
        Then: Returns the LOVE token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import LOVE

        result = tokenize_word("LOVE")
        assert result == LOVE

    def test_given_word_computers_when_tokenize_then_returns_computers_token(self):
        """
        Given: Word "COMPUTERS"
        When: tokenize_word is called
        Then: Returns the COMPUTERS token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import COMPUTERS

        result = tokenize_word("COMPUTERS")
        assert result == COMPUTERS

    def test_given_word_case_insensitive_when_tokenize_then_returns_correct_token(self):
        """
        Given: Word in lowercase or mixed case
        When: tokenize_word is called
        Then: Returns the correct token (case-insensitive)
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import I, YOU, LOVE, COMPUTERS

        assert tokenize_word("i") == I
        assert tokenize_word("you") == YOU
        assert tokenize_word("love") == LOVE
        assert tokenize_word("computers") == COMPUTERS


class TestTokenizerUnknownWords:
    """Tests for tokenizing unknown words."""

    def test_given_unknown_word_when_tokenize_then_returns_unknown_token(self):
        """
        Given: An unknown word
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN

        result = tokenize_word("UNKNOWN")
        assert result == PSEUDO_UNKNOWN

    def test_given_empty_string_when_tokenize_then_returns_punctuation_token(self):
        """
        Given: An empty string
        When: tokenize_word is called
        Then: Returns PSEUDO_PUNCTUATION token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_PUNCTUATION

        result = tokenize_word("")
        assert result == PSEUDO_PUNCTUATION

    def test_given_whitespace_when_tokenize_then_returns_punctuation_token(self):
        """
        Given: A string with only whitespace
        When: tokenize_word is called
        Then: Returns PSEUDO_PUNCTUATION token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_PUNCTUATION

        result = tokenize_word("   ")
        assert result == PSEUDO_PUNCTUATION


class TestTokenizerPunctuation:
    """Tests for tokenizing punctuation (Option A implementation)."""

    def test_given_pure_punctuation_when_tokenize_then_returns_punctuation_token(self):
        """
        Given: A string that is only punctuation
        When: tokenize_word is called
        Then: Returns PSEUDO_PUNCTUATION token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_PUNCTUATION

        assert tokenize_word(".") == PSEUDO_PUNCTUATION
        assert tokenize_word(",") == PSEUDO_PUNCTUATION
        assert tokenize_word("!") == PSEUDO_PUNCTUATION
        assert tokenize_word("?") == PSEUDO_PUNCTUATION
        assert tokenize_word(":") == PSEUDO_PUNCTUATION
        assert tokenize_word(";") == PSEUDO_PUNCTUATION

    def test_given_word_with_punctuation_when_tokenize_then_returns_unknown_token(self):
        """
        Given: A word with punctuation (Option A)
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN token

        This is the design decision: "love," -> PSEUDO_UNKNOWN (single token)
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN

        # Words with trailing punctuation
        assert tokenize_word("love,") == PSEUDO_UNKNOWN
        assert tokenize_word("I.") == PSEUDO_UNKNOWN
        assert tokenize_word("computers!") == PSEUDO_UNKNOWN

        # Words with leading punctuation
        assert tokenize_word("'hello") == PSEUDO_UNKNOWN

        # Words with punctuation in middle
        assert tokenize_word("hello-world") == PSEUDO_UNKNOWN

    def test_given_word_with_mixed_punctuation_when_tokenize_then_returns_unknown_token(self):
        """
        Given: A word with multiple punctuation characters
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN token
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN

        assert tokenize_word("hello,world") == PSEUDO_UNKNOWN
        assert tokenize_word("test...") == PSEUDO_UNKNOWN
