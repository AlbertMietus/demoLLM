"""
TDD tests for the LLM compute class (test-002 series).

These tests define the requirements for the LLMCompute class.
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

    def test_given_llm_when_compute_created_then_has_empty_buffer(self):
        """
        Given: An LLM instance
        When: LLMCompute is created with that LLM
        Then: The compute instance has an empty buffer
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        assert compute.buffer == []

    def test_given_llm_when_compute_created_then_has_no_result(self):
        """
        Given: An LLM instance
        When: LLMCompute is created with that LLM
        Then: The compute instance has no last result
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        assert compute.last_result is None


class TestLLMComputeFeedToken:
    """Tests for feeding tokens to LLMCompute."""

    def test_given_empty_buffer_when_feed_valid_token_then_adds_to_buffer(self):
        """
        Given: An LLMCompute instance with empty buffer
        When: A valid token is fed
        Then: The token is added to the buffer
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)

        assert I in compute.buffer

    def test_given_buffer_with_token_when_feed_unknown_then_buffer_reset(self):
        """
        Given: An LLMCompute instance with tokens in buffer
        When: An UNKNOWN token is fed
        Then: The buffer is reset
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, PSEUDO_UNKNOWN

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        assert len(compute.buffer) > 0

        compute.feed_token(PSEUDO_UNKNOWN)

        assert compute.buffer == []

    def test_given_buffer_with_token_when_feed_punctuation_then_buffer_reset(self):
        """
        Given: An LLMCompute instance with tokens in buffer
        When: A PUNCTUATION token is fed
        Then: The buffer is reset
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, PSEUDO_PUNCTUATION

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        assert len(compute.buffer) > 0

        compute.feed_token(PSEUDO_PUNCTUATION)

        assert compute.buffer == []

    def test_given_buffer_when_feed_stop_then_buffer_reset(self):
        """
        Given: An LLMCompute instance with tokens in buffer
        When: A STOP token is fed
        Then: The buffer is reset
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, STOP

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        assert len(compute.buffer) > 0

        compute.feed_token(STOP)

        assert compute.buffer == []


class TestLLMComputeSentenceDetection:
    """Tests for sentence detection in LLMCompute."""

    def test_given_i_love_you_when_feed_then_detects_sentence(self):
        """
        Given: Tokens I, LOVE, YOU in sequence
        When: Fed to LLMCompute
        Then: A sentence is detected (I LOVE YOU)
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, YOU

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(YOU)

        result = compute.get_last_result()
        assert result is not None
        assert len(result) >= 2

    def test_given_i_love_computers_when_feed_then_detects_sentence(self):
        """
        Given: Tokens I, LOVE, COMPUTERS in sequence
        When: Fed to LLMCompute
        Then: A sentence is detected (I LOVE COMPUTERS)
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, COMPUTERS

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(COMPUTERS)

        result = compute.get_last_result()
        assert result is not None
        assert len(result) >= 2

    def test_given_single_token_when_feed_then_no_sentence(self):
        """
        Given: A single token
        When: Fed to LLMCompute
        Then: No sentence is detected (need at least 2 tokens)
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)

        result = compute.get_last_result()
        assert result is None

    def test_given_invalid_transition_when_feed_then_no_sentence(self):
        """
        Given: Tokens with invalid transitions
        When: Fed to LLMCompute
        Then: No sentence is detected
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, COMPUTERS

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(COMPUTERS)

        result = compute.get_last_result()
        assert result is None


class TestLLMComputeGetResult:
    """Tests for getting results from LLMCompute."""

    def test_given_sentence_detected_when_get_last_result_then_returns_tokens(self):
        """
        Given: A sentence has been detected
        When: get_last_result is called
        Then: The sentence tokens are returned
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, YOU

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(YOU)

        result = compute.get_last_result()
        assert result is not None
        assert isinstance(result, list)
        assert all(isinstance(t, int) for t in result)

    def test_given_sentence_detected_when_get_last_result_as_sentence_then_returns_string(self):
        """
        Given: A sentence has been detected
        When: get_last_result_as_sentence is called
        Then: The sentence as a string is returned
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, YOU

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(YOU)

        result = compute.get_last_result_as_sentence()
        assert result is not None
        assert isinstance(result, str)
        assert " " in result  # Multiple words

    def test_given_no_sentence_when_get_last_result_then_returns_none(self):
        """
        Given: No sentence has been detected
        When: get_last_result is called
        Then: None is returned
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        result = compute.get_last_result()
        assert result is None

    def test_given_no_sentence_when_get_last_result_as_sentence_then_returns_none(self):
        """
        Given: No sentence has been detected
        When: get_last_result_as_sentence is called
        Then: None is returned
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        result = compute.get_last_result_as_sentence()
        assert result is None


class TestLLMComputeReset:
    """Tests for resetting LLMCompute."""

    def test_given_buffer_with_tokens_when_reset_then_buffer_empty(self):
        """
        Given: An LLMCompute instance with tokens in buffer
        When: reset is called
        Then: The buffer is empty
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(LOVE)
        assert len(compute.buffer) > 0

        compute.reset()

        assert compute.buffer == []

    def test_given_last_result_set_when_reset_then_result_none(self):
        """
        Given: An LLMCompute instance with a last result
        When: reset is called
        Then: The last result is None
        """
        from demo_llm.model import create_demo_llm
        from demo_llm.compute import LLMCompute
        from demo_llm.tokens import I, LOVE, YOU

        llm = create_demo_llm()
        compute = LLMCompute(llm)

        compute.feed_token(I)
        compute.feed_token(LOVE)
        compute.feed_token(YOU)
        assert compute.get_last_result() is not None

        compute.reset()

        assert compute.get_last_result() is None
