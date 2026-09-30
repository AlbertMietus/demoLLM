
"""
LLM Compute Module for DemoLLM.

This module will contain the core computation class that processes tokens
through the LLM model to detect valid sentences and perform validation.

STUB: Implementation will follow BDD-TDD workflow.
"""

from typing import Optional

from demo_llm.tokens import (
    Token,
    EOS,
    PSEUDO_UNKNOWN,
    PSEUDO_PUNCTUATION,
    STOP,
    WORD_TO_TOKEN,
)


def tokenize_word(word: str) -> Token:
    """
    Convert a word to its corresponding token ID.
    
    STUB: Implementation will follow TDD workflow.
    
    TODO: Design decision needed for words with punctuation.
    See: tests/test_003_tokenizer.py
    
    Current assumption (Option A):
    - Words with punctuation -> PSEUDO_UNKNOWN
    - Pure punctuation -> PSEUDO_PUNCTUATION
    - Known words -> Token ID
    - Unknown words -> PSEUDO_UNKNOWN
    """
    # TODO: Implement properly
    # For now, return PSEUDO_UNKNOWN for everything
    return PSEUDO_UNKNOWN
