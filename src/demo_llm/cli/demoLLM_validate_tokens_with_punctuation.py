#!/usr/bin/env python3
"""
CLI: Validate tokens with punctuation allowed (CLI3b).

STUB: Implementation will follow BDD-TDD workflow.
This script will read all input from stdin and validate that all tokens
are either in the base vocabulary or PSEUDO_PUNCTUATION.

Exit codes:
- 0 (True): All tokens are valid (base tokens or PUNCTUATION)
- 1 (False): At least one token is UNKNOWN
"""

import sys


def main():
    """Main entry point for the CLI."""
    # TODO: Implement using tokenize_word function
    # For now, just read input and exit with 0
    for line in sys.stdin:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
