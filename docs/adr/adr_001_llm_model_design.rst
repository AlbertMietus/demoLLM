.. (C) Albert Mietus -- mostly made by codeAI=mistral-medium-3-5

ADR 001: LLM Model Design
==========================

Status
------
Accepted

Context
-------
We need to create a minimalistic LLM model that demonstrates how modern
generative AI systems work. The model should be:

1. Simple enough to understand and inspect
2. Representative of real LLM architectures
3. Extensible for future enhancements
4. Testable with TDD principles

The model needs to support a small set of tokens (I, YOU, LOVE, COMPUTERS, EOS)
and be able to generate simple English sentences like:
- "I love computers"
- "You love computers"
- "I love you"

Decision
--------
We will implement the LLM model as a **dataclass** with the following components:

1. **Token Mappings**: Two dictionaries for bidirectional token-ID conversion
   - ``token_to_id: Dict[str, int]``
   - ``id_to_token: Dict[int, str]``

2. **Weights Matrix**: A square matrix (n x n) where weights[i][j] represents
   the probability (0-100) that token j follows token i
   - ``weights: List[List[int]]``

3. **Factory Function**: A function to create a pre-configured demo LLM
   - ``create_demo_llm() -> LLM``

The weights matrix represents a **first-order Markov chain** where the probability
of the next token depends only on the current token. This is a simplification
of real LLMs but serves our demonstration purposes well.

Rationale
---------

**Why a dataclass?**
- Dataclasses provide a clean, immutable way to store data
- They automatically generate ``__init__``, ``__repr__``, and other methods
- They clearly separate data from behavior
- They are easy to test and inspect

**Why a Markov chain approach?**
- Simple to understand and implement
- Directly represents token transition probabilities
- Scales well for our small token set
- Can be extended to higher-order Markov chains later

**Why percentages (0-100) instead of probabilities (0.0-1.0)?**
- More intuitive for demonstration purposes
- Avoids floating-point precision issues
- Easier to validate (integers are simpler)

**Why separate token mappings from weights?**
- Clear separation of concerns
- Allows for different tokenizations with the same weights
- Makes the structure more similar to real LLM implementations

Consequences
-----------

**Positive:**
- The model is extremely simple and easy to understand
- All components are explicitly visible and inspectable
- Easy to test with TDD
- Can be extended to support more tokens or different architectures

**Negative:**
- Not a real neural network (but that's intentional for demo purposes)
- Limited to first-order dependencies (but sufficient for our use case)
- Weights are hardcoded (but that's acceptable for a demo)

Alternatives Considered
-----------------------

1. **Neural Network Approach**: Implement a tiny neural network with
   embeddings and a prediction head. Rejected because it would be too complex
   for a demo and harder to inspect.

2. **Probability Matrix (0.0-1.0)**: Use floating-point probabilities instead
   of percentages. Rejected for simplicity and intuitiveness.

3. **Single Dictionary for Tokens**: Use a single dictionary with tokens as
   keys and both ID and other info as values. Rejected for clarity and
   separation of concerns.

4. **Class with Methods**: Make LLM a full class with prediction methods.
   Rejected because we want to separate data (model) from behavior (inference).
   Prediction logic can be added in a separate class later.

Related Decisions
----------------
- ADR 002: Tokenization Strategy (to be created)
- ADR 003: Inference Engine Design (to be created)
