
"""
TDD tests for the LLM compute class (test-002 series).

These tests define the requirements for the LLMCompute class.
All tests currently fail as the compute module is not yet fully implemented.
"""

import pytest


class TestLLMComputeInitialization:
    """Tests for LLMCompute class initialization."""

    def test_given_llm_when_compute_created_then_has_llm(self):
        """
        Given: An LLM instance
        When: LLMCompute is created with that LLM
        Then: The compute instance has the LLM
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        assert compute.llm is llm

    def test_given_llm_when_compute_created_then_buffer_is_empty(self):
        """
        Given: An LLM instance
        When: LLMCompute is created
        Then: The buffer is empty
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        assert compute.buffer == []

    def test_given_llm_when_compute_created_then_last_result_is_none(self):
        """
        Given: An LLM instance
        When: LLMCompute is created
        Then: last_result is None
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        assert compute.last_result is None


class TestLLMComputeFeedToken:
    """Tests for feeding tokens to LLMCompute."""

    def test_given_token_when_feed_then_adds_to_buffer(self):
        """
        Given: LLMCompute with empty buffer
        When: A valid token is fed
        Then: The token is added to the buffer
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        
        assert compute.buffer == [I]

    def test_given_word_when_feed_then_tokenizes_and_adds(self):
        """
        Given: LLMCompute with empty buffer
        When: A word string is fed
        Then: The word is tokenized and added to buffer
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token("I")
        
        assert compute.buffer == [I]

    def test_given_lowercase_word_when_feed_then_converts_to_uppercase(self):
        """
        Given: LLMCompute with empty buffer
        When: A lowercase word is fed
        Then: It is converted to uppercase token
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token("i")
        
        assert compute.buffer == [I]


class TestLLMComputeUnknownTokens:
    """Tests for handling unknown and punctuation tokens."""

    def test_given_unknown_word_when_feed_then_buffer_reset(self):
        """
        Given: LLMCompute with tokens in buffer
        When: An unknown word is fed
        Then: The buffer is reset to empty
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        compute.feed_token("hello")  # unknown word
        
        assert compute.buffer == []

    def test_given_punctuation_when_feed_then_buffer_reset(self):
        """
        Given: LLMCompute with tokens in buffer
        When: Punctuation is fed
        Then: The buffer is reset to empty
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        compute.feed_token(",")  # punctuation
        
        assert compute.buffer == []

    def test_given_stop_token_when_feed_then_buffer_reset(self):
        """
        Given: LLMCompute with tokens in buffer
        When: STOP token is fed
        Then: The buffer is reset to empty
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, STOP
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        compute.feed_token(STOP)
        
        assert compute.buffer == []


class TestLLMComputeSentenceDetection:
    """Tests for sentence detection in LLMCompute."""

    def test_given_i_love_computers_when_feed_then_detects_sentence(self):
        """
        Given: LLMCompute with empty buffer
        When: Tokens "I", "love", "computers" are fed
        Then: A sentence is detected and stored in last_result
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, COMPUTERS
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(COMPUTERS)
        
        assert compute.last_result == [I, LOVE, COMPUTERS]

    def test_given_you_love_computers_when_feed_then_detects_sentence(self):
        """
        Given: LLMCompute with empty buffer
        When: Tokens "YOU", "LOVE", "COMPUTERS" are fed
        Then: A sentence is detected
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import YOU, LOVE, COMPUTERS
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(YOU)
        compute.feed_token(LOVE)
        compute.feed_token(COMPUTERS)
        
        assert compute.last_result == [YOU, LOVE, COMPUTERS]

    def test_given_i_love_you_when_feed_then_detects_sentence(self):
        """
        Given: LLMCompute with empty buffer
        When: Tokens "I", "LOVE", "YOU" are fed
        Then: A sentence is detected
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, YOU
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(YOU)
        
        assert compute.last_result == [I, LOVE, YOU]

    def test_given_partial_sentence_when_feed_then_no_detection(self):
        """
        Given: LLMCompute with empty buffer
        When: Partial sentence "I love" is fed
        Then: No sentence is detected (not complete)
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE
        
        llm = create_demo_llm()
        compute = LLMCompute(llm)
        
        compute.feed_token(I)
        compute.feed_token(LOVE)
        
        assert compute.last_result is None
