
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
    
    Implementation follows Option A: words with punctuation are PSEUDO_UNKNOWN.
    
    TODO: Confirm design decision with Albert.
    Current implementation:
    - Pure punctuation -> PSEUDO_PUNCTUATION
    - Words with punctuation -> PSEUDO_UNKNOWN
    - Known words -> Token ID
    - Unknown words -> PSEUDO_UNKNOWN
    
    See: tests/test_003_tokenizer.py for design decision documentation.
    """
    # If word is empty or all whitespace
    if not word or all(c.isspace() for c in word):
        return PSEUDO_PUNCTUATION
    
    # Check if word contains any punctuation
    PUNCTUATION_CHARS = ".,;:!?()[]{}'\""
    if any(c in PUNCTUATION_CHARS for c in word):
        # If entire word IS punctuation
        if all(c in PUNCTUATION_CHARS or c.isspace() for c in word):
            return PSEUDO_PUNCTUATION
        # Word with punctuation -> invalid
        return PSEUDO_UNKNOWN
    
    # Convert to uppercase for case-insensitive matching
    upper_word = word.upper()
    
    # Check if it's a known word
    if upper_word in WORD_TO_TOKEN:
        return WORD_TO_TOKEN[upper_word]
    
    # Unknown word
    return PSEUDO_UNKNOWN
