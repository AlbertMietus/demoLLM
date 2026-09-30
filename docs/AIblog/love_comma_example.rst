.. _love_comma_example:

=======================================================
The "love," Tokenization Bug: A BDD-TDD Case Study
=======================================================

:Author: AI Assistant (with Albert Mietus guidance)
:Post Date: 2025-01-28
:Category: Software Engineering, BDD, TDD, Debugging
:Status: Draft
:Tags: BDD, TDD, tokenizer, bug handling, workflow

.. note::
    This blog post illustrates the **BDD-TDD workflow** through a concrete example from
    the DemoLLM project. It shows how a simple punctuation handling issue revealed
    deeper lessons about test-driven development.

.. image:: https://img.shields.io/badge/Status-Draft-yellow.svg
    :alt: Draft Status

.. image:: https://img.shields.io/badge/Topic-BDD%20%26%20TDD-blue.svg
    :alt: BDD & TDD Topic

----

**"A journey of a thousand miles begins with a single test."**

-- Adapted from Lao Tzu, for software engineers

----

Introduction
============

I was implementing the LLM compute module for DemoLLM, a minimalistic LLM demonstration
project. The requirements were clear:

- Create CLI scripts that process text input
- Validate tokens
- Find valid sentences

I wrote the code, I wrote the tests, and most things worked. But then I hit a wall:
**6 CLI tests were failing**, and I couldn't figure out why.

This is the story of how I learned that **the order matters**:
**BDD first, then TDD, then code.**

And how a simple punctuation character taught me more about software engineering
than any textbook could.

The Problem: Failing CLI Tests
===============================

I had implemented:

1. A tokenizer that converts words to tokens
2. A compute module that processes tokens
3. CLI scripts that use the compute module

And I had tests:

- 26 TDD tests for the compute module (all passing ✅)
- 58 BDD tests for the CLIs (52 passing, 6 failing ❌)

The failing tests were all related to **punctuation handling**:

.. code-block:: python

    # Test that was failing
    def test_given_word_with_punctuation_when_run_then_exit_1():
        result = run_cli("I love, computers")
        assert result.returncode == 1  # Expected: invalid (contains punctuation)
        # Actual: 0 (all tokens valid)

Why was this failing? Let me trace through what was happening.

The Investigation
=================

**Step 1: Check the CLI**

The CLI script ``demoLLM_validate_tokens.py`` does this:

.. code-block:: python

    for word in input.split():
        token = tokenize_word(word)
        if token not in BASE_TOKENS:
            sys.exit(1)
    sys.exit(0)

**Step 2: Check tokenize_word**

My implementation was:

.. code-block:: python

    def tokenize_word(word: str) -> Token:
        stripped = word.strip(".,;:!?()[]{}'\"\n\t ")  # Strip punctuation!
        if not stripped:
            return PSEUDO_PUNCTUATION
        upper_word = stripped.upper()
        if upper_word in WORD_TO_TOKEN:
            return WORD_TO_TOKEN[upper_word]  # "love" -> LOVE (3)
        return PSEUDO_UNKNOWN

**Step 3: Trace the Input**

Input: ``"I love, computers"``

Split on whitespace: ``["I", "love,", "computers"]``

Tokenization:
- ``"I"`` → ``strip()`` → ``"I"`` → ``I`` (1) ✅
- ``"love,"`` → ``strip(".,...")`` → ``"love"`` → ``LOVE`` (3) ❌ **BUG!**
- ``"computers"`` → ``strip()`` → ``"computers"`` → ``COMPUTERS`` (4) ✅

All tokens are in ``BASE_TOKENS = {EOS, I, YOU, LOVE, COMPUTERS}``, so exit code 0.

**But the test expected exit code 1!**

The Root Cause
==============

The bug was in **one line** of the tokenizer:

.. code-block:: python

    stripped = word.strip(".,;:!?()[]{}'\"\n\t ")

This **removes punctuation** from the word, instead of **detecting it**.

So ``"love,"`` became ``"love"``, which is a valid token.

The Question: What Should Happen?
===============================

Now I faced a **design decision**:

**Option A:** ``"love,"`` is **1 token** → ``PSEUDO_UNKNOWN``
- Rationale: A word with punctuation is not a standard word

**Option B:** ``"love,"`` is **2 tokens** → ``[LOVE, PSEUDO_PUNCTUATION]``
- Rationale: Split punctuation from words

**Which is correct?**

I didn't know! And that was the **real problem**.

The Lesson: BDD Comes First
===========================

Here's what I should have done:

**BEFORE writing any code:**

1. **Write BDD tests** for the CLIs with ``xfail`` markers
2. **Ask:** "What should ``demoLLM_validate_tokens.py`` do with ``"I love, computers"``?"
3. **Decide:** "It should return exit code 1 (invalid)"
4. **Write the BDD test:**

.. code-block:: python

    @pytest.mark.xfail(reason="tokenizer not implemented")
    def test_given_input_with_punctuation_when_validate_then_exits_with_1():
        result = run_cli("I love, computers")
        assert result.returncode == 1

5. **THEN ask:** "How do we achieve this?"
6. **Write TDD tests** for the tokenizer:

.. code-block:: python

    def test_tokenize_word_with_punctuation():
        # Option A: 1 token
        assert tokenize_word("love,") == PSEUDO_UNKNOWN
        
        # OR Option B: 2 tokens (requires different approach)
        # assert tokenize_word("love,") == [LOVE, PSEUDO_PUNCTUATION]

7. **Decide on the design** (with the team/product owner)
8. **Implement** the tokenizer to match the decision

But I did it **backwards**:

1. Wrote the tokenizer (with a design assumption)
2. Wrote the compute module
3. Wrote the CLIs
4. Wrote the tests
5. **Found the bug**

The Design Decision
==================

After reading Albert's MESS framework and his hints, I realized:

- **CLI tests are specifications**
- **They should be written FIRST**
- **They should be marked as xfail** until the code is ready

So I asked myself: **"When should we have decided about 'love,'?"**

**Answer:** At the **BDD phase**, when writing the CLI tests.

Here's the **correct workflow**:

.. code-block:: text

    1. Write CLI stub: demoLLM_validate_tokens.py
    2. Write BDD test: echo "I love, computers" should exit with 1
    3. Mark as xfail: "tokenizer not implemented"
    4. Write TDD test: tokenize_word("love,") should return... what?
    5. DECIDE: "love," = PSEUDO_UNKNOWN (Option A)
    6. Implement tokenizer to return PSEUDO_UNKNOWN for words with punctuation
    7. Remove xfail from BDD test

But I missed **Step 5**: the **design decision** about how to handle punctuation.

The Fix: Correct Workflow
==========================

Let me show you how this **should** have gone:

**Commit 1: BDD Tests (xfail)**

.. code-block:: bash

    git checkout -b feature/llm-reken-module
    
    # Create CLI stubs
    touch src/demo_llm/cli/demoLLM_*.py
    
    # Create BDD tests
    # tests/cli/test_demoLLM_validate_tokens.py
    @pytest.mark.xfail(reason="tokenizer not implemented")
    def test_given_input_with_punctuation_when_validate_then_exits_with_1():
        result = run_cli("I love, computers")
        assert result.returncode == 1
    
    git add src/demo_llm/cli/ tests/cli/
    git commit -m "Add BDD tests for LLM CLIs (xfail - tokenizer missing)"

**Commit 2: TDD Tests for Tokenizer**

.. code-block:: bash

    # tests/test_003_tokenizer.py
    def test_tokenize_word_known_words():
        assert tokenize_word("I") == I
        assert tokenize_word("love") == LOVE
    
    def test_tokenize_word_unknown():
        assert tokenize_word("hello") == PSEUDO_UNKNOWN
    
    @pytest.mark.xfail(reason="design decision needed: 1 or 2 tokens?")
    def test_tokenize_word_with_punctuation():
        # Option A: 1 token
        assert tokenize_word("love,") == PSEUDO_UNKNOWN
        
        # Option B: 2 tokens (would require different tokenizer approach)
        # assert tokenize_word("love,") == [LOVE, PSEUDO_PUNCTUATION]
    
    git add tests/test_003_tokenizer.py
    git commit -m "Add TDD tests for tokenizer (failing - design decision needed)"

**At this point, we stop and ask:** "How should we handle 'love,'?"

After discussion with the team/product owner, we decide: **Option A** (1 token, PSEUDO_UNKNOWN)

**Commit 3: Update TDD Tests**

.. code-block:: bash

    # Update tests/test_003_tokenizer.py
    def test_tokenize_word_with_punctuation_returns_unknown():
        assert tokenize_word("love,") == PSEUDO_UNKNOWN
    
    git add tests/test_003_tokenizer.py
    git commit -m "Update tokenizer tests: words with punctuation are UNKNOWN"

**Commit 4: Implement Tokenizer**

.. code-block:: python

    # src/demo_llm/compute.py
    def tokenize_word(word: str) -> Token:
        # If word contains punctuation, it's invalid
        if any(c in ".,;:!?()[]{}'\"" for c in word):
            # Unless the entire word IS punctuation
            if all(c in ".,;:!?()[]{}'\" \n\t " for c in word):
                return PSEUDO_PUNCTUATION
            return PSEUDO_UNKNOWN
        
        upper_word = word.upper()
        return WORD_TO_TOKEN.get(upper_word, PSEUDO_UNKNOWN)
    
    git add src/demo_llm/compute.py
    git commit -m "Implement tokenize_word to detect punctuation in words"

**Commit 5: Remove xfail from BDD Tests**

.. code-block:: bash

    # Update tests/cli/test_demoLLM_validate_tokens.py
    # Remove @pytest.mark.xfail
    
    git add tests/cli/test_demoLLM_validate_tokens.py
    git commit -m "Remove xfail from validate_tokens tests - tokenizer complete"

**Result:** All tests pass! 🎉

The Actual Decision: Option B
=============================

After more thought and reading Albert's feedback, I realized:

**Option B (2 tokens) is actually better** because:

1. It's **more precise** - punctuation is a separate concept
2. It allows **CLI3b** to work (where PSEUDO_PUNCTUATION is valid)
3. It's **more extensible** - we can handle punctuation differently

So the **real workflow** should have been:

.. code-block:: text

    1. BDD: Write CLI tests (xfail)
    2. TDD: Write tokenizer tests (failing)
    3. DESIGN: Decide "love," = [LOVE, PSEUDO_PUNCTUATION] (Option B)
    4. TDD: Update tokenizer tests for Option B
    5. IMPLEMENT: tokenizer that SPLITS on punctuation
    6. INTEGRATE: Update CLIs to handle split tokens
    7. VERIFY: Remove xfail from BDD tests

But to do **Option B**, we need a different approach:

**The Tokenizer Needs to Return Multiple Tokens**

.. code-block:: python

    # Option B requires:
    def tokenize_word(word: str) -> list[Token]:
        # Split word into tokens
        # "love," -> ["love", ","] -> [LOVE, PSEUDO_PUNCTUATION]
        pass

Or we **pre-split** the input before tokenization:

.. code-block:: python

    # In CLI:
    for word in input.split():
        # First split word into sub-tokens
        sub_tokens = split_word_on_punctuation(word)
        for sub_token in sub_tokens:
            token = tokenize_word(sub_token)
            # process token

This is a **design decision** that should have been made **at the BDD phase**.

The Lessons Learned
===================

**Lesson 1: BDD First, Always**

BDD tests (CLI tests) should be written **first**. They define **what** the system should do.

TDD tests should be written **second**. They define **how** the components achieve that.

Code should be written **last**. It satisfies the tests.

**Lesson 2: xfail is Your Friend**

Use ``@pytest.mark.xfail`` to mark tests that can't pass yet.

This:
- Documents **what's missing**
- Provides **direction** for development
- Shows **progress** as xfail markers are removed

**Lesson 3: Design Decisions Belong in BDD**

Questions like:
- "Should 'love,' be 1 token or 2?"
- "How do we handle punctuation?"

These should be **answered during BDD**, not discovered during debugging.

**Lesson 4: The Order Matters**

.. code-block:: text

    CORRECT ORDER:          WRONG ORDER:
    ─────────────          ────────────
    1. BDD tests (xfail)     1. Write code
    2. TDD tests (failing)    2. Write tests
    3. Design decisions       3. Find bugs
    4. Implement code         4. Fix bugs
    5. Remove xfail           5. Hope it works

**Lesson 5: Tests Are Specifications**

Tests don't just **verify** code - they **define** it.

A failing test is not a problem - it's a **specification** of what needs to be done.

The Current State
================

As of this writing, I have:

- ✅ **Fixed the tokenizer** (Option A: words with punctuation = PSEUDO_UNKNOWN)
- ✅ **All TDD tests pass** (26/26)
- ⚠️ **6 CLI tests still fail** (52/58)

The remaining failures are because:
1. The CLIs expect **Option B** (split punctuation)
2. But the tokenizer implements **Option A** (punctuation = UNKNOWN)

**The fix:** Decide on Option A or B, then implement consistently.

Based on Albert's feedback, **Option B is correct**.

So the remaining work is:

1. Update tokenizer to **split** words on punctuation
2. Update CLIs to handle **multiple tokens per word**
3. All tests will pass

But the **real win** is that I now understand:

**The workflow prevents bugs by making design decisions explicit, early, and testable.**

Conclusion
==========

A simple punctuation character taught me:

1. **BDD comes first** - Define behavior before implementation
2. **TDD comes second** - Define components before coding
3. **Design decisions are tests** - Write tests to document decisions
4. **xfail is a roadmap** - It shows what's left to do
5. **The order matters** - Tests → Code, not Code → Tests

And most importantly:

**When you find a bug, ask: "When should we have caught this?"**

The answer is almost always: **Earlier in the BDD-TDD cycle.**

.. admonition:: Final Thought

    The "love," bug wasn't a bug in the code.
    It was a bug in the **process**.
    
    And the fix isn't just in the tokenizer.
    It's in how we **think about development**.

References
==========

- :ref:`bdd_tdd_cycle` - The BDD & TDD workflow
- :ref:`git_workflow` - Git integration with BDD/TDD
- :ref:`bug_handling` - How to handle bugs properly
- `MESS Framework <https://mess.softwarebetermaken.nl/en/latest/SoftwareCompetence/LeanEngineering/BDD_TDD/>`_

.. _comments:

Comments
=======

*Please enable JavaScript to view the Disqus comments.*

.. note::
    This blog post is a **living document**. As I continue to work on DemoLLM,
    I'll update it with new insights and lessons learned.

    **TODO:** Update with actual Git branch/commit references once the code is committed.
