/* (C) Albert Mietus -- mostly made by codeAI=mistral-medium-3-5 */

"""
Test suite for the LLM model class (test-001 series).

These tests define the requirements for the LLM model using pseudo-BDD style:
- given: the initial state/conditions
- when: the action performed
- then: the expected outcome

All tests follow the naming convention: test_<series>_<description>
"""

import pytest
from typing import Dict, List


class TestLLMModelStructure:
    """Tests for the basic structure of the LLM model."""

    def test_001_given_llm_class_when_instantiated_then_has_token_mappings(self):
        """
        Given: The LLM class is available
        When: An instance is created with token_to_id and id_to_token
        Then: The instance has both token_to_id and id_to_token attributes
        """
        from demo_llm.model import LLM
        
        token_to_id = {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
        id_to_token = {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
        weights = [[0] * 5 for _ in range(5)]
        
        llm = LLM(token_to_id=token_to_id, id_to_token=id_to_token, weights=weights)
        
        assert hasattr(llm, 'token_to_id')
        assert hasattr(llm, 'id_to_token')
        assert hasattr(llm, 'weights')

    def test_002_given_llm_instance_when_inspected_then_token_mappings_are_correct(self):
        """
        Given: An LLM instance with specific token mappings
        When: The mappings are inspected
        Then: The mappings match the provided values
        """
        from demo_llm.model import LLM
        
        token_to_id = {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
        id_to_token = {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
        weights = [[0] * 5 for _ in range(5)]
        
        llm = LLM(token_to_id=token_to_id, id_to_token=id_to_token, weights=weights)
        
        assert llm.token_to_id == token_to_id
        assert llm.id_to_token == id_to_token

    def test_003_given_llm_instance_when_inspected_then_weights_are_correct(self):
        """
        Given: An LLM instance with specific weights
        When: The weights are inspected
        Then: The weights match the provided matrix
        """
        from demo_llm.model import LLM
        
        token_to_id = {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
        id_to_token = {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
        weights = [
            [0, 0, 0, 0, 100],  # EOS
            [0, 0, 0, 100, 0],  # I
            [0, 0, 0, 100, 0],  # YOU
            [0, 0, 0, 0, 100],  # LOVE
            [0, 0, 0, 0, 0]     # COMPUTERS
        ]
        
        llm = LLM(token_to_id=token_to_id, id_to_token=id_to_token, weights=weights)
        
        assert llm.weights == weights


class TestLLMModelValidation:
    """Tests for validation of the LLM model."""

    def test_004_given_token_mappings_when_checked_then_are_bidirectional(self):
        """
        Given: Token mappings in an LLM instance
        When: The mappings are validated
        Then: Each token has a corresponding ID and vice versa
        """
        from demo_llm.model import LLM
        
        token_to_id = {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
        id_to_token = {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
        weights = [[0] * 5 for _ in range(5)]
        
        llm = LLM(token_to_id=token_to_id, id_to_token=id_to_token, weights=weights)
        
        # Check all tokens have an ID
        for token, token_id in llm.token_to_id.items():
            assert llm.id_to_token[token_id] == token
        
        # Check all IDs have a token
        for token_id, token in llm.id_to_token.items():
            assert llm.token_to_id[token] == token_id

    def test_005_given_weights_when_checked_then_matrix_is_square(self):
        """
        Given: Weights matrix in an LLM instance
        When: The matrix dimensions are checked
        Then: The matrix is square (n x n where n = number of tokens)
        """
        from demo_llm.model import LLM
        
        token_to_id = {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
        id_to_token = {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
        weights = [[0] * 5 for _ in range(5)]
        
        llm = LLM(token_to_id=token_to_id, id_to_token=id_to_token, weights=weights)
        
        num_tokens = len(llm.token_to_id)
        assert len(llm.weights) == num_tokens
        for row in llm.weights:
            assert len(row) == num_tokens

    def test_006_given_weights_when_checked_then_values_are_percentages(self):
        """
        Given: Weights matrix in an LLM instance
        When: The weight values are checked
        Then: All values are integers between 0 and 100 (inclusive)
        """
        from demo_llm.model import LLM
        
        token_to_id = {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
        id_to_token = {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
        weights = [
            [0, 0, 0, 0, 100],
            [0, 0, 0, 100, 0],
            [0, 0, 0, 100, 0],
            [0, 0, 0, 0, 100],
            [0, 0, 0, 0, 0]
        ]
        
        llm = LLM(token_to_id=token_to_id, id_to_token=id_to_token, weights=weights)
        
        for row in llm.weights:
            for value in row:
                assert isinstance(value, int)
                assert 0 <= value <= 100


class TestDemoLLMFactory:
    """Tests for the create_demo_llm factory function."""

    def test_007_given_demo_llm_factory_when_called_then_returns_llm_instance(self):
        """
        Given: The create_demo_llm factory function
        When: It is called
        Then: It returns an LLM instance
        """
        from demo_llm.model import create_demo_llm, LLM
        
        llm = create_demo_llm()
        
        assert isinstance(llm, LLM)

    def test_008_given_demo_llm_when_inspected_then_has_5_tokens(self):
        """
        Given: The demo LLM created by the factory
        When: The tokens are inspected
        Then: It has exactly 5 tokens: I, YOU, LOVE, COMPUTERS, EOS
        """
        from demo_llm.model import create_demo_llm
        
        llm = create_demo_llm()
        
        expected_tokens = {"I", "YOU", "LOVE", "COMPUTERS", "EOS"}
        assert set(llm.token_to_id.keys()) == expected_tokens
        assert set(llm.id_to_token.values()) == expected_tokens

    def test_009_given_demo_llm_when_inspected_then_has_correct_token_ids(self):
        """
        Given: The demo LLM created by the factory
        When: The token IDs are inspected
        Then: The tokens have IDs 0 (EOS), 1 (I), 2 (YOU), 3 (LOVE), 4 (COMPUTERS)
        """
        from demo_llm.model import create_demo_llm
        
        llm = create_demo_llm()
        
        assert llm.token_to_id["EOS"] == 0
        assert llm.token_to_id["I"] == 1
        assert llm.token_to_id["YOU"] == 2
        assert llm.token_to_id["LOVE"] == 3
        assert llm.token_to_id["COMPUTERS"] == 4

    def test_010_given_demo_llm_when_inspected_then_weights_are_5x5(self):
        """
        Given: The demo LLM created by the factory
        When: The weights matrix is inspected
        Then: The weights are a 5x5 matrix
        """
        from demo_llm.model import create_demo_llm
        
        llm = create_demo_llm()
        
        assert len(llm.weights) == 5
        for row in llm.weights:
            assert len(row) == 5

    def test_011_given_demo_llm_when_inspected_then_valid_sentences_possible(self):
        """
        Given: The demo LLM created by the factory
        When: The weights are inspected for valid sentences
        Then: The weights allow for "I love computers", "You love computers", and "I love you"
        """
        from demo_llm.model import create_demo_llm
        
        llm = create_demo_llm()
        
        # Token IDs
        eos_id = llm.token_to_id["EOS"]
        i_id = llm.token_to_id["I"]
        you_id = llm.token_to_id["YOU"]
        love_id = llm.token_to_id["LOVE"]
        computers_id = llm.token_to_id["COMPUTERS"]
        
        # Check I -> LOVE has high probability
        assert llm.weights[i_id][love_id] > 0
        
        # Check YOU -> LOVE has high probability
        assert llm.weights[you_id][love_id] > 0
        
        # Check LOVE -> COMPUTERS has high probability
        assert llm.weights[love_id][computers_id] > 0
        
        # Check LOVE -> YOU has some probability (for "I love you")
        assert llm.weights[love_id][you_id] > 0
        
        # Check COMPUTERS -> EOS has high probability (end of sentence)
        assert llm.weights[computers_id][eos_id] > 0
        
        # Check YOU -> EOS has some probability (end of sentence)
        assert llm.weights[you_id][eos_id] > 0

    def test_012_given_demo_llm_when_inspected_then_row_sums_are_reasonable(self):
        """
        Given: The demo LLM created by the factory
        When: The weights matrix row sums are checked
        Then: Each row sums to <= 100 (probabilities don't exceed 100%)
        """
        from demo_llm.model import create_demo_llm
        
        llm = create_demo_llm()
        
        for row in llm.weights:
            row_sum = sum(row)
            assert row_sum <= 100, f"Row sum {row_sum} exceeds 100%"
