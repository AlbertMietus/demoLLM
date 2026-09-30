#!/usr/bin/env python3

"""
CLI: Validate tokens with punctuation allowed (CLI3b).

This script reads all input from stdin, converts words to tokens,
and validates that all tokens are either in the base vocabulary or
PSEUDO_PUNCTUATION.

Exit codes:
- 0 (True): All tokens are valid (base tokens or PUNCTUATION)
- 1 (False): At least one token is UNKNOWN
"""

import sys

from demo_llm.tokens import BASE_TOKENS, PSEUDO_PUNCTUATION
from demo_llm.compute import tokenize_word


def main() -> None:
    """Main entry point for the CLI."""
    # Valid tokens include base tokens plus PSEUDO_PUNCTUATION
    valid_tokens = BASE_TOKENS | {PSEUDO_PUNCTUATION}

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
