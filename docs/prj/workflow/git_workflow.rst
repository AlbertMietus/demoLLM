.. _git_workflow:

=======================================
Git Workflow with BDD & TDD
=======================================

:Author: Albert Mietus (with AI assistance)
:Version: 1.0
:Date: 2025-01-28
:Status: Draft

.. note::
    This document describes how to integrate **Git version control** with the
    **BDD & TDD workflow**. Each commit should represent a small, testable step
    in the development process.

.. toctree::
    :maxdepth: 2
    :caption: Contents

Introduction
============

Git is not just a version control system; when combined with BDD & TDD, it becomes a
**powerful tool for tracking progress, ensuring quality, and enabling collaboration**.

The key principle is: **Each commit should move the codebase from one valid state to another.**

This means:
- Every commit should have **passing tests** (or intentionally failing tests marked with xfail)
- The commit message should **explain the step** in the BDD-TDD cycle
- The git history should **tell the story** of how the feature was developed

References
=========

This workflow is based on the BDD & TDD principles from:

- `Introducing BDD & TDD <https://mess.softwarebetermaken.nl/en/latest/SoftwareCompetence/LeanEngineering/BDD_TDD/01.introducingB+TDD.html>`_
- `Applying BDD & TDD in Legacy <https://mess.softwarebetermaken.nl/en/latest/SoftwareCompetence/LeanEngineering/BDD_TDD/02.applyingBTDD_inLegacy.html>`_

The Git-BDD-TDD Cycle
=====================

The development process follows this **commit sequence**:

.. code-block:: text

    1. git branch: feature/[description]
    2. git commit: "Add BDD tests (xfail) for [feature]"
    3. git commit: "Add TDD tests for [module]"
    4. git commit: "Implement [module] to pass TDD tests"
    5. git commit: "Integrate [module] into [system]"
    6. git commit: "Remove xfail from BDD tests"
    7. git push + Create PR

Let's break this down:

Step 1: Create Feature Branch
----------------------------

**When:** Starting a new feature or component

**Action:**

.. code-block:: bash

    git checkout main
    git pull origin main
    git checkout -b feature/[short-description]
    # Example: git checkout -b feature/llm-reken-module

**Why:**
- Isolates the feature development
- Allows for independent testing
- Makes it easy to review and merge

Step 2: Add BDD Tests (xfail)
-----------------------------

**When:** Defining the system behavior

**Action:**

.. code-block:: bash

    # Create CLI stubs
    touch src/demo_llm/cli/demoLLM_*.py
    
    # Create BDD tests with xfail markers
    # tests/cli/test_demoLLM_*.py
    
    git add src/demo_llm/cli/ tests/cli/
    git commit -m "Add BDD tests for LLM CLIs (xfail - rekenmodule missing)"

**Commit Message Format:**

.. code-block:: text

    Add BDD tests for [feature] (xfail - [reason])
    
    - Created CLI scripts: [list]
    - Added BDD tests: [list]
    - All tests marked as xfail: [reason]

**Why:**
- Defines the **acceptance criteria** first
- Shows what needs to be implemented
- Provides **direction** for TDD phase

**Example Commit:**

.. code-block:: bash

    git commit -m "Add BDD tests for LLM CLI scripts (xfail - rekenmodule not implemented)
    
    - Created demoLLM_find_first_sentence.py
    - Created demoLLM_find_all_sentences.py  
    - Created demoLLM_validate_tokens.py
    - Created demoLLM_validate_tokens_with_punctuation.py
    - Added pytest tests with xfail markers
    - Reason: compute module and tokenizer not implemented"

Step 3: Add TDD Tests
----------------------

**When:** Starting to implement components

**Action:**

.. code-block:: bash

    # Write failing unit tests for a component
    # tests/test_00X_component.py
    
    git add tests/test_00X_component.py
    git commit -m "Add TDD tests for [component] (failing)"

**Commit Message Format:**

.. code-block:: text

    Add TDD tests for [component] (failing)
    
    - Tests for: [list of functions/classes]
    - All tests currently fail
    - Next: Implement [component]

**Why:**
- Defines the **interface** of the component
- Shows what behavior is expected
- Provides **specifications** for implementation

**Example Commit:**

.. code-block:: bash

    git commit -m "Add TDD tests for tokenizer function (failing)
    
    - test_tokenize_word with known words
    - test_tokenize_word with unknown words
    - test_tokenize_word with punctuation
    - All tests fail: tokenizer not implemented"

Step 4: Implement Component
--------------------------

**When:** Making TDD tests pass

**Action:**

.. code-block:: bash

    # Implement the component to pass tests
    # src/demo_llm/[module].py
    
    git add src/demo_llm/[module].py
    git commit -m "Implement [component] to pass TDD tests"

**Commit Message Format:**

.. code-block:: text

    Implement [component] to pass TDD tests
    
    - Implemented: [list of functions/classes]
    - All TDD tests now pass
    - Next: Integrate into [system]

**Why:**
- **Minimal implementation** to pass tests
- Follows **Red-Green-Refactor** cycle
- Each commit is **small and focused**

**Example Commit:**

.. code-block:: bash

    git commit -m "Implement tokenize_word function to pass TDD tests
    
    - Implemented tokenize_word in compute.py
    - Handles known words, unknown words, punctuation
    - All tokenizer tests pass"

Step 5: Integrate Components
-----------------------------

**When:** Connecting TDD-tested components to the system

**Action:**

.. code-block:: bash

    # Update CLIs to use the new components
    # Update __init__.py files for exports
    
    git add src/demo_llm/cli/*.py src/demo_llm/__init__.py
    git commit -m "Integrate [component] into CLIs"

**Commit Message Format:**

.. code-block:: text

    Integrate [component] into [system]
    
    - Updated: [list of files]
    - CLIs now use [component]
    - BDD tests may still fail (xfail)

**Why:**
- Connects **components to system**
- Prepares for **BDD test validation**
- May reveal **integration issues**

**Example Commit:**

.. code-block:: bash

    git commit -m "Integrate compute module into CLIs
    
    - Updated demoLLM_*.py to use LLMCompute
    - Updated __init__.py to export compute module
    - BDD tests still marked as xfail"

Step 6: Remove xfail Markers
---------------------------

**When:** All tests pass

**Action:**

.. code-block:: bash

    # Remove xfail markers from BDD tests
    # Run all tests to verify
    
    git add tests/cli/*.py
    git commit -m "Remove xfail from BDD tests - all passing"

**Commit Message Format:**

.. code-block:: text

    Remove xfail from BDD tests for [feature]
    
    - Removed xfail markers: [list]
    - All BDD tests now pass
    - Feature [feature] is complete

**Why:**
- **Validates** that BDD requirements are met
- Shows **progress** in git history
- Feature is **ready for review**

**Example Commit:**

.. code-block:: bash

    git commit -m "Remove xfail from LLM CLI tests - all passing
    
    - Removed xfail from all CLI tests
    - All 58 BDD tests pass
    - All 26 TDD tests pass
    - LLM rekenmodule feature complete"

Step 7: Push and Create PR
--------------------------

**When:** Feature is complete and tested

**Action:**

.. code-block:: bash

    git push origin feature/[description]
    # Create Pull Request with description

**For AI Agents with Explicit Merge Permission:**

When the user explicitly states "Je mag hem direct mergen!" or similar phrases,
the AI agent **should merge the PR directly** using the GitHub CLI.

This is an exception to the normal workflow where PRs are created for review.
The explicit permission overrides the need for manual review.

.. code-block:: bash

    # First, ensure the branch is up to date with main
    git checkout feature/[description]
    git pull origin main
    git push origin feature/[description]

    # Then merge the PR using gh CLI
    gh pr merge --repo owner/repo --pr <number> --squash --delete-branch

.. note::
    The ``--squash`` flag combines all commits into one, and ``--delete-branch``
    removes the feature branch after merging. Use these flags when explicitly
    permitted by the user.

**PR Description Format:**

.. code-block:: markdown

    ## Summary
    - Implemented LLM rekenmodule with compute class
    - Added 4 CLI scripts for sentence detection and token validation
    - All tests passing (26 TDD + 58 BDD)

    ## Changes
    - Added `src/demo_llm/tokens.py` - Token definitions
    - Added `src/demo_llm/compute.py` - Compute module with LLMCompute class
    - Added `src/demo_llm/cli/` - CLI scripts
    - Added `tests/test_002_llm_compute.py` - TDD tests
    - Added `tests/test_003_tokenizer.py` - TDD tests
    - Added `tests/cli/` - BDD tests

    ## Verification
    ```bash
    pytest tests/ -v  # All 84 tests pass
    ```

    Closes #XXX

**Why:**
- **Shares** the completed feature
- Allows for **code review**
- Enables **collaboration**

Branch Naming Convention
=======================

Use **descriptive, consistent** branch names:

.. code-block:: text

    feature/[short-description]    # New features
    bugfix/[short-description]     # Bug fixes
    refactor/[short-description]   # Code refactoring
    docs/[short-description]       # Documentation only

Examples:

- ``feature/llm-reken-module``
- ``feature/tokenizer-split-punctuation``
- ``bugfix/love-comma-tokenization``
- ``refactor/compute-module``
- ``docs/bdd-tdd-workflow``

Commit Message Guidelines
=========================

1. **Use Imperative Mood**
   - ✅ ``Add BDD tests for CLIs``
   - ❌ ``Added BDD tests for CLIs``
   - ❌ ``Adding BDD tests for CLIs``

2. **Be Specific**
   - ✅ ``Add TDD tests for tokenize_word with punctuation``
   - ❌ ``Add tests``

3. **Include Context**
   - ✅ ``Add xfail BDD tests (rekenmodule not implemented)``
   - ❌ ``Add tests``

4. **Keep it Short**
   - First line: <50 characters
   - Body: Explain what and why

5. **Reference Issues**
   - Include issue/PR numbers if applicable

Example Commit Messages
----------------------

.. code-block:: text

    Add BDD tests for LLM CLI scripts (xfail)
    
    - Created 4 CLI stubs
    - Added 58 BDD tests with xfail markers
    - Reason: compute module not implemented

    Implement tokenize_word to handle punctuation
    
    - Words with punctuation split into separate tokens
    - "love," -> [LOVE, PSEUDO_PUNCTUATION]
    - All tokenizer tests pass

    Remove xfail from validate_tokens tests
    
    - Tokenizer now handles punctuation correctly
    - All 14 validate_tokens tests pass

Git History Should Tell a Story
===============================

A good git history for a feature should read like a **narrative**:

.. code-block:: text

    commit abc1234
    Author: Developer
    Date:   2025-01-28
    
        Remove xfail from LLM CLI tests - all passing
    
    commit def5678
    Author: Developer
    Date:   2025-01-28
    
        Integrate compute module into CLIs
    
    commit ghi9012
    Author: Developer
    Date:   2025-01-28
    
        Implement LLMCompute class to pass TDD tests
    
    commit jkl3456
    Author: Developer
    Date:   2025-01-28
    
        Add TDD tests for LLMCompute class (failing)
    
    commit mno7890
    Author: Developer
    Date:   2025-01-28
    
        Add BDD tests for LLM CLIs (xfail - compute missing)

This tells the **complete story** of how the feature was developed using BDD-TDD.

Working with AI
==============

When using AI with this Git workflow:

1. **Ask for Commit Messages**
   - "What should my commit message be for this change?"
   - "Should I split this into multiple commits?"

2. **Review Commits Together**
   - "Does this commit follow the BDD-TDD workflow?"
   - "Is this commit message clear and specific?"

3. **Plan the Git History**
   - "What commits should I make for this feature?"
   - "In what order should I make them?"

Example AI Interaction
----------------------

.. code-block:: text

    User: I need to implement the LLM compute module. What commits should I make?
    
    AI: Based on the BDD-TDD workflow, I recommend these commits:
    
    1. "Add BDD tests for LLM CLIs (xfail - compute module missing)"
    2. "Add TDD tests for tokenizer (failing)"
    3. "Implement tokenizer to pass TDD tests"
    4. "Add TDD tests for LLMCompute class (failing)"
    5. "Implement LLMCompute class to pass TDD tests"
    6. "Integrate compute module into CLIs"
    7. "Remove xfail from BDD tests - all passing"
    
    User: How many commits for the tokenizer fix?
    
    AI: For the tokenizer fix specifically:
    1. "Add TDD tests for tokenizer with punctuation (failing)"
    2. "Implement tokenizer to split on punctuation"
    
    That's 2 commits.

See Also
========

- :ref:`bdd_tdd_cycle` - The BDD & TDD development process
- :ref:`bug_handling` - How to handle bugs in this workflow
- :doc:`/AIblog/love_comma_example` - A concrete example
