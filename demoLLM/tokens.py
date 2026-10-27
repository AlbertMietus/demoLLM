"""
Token definitions for DemoLLM.

This module defines all token constants used throughout the DemoLLM package.
Tokens are represented as integers (Token type alias) for internal processing,
but exposed as named constants for readability.

Type Aliases
-----------
Token
    An integer representing a token ID. All tokens in DemoLLM are integers.

Constants
---------
EOS
    End Of Sentence token (ID 0). Marks the end of a valid sentence.
I
    Token for the word "I" (ID 1).
YOU
    Token for the word "you" / "You" (ID 2).
LOVE
    Token for the word "love" (ID 3).
COMPUTERS
    Token for the word "computers" (ID 4).
PSEUDO_UNKNOWN
    Pseudo-token for unknown words (ID 5). Used when input contains words
    not in the vocabulary.
PSEUDO_PUNCTUATION
    Pseudo-token for punctuation marks (ID 6). Used when input contains
    punctuation characters.
STOP
    Token to signal end of input stream (ID 7). Used as a control token.

Notes
-----
All token constants are uppercase to match the convention of the existing
model weights. The tokenizer should convert input to uppercase before
mapping to these token IDs.

The token IDs are carefully chosen to allow for easy extension:
- 0-4: Core tokens (EOS, I, YOU, LOVE, COMPUTERS)
- 5-6: Pseudo-tokens (UNKNOWN, PUNCTUATION)
- 7: Control token (STOP)
- 8+: Available for future expansion
"""

# Token type: all tokens are integers
Token = int

# Core tokens (the 4 basis words + EOS)
EOS: Token = 0
I: Token = 1
YOU: Token = 2
LOVE: Token = 3
COMPUTERS: Token = 4

# Pseudo-tokens for special cases
PSEUDO_UNKNOWN: Token = 5
PSEUDO_PUNCTUATION: Token = 6

# Control token
STOP: Token = 7

# All valid tokens in the base vocabulary (excluding pseudo-tokens)
BASE_TOKENS: set[Token] = {EOS, I, YOU, LOVE, COMPUTERS}

# All tokens including pseudo-tokens
ALL_TOKENS: set[Token] = {EOS, I, YOU, LOVE, COMPUTERS, PSEUDO_UNKNOWN, PSEUDO_PUNCTUATION, STOP}

# Mapping from word strings to token IDs (for tokenizer)
# Words are stored in uppercase for case-insensitive matching
WORD_TO_TOKEN: dict[str, Token] = {
    "EOS": EOS,
    "I": I,
    "YOU": YOU,
    "LOVE": LOVE,
    "COMPUTERS": COMPUTERS,
    "STOP": STOP,
}

# Reverse mapping from token IDs to word strings
TOKEN_TO_WORD: dict[Token, str] = {
    EOS: "EOS",
    I: "I",
    YOU: "YOU",
    LOVE: "LOVE",
    COMPUTERS: "COMPUTERS",
    PSEUDO_UNKNOWN: "PSEUDO_UNKNOWN",
    PSEUDO_PUNCTUATION: "PSEUDO_PUNCTUATION",
    STOP: "STOP",
}
