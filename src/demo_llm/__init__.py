"""
DemoLLM: A minimalistic LLM implementation for demonstration purposes.

This package contains a simplified LLM model to demonstrate how modern
generative AI systems work. The implementation is intentionally small
and uses hardcoded weights for a handful of tokens.

.. note::
    This is a demo-only implementation. It is not meant for production use.
"""

from demo_llm.model import LLM, create_demo_llm
from demo_llm.tokens import Token, EOS, I, YOU, LOVE, COMPUTERS, PSEUDO_UNKNOWN, PSEUDO_PUNCTUATION, STOP
from demo_llm.compute import LLMCompute, tokenize_word

__all__ = ["LLM", "create_demo_llm", "Token", "EOS", "I", "YOU", "LOVE", "COMPUTERS", "PSEUDO_UNKNOWN", "PSEUDO_PUNCTUATION", "STOP", "LLMCompute", "tokenize_word"]
