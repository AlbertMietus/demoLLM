#!/usr/bin/env python3

"""
CLI: Find and print the first valid sentence from input.

This script reads input word by word from stdin, converts words to tokens,
and detects the first complete valid sentence based on the LLM model.
Once a valid sentence is found, it is printed and the program exits.
"""

import sys

from demo_llm.model import create_demo_llm
from demo_llm.compute import LLMCompute, tokenize_word


def main() -> None:
    """Main entry point for the CLI."""
    llm = create_demo_llm()
    compute = LLMCompute(llm)

    # Read from stdin word by word
    for line in sys.stdin:
        words = line.split()
        for word in words:
            compute.feed_token(word)

            # Check if we have a result
            result = compute.get_last_result_as_sentence()
            if result is not None:
                print(result)
                sys.exit(0)

    # No valid sentence found
    sys.exit(0)


if __name__ == "__main__":
    main()
