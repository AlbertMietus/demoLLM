"""
LLM Model Module for DemoLLM.

This module contains the core LLM model class and factory function.
The LLM class is a simple dataclass that stores the model's weights and token mappings.

.. note::
    This is a minimalistic implementation for demonstration purposes only.

Classes
-------
LLM
    A dataclass representing a minimal LLM model with token mappings and weights.

Functions
---------
create_demo_llm
    Factory function to create a pre-configured LLM with 5 tokens and hardcoded weights.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class LLM:
    """
    A minimalistic LLM model for demonstration purposes.
    
    This class stores the essential components of an LLM:
    - Token to ID mapping
    - ID to token mapping
    - Weights matrix representing transition probabilities between tokens
    
    Attributes
    ----------
    token_to_id : Dict[str, int]
        Mapping from token strings to their integer IDs.
        Example: {"I": 1, "YOU": 2, "LOVE": 3, "COMPUTERS": 4, "EOS": 0}
    
    id_to_token : Dict[int, str]
        Mapping from integer IDs to token strings.
        Example: {0: "EOS", 1: "I", 2: "YOU", 3: "LOVE", 4: "COMPUTERS"}
    
    weights : List[List[int]]
        A square matrix (n x n where n = number of tokens) where weights[i][j]
        represents the probability (0-100) that token j follows token i.
        
    Notes
    -----
    This is a simplified model that uses hardcoded weights to demonstrate
    the basic structure of an LLM. In a real implementation, these weights
    would be learned during training.
    
    The weights matrix represents a first-order Markov chain where the
    probability of the next token depends only on the current token.
    
    Examples
    --------
    >>> from demo_llm.model import create_demo_llm
    >>> llm = create_demo_llm()
    >>> llm.token_to_id["I"]
    1
    >>> llm.weights[1][3]  # Probability of LOVE (3) following I (1)
    100
    """
    
    token_to_id: Dict[str, int]
    id_to_token: Dict[int, str]
    weights: List[List[int]]


def create_demo_llm() -> LLM:
    """
    Create a pre-configured demo LLM with 5 tokens and hardcoded weights.
    
    The demo LLM supports the following tokens:
    - EOS (End Of Sentence) - ID 0
    - I - ID 1
    - YOU - ID 2
    - LOVE - ID 3
    - COMPUTERS - ID 4
    
    The weights are configured to allow the following valid sentences:
    - "I love computers"
    - "You love computers"
    - "I love you"
    
    Returns
    -------
    LLM
        An LLM instance with the demo configuration.
    
    Notes
    -----
    The weights matrix is designed such that:
    - "I" (1) is most likely followed by "love" (3)
    - "YOU" (2) is most likely followed by "love" (3)
    - "LOVE" (3) can be followed by "computers" (4) or "you" (2)
    - "COMPUTERS" (4) is followed by EOS (0)
    - "YOU" (2) can also be followed by EOS (0) to end a sentence
    
    This creates a simple but functional demo that can generate the target sentences.
    
    Examples
    --------
    >>> from demo_llm.model import create_demo_llm
    >>> llm = create_demo_llm()
    >>> len(llm.token_to_id)
    5
    >>> llm.weights[1][3]  # I -> LOVE
    100
    >>> llm.weights[3][4]  # LOVE -> COMPUTERS
    70
    >>> llm.weights[3][2]  # LOVE -> YOU
    30
    """
    
    # Define token mappings
    token_to_id: Dict[str, int] = {
        "EOS": 0,
        "I": 1,
        "YOU": 2,
        "LOVE": 3,
        "COMPUTERS": 4
    }
    
    id_to_token: Dict[int, str] = {
        0: "EOS",
        1: "I",
        2: "YOU",
        3: "LOVE",
        4: "COMPUTERS"
    }
    
    # Define weights matrix (5x5)
    # Rows: current token, Columns: next token
    # EOS (0), I (1), YOU (2), LOVE (3), COMPUTERS (4)
    weights: List[List[int]] = [
        # EOS row: once we hit EOS, we stay at EOS
        [100, 0, 0, 0, 0],
        
        # I row: I is always followed by LOVE (100%)
        [0, 0, 0, 100, 0],
        
        # YOU row: YOU can be followed by LOVE (70%) or EOS (30%)
        [30, 0, 0, 70, 0],
        
        # LOVE row: LOVE is followed by COMPUTERS (70%) or YOU (30%)
        [0, 0, 30, 0, 70],
        
        # COMPUTERS row: COMPUTERS is always followed by EOS (100%)
        [100, 0, 0, 0, 0]
    ]
    
    return LLM(
        token_to_id=token_to_id,
        id_to_token=id_to_token,
        weights=weights
    )
