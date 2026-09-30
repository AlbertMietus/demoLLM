# (C) Albert Mietus -- mostly made by codeAI=mistral-medium-3-5 

"""DemoLLM: A minimalistic LLM implementation for demonstration purposes.

This package contains a simplified LLM model to demonstrate how modern
 generative AI systems work. The implementation is intentionally small
 and uses hardcoded weights for a handful of tokens.

.. note::
    This is a demo-only implementation. It is not meant for production use.
"""

from demo_llm.model import LLM, create_demo_llm

__all__ = ["LLM", "create_demo_llm"]
