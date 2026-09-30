
"""
TDD tests for the tokenizer function (test-003 series).

These tests define the requirements for the tokenize_word function.
All tests currently fail as the tokenizer is not yet implemented.

TODO: Design decision needed - see test_tokenize_word_with_punctuation
"""

import pytest


class TestTokenizerKnownWords:
    """Tests for tokenizing known words."""

    def test_given_word_i_when_tokenize_then_returns_i_token(self):
        """
        Given: Word "I"
        When: tokenize_word is called
        Then: Returns I token (1)
        """
        from demo_llm.tokens import I
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("I")
        
        assert result == I

    def test_given_word_you_when_tokenize_then_returns_you_token(self):
        """
        Given: Word "You"
        When: tokenize_word is called
        Then: Returns YOU token (2)
        """
        from demo_llm.tokens import YOU
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("You")
        
        assert result == YOU

    def test_given_word_love_when_tokenize_then_returns_love_token(self):
        """
        Given: Word "love"
        When: tokenize_word is called
        Then: Returns LOVE token (3)
        """
        from demo_llm.tokens import LOVE
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("love")
        
        assert result == LOVE

    def test_given_word_computers_when_tokenize_then_returns_computers_token(self):
        """
        Given: Word "computers"
        When: tokenize_word is called
        Then: Returns COMPUTERS token (4)
        """
        from demo_llm.tokens import COMPUTERS
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("computers")
        
        assert result == COMPUTERS


class TestTokenizerCaseInsensitive:
    """Tests for case-insensitive tokenization."""

    def test_given_lowercase_i_when_tokenize_then_returns_i_token(self):
        """
        Given: Word "i"
        When: tokenize_word is called
        Then: Returns I token (1)
        """
        from demo_llm.tokens import I
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("i")
        
        assert result == I

    def test_given_mixed_case_you_when_tokenize_then_returns_you_token(self):
        """
        Given: Word "yOu"
        When: tokenize_word is called
        Then: Returns YOU token (2)
        """
        from demo_llm.tokens import YOU
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("yOu")
        
        assert result == YOU


class TestTokenizerUnknownWords:
    """Tests for tokenizing unknown words."""

    def test_given_unknown_word_hello_when_tokenize_then_returns_unknown(self):
        """
        Given: Word "hello"
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN token (5)
        """
        from demo_llm.tokens import PSEUDO_UNKNOWN
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("hello")
        
        assert result == PSEUDO_UNKNOWN


class TestTokenizerPunctuation:
    """Tests for tokenizing punctuation."""

    def test_given_comma_when_tokenize_then_returns_punctuation(self):
        """
        Given: Word ","
        When: tokenize_word is called
        Then: Returns PSEUDO_PUNCTUATION token (6)
        """
        from demo_llm.tokens import PSEUDO_PUNCTUATION
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word(",")
        
        assert result == PSEUDO_PUNCTUATION

    def test_given_period_when_tokenize_then_returns_punctuation(self):
        """
        Given: Word "."
        When: tokenize_word is called
        Then: Returns PSEUDO_PUNCTUATION token (6)
        """
        from demo_llm.tokens import PSEUDO_PUNCTUATION
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word(".")
        
        assert result == PSEUDO_PUNCTUATION


class TestTokenizerWordsWithPunctuation:
    """Tests for words with punctuation attached.
    
    TODO: DESIGN DECISION NEEDED
    
    Currently assuming Option A: words with punctuation = PSEUDO_UNKNOWN
    Alternative: Option B: split into multiple tokens
    
    See: docs/prj/workflow/bug_handling.rst
    See: docs/AIblog/love_comma_example.rst
    """

    def test_given_word_with_trailing_comma_when_tokenize_then_returns_unknown(self):
        """
        Given: Word "love,"
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN token (5)
        
        DESIGN DECISION (Option A):
        - "love," = 1 token (PSEUDO_UNKNOWN)
        - Alternative (Option B): "love," = 2 tokens (LOVE + PSEUDO_PUNCTUATION)
        
        TODO: Confirm with Albert which option to use.
        Current implementation: Option A.
        """
        from demo_llm.tokens import PSEUDO_UNKNOWN
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word("love,")
        
        assert result == PSEUDO_UNKNOWN

    def test_given_word_with_leading_comma_when_tokenize_then_returns_unknown(self):
        """
        Given: Word ",love"
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN token (5)
        """
        from demo_llm.tokens import PSEUDO_UNKNOWN
        from demo_llm.compute import tokenize_word
        
        result = tokenize_word(",love")
        
        assert result == PSEUDO_UNKNOWN
