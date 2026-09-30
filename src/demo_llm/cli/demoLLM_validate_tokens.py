#!/usr/bin/env python3

"""
CLI: Validate that all input tokens are valid.

This script reads all input from stdin, converts words to tokens,
and validates that all tokens are in the base vocabulary (EOS, I, YOU,
LOVE, COMPUTERS).

Exit codes:
- 0 (True): All tokens are valid
- 1 (False): At least one token is invalid (UNKNOWN or PUNCTUATION)
"""

import sys

from demo_llm.tokens import BASE_TOKENS
from demo_llm.compute import tokenize_word


def main():
    """Main entry point for the CLI."""
    valid_tokens = BASE_TOKENS
    
    # Read all input
    for line in sys.stdin:
        words = line.split()
        for word in words:
            token = tokenize_word(word)
            
            # Check if token is valid
            if token not in valid_tokens:
                sys.exit(1)
    
    # All tokens were valid
    sys.exit(0)


if __name__ == "__main__":
    main()
