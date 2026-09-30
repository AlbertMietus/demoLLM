.. _bdd_tdd_cycle:

===================================
BDD & TDD Cycle: The Workflow
===================================

:Author: Albert Mietus (with AI assistance)
:Version: 1.0
:Date: 2025-01-28
:Status: Draft

.. note::
    This document describes the **interwoven process** of Behavior-Driven Development (BDD) and
    Test-Driven Development (TDD) as practiced in professional software engineering.
    It is based on the principles outlined in the MESS framework by Albert Mietus.

.. toctree::
    :maxdepth: 2
    :caption: Contents

Introduction
============

Behavior & Test Driven Development (B&TDD) are **not competing methodologies** but **complementary disciplines**
that work together at different levels of the software development process. BDD operates at the
**system/acceptance level** (what the system should do), while TDD operates at the **unit/module level**
(how the code achieves that behavior).

The key insight from the MESS framework is that **BDD and TDD must be interwoven** with the typical
steps in a development process, and they **change the order** of traditional development.

.. admonition:: Core Principle

    **Write tests first, code second.** This applies to both BDD and TDD.
    The tests define the requirements; the code satisfies them.

References
=========

This workflow is based on the following authoritative sources:

1. `Introducing BDD & TDD <https://mess.softwarebetermaken.nl/en/latest/SoftwareCompetence/LeanEngineering/BDD_TDD/01.introducingB+TDD.html>`_
2. `Applying BDD & TDD in Legacy <https://mess.softwarebetermaken.nl/en/latest/SoftwareCompetence/LeanEngineering/BDD_TDD/02.applyingBTDD_inLegacy.html>`_
3. `LinkedIn: Introducing BDD & TDD <https://www.linkedin.com/pulse/introducing-bdd-tdd-albert-mietus/>`_
4. `LinkedIn: Applying BDD & TDD in Legacy <https://www.linkedin.com/pulse/applying-bdd-tdd-legacy-albert-mietus/>`_

The Process: Step by Step
==========================

The BDD-TDD cycle follows a **top-down, outside-in** approach:

1. **BDD Phase: Define Behavior (System Level)**
2. **TDD Phase: Implement Components (Unit Level)**
3. **Integration Phase: Connect Components (Module Level)**
4. **Verification Phase: Validate System (Acceptance Level)**

.. _bdd-phase:

Phase 1: BDD - Define Behavior
------------------------------

**Purpose:** Define **what** the system should do at the highest level.

**Activities:**

1. **Create CLI/Executable Specifications**
   - Write small CLI scripts that demonstrate the desired behavior
   - These are the **entry points** for the system
   - Example: ``demoLLM_validate_tokens.py``, ``demoLLM_find_first_sentence.py``

2. **Write BDD Tests (xfail)**
   - Create pytest tests that call the CLIs with various inputs
   - **Mark them as xfail** with a reason explaining what's missing
   - Example: ``@pytest.mark.xfail(reason="tokenizer module not implemented")``

3. **Define Acceptance Criteria**
   - Each BDD test represents an acceptance criterion
   - The tests should cover the **happy path** and **edge cases**

**Key Question:** *What should the system do?*

**Output:** A set of failing BDD tests that define the system's expected behavior.

.. code-block:: python

    # Example: BDD test for CLI (marked as xfail)
    import pytest
    import subprocess

    @pytest.mark.xfail(reason="rekenmodule (compute) not implemented")
    def test_given_input_with_punctuation_when_validate_then_exits_with_1():
        """
        Given: Input containing punctuation
        When: demoLLM_validate_tokens CLI is run
        Then: Exit code is 1 (invalid)
        """
        result = subprocess.run(
            ["python", "-m", "demo_llm.cli.demoLLM_validate_tokens"],
            input="I love, computers",
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

.. _tdd-phase:

Phase 2: TDD - Implement Components
-------------------------------

**Purpose:** Define **how** the system achieves the behavior, one component at a time.

**Activities:**

1. **Analyze BDD Failures**
   - Look at which BDD tests are failing and why
   - Identify the **missing components** (modules, classes, functions)

2. **Write TDD Tests (failing)**
   - For each missing component, write unit tests **first**
   - These tests should **fail** initially (Red phase)
   - Example: Tokenizer tests, Compute module tests

3. **Implement Components**
   - Write the **minimal code** to make the TDD tests pass (Green phase)
   - Refactor as needed (Refactor phase)

**Key Question:** *How should this component work to satisfy the BDD tests?*

**Output:** Working components with passing TDD tests.

.. code-block:: python

    # Example: TDD test for tokenizer
    def test_given_word_with_trailing_comma_when_tokenize_then_returns_unknown():
        """
        Given: Word "love,"
        When: tokenize_word is called
        Then: Returns PSEUDO_UNKNOWN (word with punctuation is invalid)
        """
        from demo_llm.compute import tokenize_word
        from demo_llm.tokens import PSEUDO_UNKNOWN
        
        result = tokenize_word("love,")
        
        assert result == PSEUDO_UNKNOWN

.. _integration-phase:

Phase 3: Integration - Connect Components
----------------------------------------

**Purpose:** Connect the TDD-implemented components to satisfy the BDD tests.

**Activities:**

1. **Integrate Components**
   - Use the TDD-tested components in the CLI scripts
   - Ensure the CLIs call the correct modules

2. **Update BDD Tests**
   - Remove ``xfail`` markers as components are integrated
   - Verify BDD tests now pass

**Key Question:** *Are all components working together correctly?*

**Output:** Working CLIs with passing BDD tests.

.. _verification-phase:

Phase 4: Verification - Validate System
---------------------------------------

**Purpose:** Ensure the complete system works as specified.

**Activities:**

1. **Run All Tests**
   - Execute both BDD and TDD tests
   - All tests should pass

2. **Manual Verification**
   - Test the CLIs manually with various inputs
   - Verify edge cases

**Key Question:** *Does the system meet all acceptance criteria?*

**Output:** A fully tested, working system.

Practical Example: The DemoLLM Workflow
=======================================

Let's trace through how this would work for the DemoLLM project:

1. **BDD Phase:**
   - Create CLI stubs: ``demoLLM_find_first_sentence.py``, ``demoLLM_validate_tokens.py``
   - Write BDD tests with xfail markers
   - Git commit: ``"Add BDD tests for LLM CLIs (xfail - rekenmodule missing)"``

2. **TDD Phase:**
   - Analyze: BDD tests fail because tokenizer and compute module are missing
   - Write TDD tests for ``tokenize_word()`` function
   - Implement ``tokenize_word()`` to pass tests
   - Write TDD tests for ``LLMCompute`` class
   - Implement ``LLMCompute`` class to pass tests
   - Git commits for each component

3. **Integration Phase:**
   - Update CLIs to use ``LLMCompute`` and ``tokenize_word()``
   - Remove xfail markers from BDD tests
   - Git commit: ``"Integrate compute module into CLIs"``

4. **Verification Phase:**
   - Run all tests (BDD + TDD)
   - All pass
   - Git commit: ``"All tests passing - rekenmodule complete"``

Key Principles
==============

1. **Tests First, Always**
   - Never write production code without a failing test first
   - Tests define the requirements

2. **Small, Frequent Commits**
   - Each commit should be a small, testable step
   - Git history should tell the story of development

3. **Fail Fast, Fix Fast**
   - If a test fails, fix it immediately
   - Don't let failing tests accumulate

4. **Refactor Mercilessly**
   - Once tests pass, improve the code
   - Tests provide the safety net for refactoring

5. **All Levels Matter**
   - BDD for system behavior
   - TDD for component implementation
   - Both are essential

Common Pitfalls
===============

1. **Skipping BDD**
   - Starting with TDD without BDD leads to components that don't work together
   - **Solution:** Always start with at least one BDD test

2. **Overly Complex BDD Tests**
   - BDD tests should be high-level, not implementation details
   - **Solution:** Keep BDD tests simple and behavioral

3. **TDD Without Refactoring**
   - TDD without refactoring leads to messy code
   - **Solution:** Follow Red-Green-Refactor cycle strictly

4. **Ignoring Failing Tests**
   - Letting tests fail for days/weeks defeats the purpose
   - **Solution:** Fix failing tests immediately

5. **Testing Implementation Instead of Behavior**
   - Tests should verify behavior, not implementation
   - **Solution:** Write tests from the user's perspective

For AI Assistance
================

When working with AI coding assistants:

1. **Provide Context**
   - Explain the BDD requirements first
   - Show the failing tests
   - Then ask for implementation help

2. **Demand Tests First**
   - Always ask: "What tests should I write first?"
   - Never accept code without tests

3. **Verify Understanding**
   - Ask the AI to explain the requirements in its own words
   - Confirm the BDD-TDD cycle is understood

4. **Review Together**
   - Use the AI to review code and tests
   - Ask: "What edge cases are missing from these tests?"

Example AI Prompt
----------------

.. code-block:: text

    Context: I'm implementing an LLM compute module. The BDD tests show that
    "I love, computers" should be treated as containing invalid tokens.
    
    Current situation:
    - BDD test: echo "I love, computers" | demoLLM_validate_tokens.py
    - Expected: exit code 1 (invalid)
    - Current: exit code 0 (all tokens valid)
    
    Question: What TDD tests should I write for the tokenizer to fix this?
    
    AI Response:
    You should write these TDD tests first:
    1. test_tokenize_word("love,") should return PSEUDO_UNKNOWN (or [LOVE, PSEUDO_PUNCTUATION])
    2. test_tokenize_word(",") should return PSEUDO_PUNCTUATION
    3. test_tokenize_word("I") should return I
    
    Then implement the tokenizer to pass these tests.

See Also
========

- :ref:`git_workflow` - How BDD/TDD integrates with Git
- :ref:`bug_handling` - How to handle bugs in a BDD/TDD workflow
- :doc:`/AIblog/love_comma_example` - A concrete example of this workflow in action
