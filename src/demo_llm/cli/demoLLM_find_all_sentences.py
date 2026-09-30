#!/usr/bin/env python3

"""
CLI: Find and print all valid sentences from input.

This script reads input word by word from stdin, converts words to tokens,
and detects all valid sentences based on the LLM model. Each valid sentence
is printed immediately when found. At the end, a summary of all detected
sentences and their counts is printed.
"""

import sys
from collections import Counter

from demo_llm.model import create_demo_llm
from demo_llm.compute import LLMCompute, tokenize_word
from demo_llm.tokens import STOP


def main() -> None:
    """Main entry point for the CLI."""
    llm = create_demo_llm()
    compute = LLMCompute(llm)

    sentence_counter: Counter[str] = Counter()

    # Read from stdin word by word
    for line in sys.stdin:
        words = line.split()
        for word in words:
            # Check for STOP word
            token = tokenize_word(word)
            if token == STOP:
                break

            compute.feed_token(word)

            # Check if we have a result
            result = compute.get_last_result_as_sentence()
            if result is not None:
                print(result)
                sentence_counter[result] += 1

        # Check for STOP in the line
        if any(tokenize_word(w.strip()) == STOP for w in line.split()):
            break

    # Print summary
    if sentence_counter:
        print()
        for sentence, count in sorted(sentence_counter.items()):
            print(f"{sentence}: {count}")

    sys.exit(0)


if __name__ == "__main__":
    main()
