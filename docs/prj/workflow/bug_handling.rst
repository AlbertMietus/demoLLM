.. _bug_handling:

===================================
Bug Handling in BDD & TDD Workflow
===================================

:Author: Albert Mietus (with AI assistance)
:Version: 1.0
:Date: 2025-01-28
:Status: Draft

.. note::
    This document describes how to **handle bugs** within a BDD & TDD workflow.
    The core principle: **Always write a test first that reproduces the bug.**

.. toctree::
    :maxdepth: 2
    :caption: Contents

Introduction
============

Bugs are inevitable in software development. However, in a **BDD & TDD workflow**,
bugs are **easier to find, reproduce, and fix** because:

1. Tests run **frequently and automatically**
2. The **scope of the bug** is immediately clear (which test fails)
3. The **expected behavior** is already defined (by the failing test)
4. The **fix can be verified** immediately (test passes after fix)

The Golden Rule
==============

.. admonition:: Core Principle

    **Always write a failing test that reproduces the bug before fixing it.**
    
    Never fix a bug without a test that:
    1. **Fails** before the fix
    2. **Passes** after the fix
    3. **Documents** the expected behavior

Why This Rule Matters
--------------------

Without a test:

- ❌ You don't **know** the bug is really fixed
- ❌ The bug can **reappear** later (regression)
- ❌ You don't **understand** the exact problem
- ❌ Other developers don't **know** about the bug

With a test:

- ✅ You have **proof** the bug is fixed
- ✅ The bug **stays fixed** (regression protection)
- ✅ The **requirements** are clear
- ✅ The **knowledge** is shared

Bug Handling Workflow
=====================

.. code-block:: text

    1. REPRODUCE: Find steps to reproduce the bug
    2. WRITE TEST: Create a test that reproduces the bug
    3. VERIFY FAIL: Confirm the test fails
    4. FIX CODE: Make minimal change to fix the bug
    5. VERIFY PASS: Confirm the test now passes
    6. REFACTOR: Improve code while tests still pass

Let's explore each step:

Step 1: Reproduce the Bug
-------------------------

**Goal:** Find the **exact steps** to reproduce the bug.

**Questions to Answer:**

- What input causes the bug?
- What is the expected output?
- What is the actual output?
- Is the bug consistent or intermittent?

**Example:**

.. code-block:: text

    Bug Report: "demoLLM_validate_tokens.py accepts punctuation"
    
    Reproduction:
    1. Run: echo "I love, computers" | python -m demo_llm.cli.demoLLM_validate_tokens
    2. Expected: exit code 1 (invalid)
    3. Actual: exit code 0 (valid)
    
    The bug is consistent.

Step 2: Write a Test
--------------------

**Goal:** Create a **test that reproduces the bug**.

**Rules for Bug Tests:**

1. **Test should fail** before the fix
2. **Test should pass** after the fix
3. **Test should be minimal** (only test the bug, not the whole system)
4. **Test should be isolated** (not depend on other failing tests)

**Where to Put the Test:**

- If the bug is in a **specific function**: Add to the **TDD test file** for that component
- If the bug is in **system behavior**: Add to the **BDD test file**
- If the bug is **new and unexpected**: Create a new test file

**Example: Tokenizer Bug**

.. code-block:: python

    # In tests/test_003_tokenizer.py
    
    def test_given_word_with_punctuation_when_tokenize_then_returns_unknown():
        """
        BUG: tokenize_word("love,") currently returns LOVE (3)
        EXPECTED: Should return PSEUDO_UNKNOWN (5) or [LOVE, PSEUDO_PUNCTUATION]
        
        This test reproduces the bug where punctuation is stripped instead of detected.
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN
        
        result = tokenize_word("love,")
        
        # This will FAIL with current implementation
        assert result == PSEUDO_UNKNOWN

Step 3: Verify Test Fails
------------------------

**Goal:** Confirm the test **actually reproduces the bug**.

**Action:**

.. code-block:: bash

    pytest tests/test_003_tokenizer.py::test_given_word_with_punctuation_when_tokenize_then_returns_unknown -v

**Expected Output:**

.. code-block:: text

    FAILED tests/test_003_tokenizer.py::test_given_word_with_punctuation_when_tokenize_then_returns_unknown
    AssertionError: assert 3 == 5

**If the test passes:**
- ❌ The bug is **not reproduced**
- ❌ The test is **wrong**
- ❌ Go back to Step 1

Step 4: Fix the Code
--------------------

**Goal:** Make the **minimal change** to fix the bug.

**Rules for Bug Fixes:**

1. **Minimal change**: Only change what's necessary
2. **No refactoring yet**: Fix the bug first, refactor later
3. **All tests must pass**: Don't break existing functionality
4. **Document the fix**: Add comments if the fix is non-obvious

**Example: Fixing the Tokenizer**

.. code-block:: python

    # BEFORE (buggy):
    def tokenize_word(word: str) -> Token:
        stripped = word.strip(".,;:!?()[]{}'\"\n\t ")  # ❌ Strips punctuation
        if not stripped:
            return PSEUDO_PUNCTUATION
        upper_word = stripped.upper()
        if upper_word in WORD_TO_TOKEN:
            return WORD_TO_TOKEN[upper_word]  # ❌ "love," -> "love" -> LOVE
        return PSEUDO_UNKNOWN

    # AFTER (fixed):
    def tokenize_word(word: str) -> Token:
        # If word contains punctuation, it's invalid (or split into tokens)
        if any(c in ".,;:!?()[]{}'\"" for c in word):
            # If entire word is punctuation
            if all(c in ".,;:!?()[]{}'\" \n\t " for c in word):
                return PSEUDO_PUNCTUATION
            # Word with punctuation -> split or mark as unknown
            return PSEUDO_UNKNOWN  # or split into [word_part, punctuation]
        
        upper_word = word.upper()
        if upper_word in WORD_TO_TOKEN:
            return WORD_TO_TOKEN[upper_word]
        return PSEUDO_UNKNOWN

Step 5: Verify Test Passes
------------------------

**Goal:** Confirm the fix **actually works**.

**Action:**

.. code-block:: bash

    pytest tests/test_003_tokenizer.py::test_given_word_with_punctuation_when_tokenize_then_returns_unknown -v

**Expected Output:**

.. code-block:: text

    PASSED tests/test_003_tokenizer.py::test_given_word_with_punctuation_when_tokenize_then_returns_unknown

**If the test still fails:**
- ❌ The fix is **incomplete**
- ❌ Go back to Step 4

Step 6: Refactor (Optional)
---------------------------

**Goal:** Improve the code **while maintaining correctness**.

**Rules for Refactoring:**

1. **All tests must pass** before and after refactoring
2. **Small steps**: One refactoring at a time
3. **Test after each change**: Don't break anything
4. **Improve readability**: Better names, structure, etc.

**Example: Refactoring the Tokenizer**

.. code-block:: python

    # BEFORE:
    def tokenize_word(word: str) -> Token:
        if any(c in ".,;:!?()[]{}'\"" for c in word):
            if all(c in ".,;:!?()[]{}'\" \n\t " for c in word):
                return PSEUDO_PUNCTUATION
            return PSEUDO_UNKNOWN
        upper_word = word.upper()
        if upper_word in WORD_TO_TOKEN:
            return WORD_TO_TOKEN[upper_word]
        return PSEUDO_UNKNOWN

    # AFTER (refactored):
    PUNCTUATION_CHARS = ".,;:!?()[]{}'\""
    
    def tokenize_word(word: str) -> Token:
        if not word or all(c in f"{PUNCTUATION_CHARS} \n\t " for c in word):
            return PSEUDO_PUNCTUATION
        
        if any(c in PUNCTUATION_CHARS for c in word):
            return PSEUDO_UNKNOWN
        
        upper_word = word.upper()
        return WORD_TO_TOKEN.get(upper_word, PSEUDO_UNKNOWN)

Bug Types and Handling
======================

Different types of bugs require different approaches:

1. **Regression Bugs**
   - A test that **used to pass** now fails
   - **Action:** Find what changed, revert or fix
   - **Prevention:** Don't remove tests, keep test coverage high

2. **New Feature Bugs**
   - Bug found while **developing new features**
   - **Action:** Write test, fix, continue development
   - **Prevention:** Use BDD-TDD workflow from the start

3. **Legacy Code Bugs**
   - Bug in **existing, untested code**
   - **Action:**
     1. Write a **characterization test** (documents current behavior)
     2. Write a **new test** for expected behavior
     3. Fix the code to pass the new test
   - **Prevention:** Gradually add tests to legacy code

4. **Edge Case Bugs**
   - Bug found in **unusual input/situation**
   - **Action:** Add test for the edge case, fix
   - **Prevention:** Think about edge cases when writing tests

5. **Integration Bugs**
   - Bug in **how components work together**
   - **Action:** Write integration test, fix interface
   - **Prevention:** Test interfaces between components

Example: The "love," Bug in DemoLLM
==================================

Let's trace through the **complete bug handling workflow** for the punctuation issue:

**Bug Report:**
- CLI: ``demoLLM_validate_tokens.py``
- Input: ``"I love, computers"``
- Expected: exit code 1 (contains invalid token)
- Actual: exit code 0 (all tokens valid)

**Step 1: Reproduce**

.. code-block:: bash

    echo "I love, computers" | python -m demo_llm.cli.demoLLM_validate_tokens
    echo $?  # Returns 0, should be 1

**Step 2: Write Test**

.. code-block:: python

    # In tests/test_003_tokenizer.py
    
    def test_tokenize_word_with_trailing_comma_returns_unknown():
        """
        BUG: tokenize_word("love,") returns LOVE (3)
        EXPECTED: PSEUDO_UNKNOWN (5) because word contains punctuation
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN
        
        result = tokenize_word("love,")
        assert result == PSEUDO_UNKNOWN

**Step 3: Verify Fail**

.. code-block:: bash

    pytest tests/test_003_tokenizer.py::test_tokenize_word_with_trailing_comma_returns_unknown -v
    # FAILED: assert 3 == 5

**Step 4: Fix Code**

.. code-block:: python

    # In src/demo_llm/compute.py
    
    def tokenize_word(word: str) -> Token:
        # Check if word contains punctuation
        if any(c in ".,;:!?()[]{}'\"" for c in word):
            # If entire word is punctuation
            if all(c in ".,;:!?()[]{}'\" \n\t " for c in word):
                return PSEUDO_PUNCTUATION
            # Word with punctuation is invalid
            return PSEUDO_UNKNOWN
        
        upper_word = word.upper()
        return WORD_TO_TOKEN.get(upper_word, PSEUDO_UNKNOWN)

**Step 5: Verify Pass**

.. code-block:: bash

    pytest tests/test_003_tokenizer.py::test_tokenize_word_with_trailing_comma_returns_unknown -v
    # PASSED

**Step 6: Refactor**

.. code-block:: python

    # Extract constants
    PUNCTUATION_CHARS = ".,;:!?()[]{}'\""
    
    def tokenize_word(word: str) -> Token:
        if not word:
            return PSEUDO_PUNCTUATION
        
        if all(c in f"{PUNCTUATION_CHARS} \n\t " for c in word):
            return PSEUDO_PUNCTUATION
        
        if any(c in PUNCTUATION_CHARS for c in word):
            return PSEUDO_UNKNOWN
        
        return WORD_TO_TOKEN.get(word.upper(), PSEUDO_UNKNOWN)

**Result:**
- Bug is **fixed**
- Bug is **documented** (by the test)
- Bug **won't reappear** (test protects against regression)
- Code is **cleaner** (after refactoring)

Git Workflow for Bug Fixes
==========================

Bug fixes should follow the **same Git workflow** as features:

.. code-block:: text

    1. git branch: bugfix/[short-description]
    2. git commit: "Add test reproducing [bug] (failing)"
    3. git commit: "Fix [bug] in [component]"
    4. git push + PR

**Example:**

.. code-block:: bash

    git checkout -b bugfix/love-comma-tokenization
    
    # Add failing test
    git add tests/test_003_tokenizer.py
    git commit -m "Add test for love, tokenization bug (failing)"
    
    # Fix the bug
    git add src/demo_llm/compute.py
    git commit -m "Fix tokenize_word to detect punctuation in words"
    
    git push origin bugfix/love-comma-tokenization

When to Use xfail for Bugs
==========================

Sometimes you find a bug but **can't fix it immediately**. In this case:

1. **Write the test** that reproduces the bug
2. **Mark it as xfail** with a clear reason
3. **Track it** in your issue tracker
4. **Fix it later**

**Example:**

.. code-block:: python

    @pytest.mark.xfail(reason="Bug #123: tokenizer strips punctuation instead of detecting")
    def test_tokenize_word_with_punctuation_returns_unknown():
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN
        
        assert tokenize_word("love,") == PSEUDO_UNKNOWN

**When to Remove xfail:**
- When the bug is **fixed**
- When the test **passes**
- **Always** remove the xfail marker (don't leave it in the code)

Bug Prevention
==============

The best way to handle bugs is to **prevent them**:

1. **Use BDD-TDD Workflow**
   - Tests define behavior first
   - Code satisfies tests
   - Bugs are caught early

2. **Write Testable Code**
   - Small functions
   - Clear interfaces
   - No global state

3. **Test Frequently**
   - Run tests **after every change**
   - Use **CI/CD** for automated testing
   - **Never** commit with failing tests

4. **Code Reviews**
   - Review **tests** as well as code
   - Ask: "What edge cases are missing?"
   - Verify tests **actually test** the requirements

5. **Document Decisions**
   - Why was this approach chosen?
   - What edge cases were considered?
   - What assumptions were made?

Working with AI on Bugs
=======================

When using AI to help with bugs:

1. **Describe the Bug Clearly**
   - Input, expected output, actual output
   - Steps to reproduce
   - Current code behavior

2. **Ask for Tests First**
   - "What test should I write to reproduce this bug?"
   - "What edge cases should this test cover?"

3. **Review the Fix**
   - "Does this fix address the root cause?"
   - "Are there any side effects?"
   - "Is this the minimal fix?"

4. **Ask for Prevention**
   - "How can I prevent this type of bug in the future?"
   - "What tests should I add to catch similar bugs?"

Example AI Interaction
----------------------

.. code-block:: text

    User: I found a bug in my tokenizer. Input "love," returns LOVE token instead of PSEUDO_UNKNOWN.
    
    AI: Let's handle this with the bug workflow:
    
    Step 1: Can you reproduce it?
    User: Yes, tokenize_word("love,") returns 3 (LOVE) instead of 5 (PSEUDO_UNKNOWN)
    
    Step 2: Write this test:
    ```python
    def test_tokenize_word_with_comma_returns_unknown():
        assert tokenize_word("love,") == PSEUDO_UNKNOWN
    ```
    
    Step 3: Does it fail?
    User: Yes, assert 3 == 5 fails
    
    Step 4: The fix is to check for punctuation in the word:
    ```python
    def tokenize_word(word: str) -> Token:
        if any(c in PUNCTUATION_CHARS for c in word):
            if all(c in PUNCTUATION_CHARS or c.isspace() for c in word):
                return PSEUDO_PUNCTUATION
            return PSEUDO_UNKNOWN
        # ... rest
    ```
    
    Step 5: Verify the test passes
    Step 6: Consider refactoring

Summary
=======

.. admonition:: Key Takeaways

    1. **Always write a test first** that reproduces the bug
    2. **Verify the test fails** before fixing
    3. **Make minimal changes** to fix the bug
    4. **Verify the test passes** after fixing
    5. **Refactor** to improve code quality
    6. **Never leave xfail markers** in the code

By following this workflow, you:
- ✅ **Find bugs faster**
- ✅ **Fix bugs correctly**
- ✅ **Prevent regressions**
- ✅ **Document expected behavior**
- ✅ **Improve code quality**

See Also
========

- :ref:`bdd_tdd_cycle` - The BDD & TDD development process
- :ref:`git_workflow` - How to integrate with Git
- :doc:`/AIblog/love_comma_example` - A concrete example of bug handling
