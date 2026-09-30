#!/usr/bin/env python3
"""
CLI: Validate that all input tokens are valid.

STUB: Implementation will follow BDD-TDD workflow.
This script will read all input from stdin and validate that all tokens
are in the base vocabulary (EOS, I, YOU, LOVE, COMPUTERS).

Exit codes:
- 0 (True): All tokens are valid
- 1 (False): At least one token is invalid
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
