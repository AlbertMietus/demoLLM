"""
LLM Compute Module for DemoLLM.

This module contains the core computation class that processes tokens
through the LLM model to detect valid sentences and perform validation.

Classes
-------
LLMCompute
    The main compute class that takes an LLM model and processes tokens.
    It can feed tokens one by one (stream-like) and detect valid sentences.
"""

from demo_llm.model import LLM
from demo_llm.tokens import (
    Token,
    EOS,
    PSEUDO_UNKNOWN,
    PSEUDO_PUNCTUATION,
    STOP,
    WORD_TO_TOKEN,
    TOKEN_TO_WORD,
)


def tokenize_word(word: str) -> Token:
    """
    Convert a word to its corresponding token ID.

    Implementation follows Option A: words with punctuation are PSEUDO_UNKNOWN.

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


class LLMCompute:
    """
    Compute class for processing tokens through an LLM model.

    This class takes an LLM model instance and provides methods to:
    - Feed tokens one by one (stream-like processing)
    - Get the last result (token or sentence)
    - Detect valid sentences based on the model's weights

    Parameters
    ----------
    llm : LLM
        The LLM model to use for computations.

    Attributes
    ----------
    llm : LLM
        The LLM model instance.
    buffer : list[Token]
        Current buffer of tokens being processed.
    last_result : list[Token] | None
        The last detected valid sentence (as token list).
    """

    def __init__(self, llm: LLM) -> None:
        """
        Initialize the compute module with an LLM model.

        Parameters
        ----------
        llm : LLM
            The LLM model to use for computations.
        """
        self.llm = llm
        self.buffer: list[Token] = []
        self.last_result: list[Token] | None = None

    def _is_valid_transition(self, from_token: Token, to_token: Token) -> bool:
        """
        Check if transitioning from one token to another is valid.

        A transition is valid if the weight is non-zero.

        Parameters
        ----------
        from_token : Token
            The source token ID.
        to_token : Token
            The destination token ID.

        Returns
        -------
        bool
            True if the transition is valid (weight > 0).
        """
        # If either token is outside the weights matrix, it's invalid
        num_tokens = len(self.llm.weights)
        if from_token >= num_tokens or to_token >= num_tokens:
            return False

        return self.llm.weights[from_token][to_token] > 0

    def _can_end_sentence(self, token: Token) -> bool:
        """
        Check if a token can be followed by EOS (end of sentence).

        Parameters
        ----------
        token : Token
            The token to check.

        Returns
        -------
        bool
            True if the token can transition to EOS.
        """
        return self._is_valid_transition(token, EOS)

    def _detect_sentences(self) -> list[list[Token]]:
        """
        Detect all valid sentences in the current buffer.

        A valid sentence is a contiguous sequence of tokens where:
        - Has at least 2 tokens (a single token is not a complete sentence)
        - Each consecutive pair has a valid transition
        - The last token can transition to EOS

        Returns
        -------
        list[list[Token]]
            List of detected sentences (each as a list of tokens).
        """
        sentences: list[list[Token]] = []

        if not self.buffer or len(self.buffer) < 2:
            return sentences

        # Try to find sentences starting at each position
        i = 0
        while i < len(self.buffer):
            # Try to build a sentence starting at position i
            sentence: list[Token] = []
            j = i

            while j < len(self.buffer):
                token = self.buffer[j]

                # If this is the first token in the sentence, just add it
                if not sentence:
                    sentence.append(token)
                    j += 1
                    continue

                # Check if we can transition from the last token in the sentence to this token
                if self._is_valid_transition(sentence[-1], token):
                    sentence.append(token)
                    j += 1
                else:
                    # Invalid transition, stop building this sentence
                    break

            # Check if this sentence can end (last token can transition to EOS)
            # AND has at least 2 tokens (a single token is not a complete sentence)
            if len(sentence) >= 2 and self._can_end_sentence(sentence[-1]):
                sentences.append(sentence)
                # Move past this sentence - we found a complete valid sentence
                i = j
            else:
                # This wasn't a valid sentence, try starting at next position
                i += 1

        return sentences

    def feed_token(self, token_or_word: Token | str) -> None:
        """
        Feed a token or word to the compute module.

        This method processes the token/word and updates the internal state.
        If the token is invalid (UNKNOWN or PUNCTUATION), the buffer is reset.
        Otherwise, the token is added to the buffer and checked for valid sentences.

        Parameters
        ----------
        token_or_word : Token | str
            Either a Token ID or a word string to tokenize.

        Notes
        -----
        - If token_or_word is a string, it will be tokenized first
        - If the resulting token is PSEUDO_UNKNOWN or PSEUDO_PUNCTUATION,
          the buffer is reset
        - If the resulting token is STOP, processing stops
        - After adding a valid token, the buffer is checked for valid sentences
        - If a valid sentence is found, it is stored in last_result and
          removed from the buffer
        """
        # Convert word to token if necessary
        if isinstance(token_or_word, str):
            token = tokenize_word(token_or_word)
        else:
            token = token_or_word

        # Handle STOP token
        if token == STOP:
            self.buffer = []
            return

        # Handle invalid tokens (reset buffer)
        if token == PSEUDO_UNKNOWN or token == PSEUDO_PUNCTUATION:
            self.buffer = []
            return

        # Add token to buffer
        self.buffer.append(token)

        # Detect sentences in the buffer
        sentences = self._detect_sentences()

        if sentences:
            # Store the first detected sentence as last_result
            self.last_result = sentences[0]

            # Remove the detected sentence from the buffer
            sentence_tokens = sentences[0]
            sentence_len = len(sentence_tokens)

            # Find where the sentence starts in the buffer
            for i in range(len(self.buffer) - sentence_len + 1):
                if self.buffer[i:i + sentence_len] == sentence_tokens:
                    # Remove the sentence from the buffer
                    self.buffer = self.buffer[:i] + self.buffer[i + sentence_len:]
                    break

    def get_last_result(self) -> list[Token] | None:
        """
        Get the last detected valid sentence.

        Returns
        -------
        list[Token] | None
            The last detected valid sentence as a list of Token IDs,
            or None if no sentence has been detected yet.

        Notes
        -----
        The returned sentence does NOT include the EOS token.
        """
        return self.last_result

    def get_last_result_as_sentence(self) -> str | None:
        """
        Get the last detected valid sentence as a space-separated string.

        Returns
        -------
        str | None
            The last detected valid sentence as a string,
            or None if no sentence has been detected yet.
        """
        result = self.get_last_result()
        if result is None:
            return None
        words = [TOKEN_TO_WORD[t] for t in result]
        return " ".join(words)

    def reset(self) -> None:
        """
        Reset the compute module state.

        Clears the buffer and last_result.
        """
        self.buffer = []
        self.last_result = None
