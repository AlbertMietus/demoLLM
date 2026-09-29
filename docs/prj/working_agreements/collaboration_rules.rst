.. (C) Albert Mietus -- mostly made by codeAI=mistral-medium-3-5

Collaboration Rules
==================

General Principles
------------------

1. **No Guessing**
   - AI **must never guess** what the human wants
   - If anything is unclear, **ask explicitly**
   - Human **must clarify** until AI understands completely

2. **Human Sets Pace**
   - Human **controls the tempo** of work
   - AI **follows** the human's lead
   - AI **never proceeds** without explicit human approval when in doubt

3. **Explicit Confirmation Required**
   - For any **significant decision** (architecture, design, scope)
   - For any **change** to existing agreements
   - Before **pushing to remote** (except for trivial fixes)

4. **Document Everything**
   - All agreements **must** be documented in this section
   - All decisions **must** have an ADR if architectural
   - All progress **must** be tracked in /docs/prj/progress/

Communication
-------------

1. **Language**
   - **Primary**: English (for all documentation and code)
   - **Secondary**: Dutch (allowed in chat for clarification only)
   - All **written documentation** must be in English

2. **Clarity Over Brevity**
   - Be **explicit** rather than concise when clarity is at stake
   - Use **full sentences** in documentation
   - Avoid **ambiguity** at all costs

3. **Question Format**
   - AI must **number questions** when asking multiple
   - AI must **quote** the unclear statement when asking for clarification
   - Human must **answer all parts** of multi-part questions

4. **Status Updates**
   - AI must provide **clear status updates** at logical milestones
   - Use **todo lists** for multi-step tasks
   - Mark items as **completed** only when actually finished

Development Process
-------------------

1. **TDD (Test-Driven Development)**
   - **Always** write tests **before** implementation
   - Tests must use **pseudo-BDD naming**: ``test_<nr>_given_when_then``
   - Tests must be **numbered sequentially** per file (test-001, test-002, etc.)
   - All tests **must pass** before considering a feature complete

2. **Code Quality**
   - Follow **SOLID principles** strictly
   - Follow **Uncle Bob's clean code** standards
   - **No comments** in code (code must be self-documenting)
   - **No magic numbers** (use named constants)
   - **Type hints** required for all Python functions

3. **Documentation**
   - All **modules, classes, and functions** must have docstrings
   - Use **Sphinx/rst format** for all documentation
   - Use **Google-style** docstrings for Python code
   - Include **examples** in docstrings where helpful

4. **File Headers**
   - **Every file** must start with copyright header:
     ``(C) Albert Mietus -- mostly made by codeAI=<model>``
   - AI must **include its model name and version** in the header

5. **Version Control**
   - Use **atomic commits** (one logical change per commit)
   - Write **descriptive commit messages**
   - Include **what** was changed and **why**
   - **Never** commit generated files (except documentation build artifacts)

6. **Branch Strategy**
   - **Main branch** is always **stable**
   - Use **feature branches** for new functionality
   - Use **vibe/<slug>** prefix for AI-created branches
   - **Merge via PR** with explicit human approval

Engineering Standards
--------------------

1. **Naming Conventions**
   - Python: **snake_case** for variables/functions
   - Python: **PascalCase** for classes
   - Python: **UPPER_CASE** for constants
   - Files: **snake_case** with ``_`` separator
   - Tests: **test_<nr>_<description>** format

2. **Error Handling**
   - **No silent failures** (always raise or log)
   - Use **custom exceptions** for domain-specific errors
   - Include **context** in error messages

3. **Testing**
   - **100% coverage** for all implemented features
   - Test **edge cases** explicitly
   - Use **pytest** as test framework
   - Include **happy path** and **error path** tests

4. **Dependencies**
   - **Minimize** external dependencies
   - **Pin versions** in pyproject.toml
   - **Document** why each dependency is needed

Documentation Standards
-----------------------

1. **Structure**
   - Use **rst format** (not markdown) for Sphinx
   - One **sentence per line** for readability
   - Use **proper nesting** for headings (====, ----, ~~~~, ^^^^)

2. **ADR (Architecture Decision Records)**
   - Create ADR for **every architectural decision**
   - Use **standard ADR template**
   - Include **context, decision, rationale, consequences**
   - Number ADRs **sequentially** (adr_001, adr_002, etc.)

3. **Project Documentation**
   - Track **all progress** in /docs/prj/progress/
   - Document **test results** in /docs/prj/tests/
   - Document **design notes** in /docs/prj/design/
   - Use **.. todo::** for future work

4. **API Documentation**
   - Use **autodoc** for Python code
   - Document **all public interfaces**
   - Include **examples** where helpful

Project-Specific Agreements
---------------------------

1. **Token Definition**
   - Base tokens: **I, YOU, LOVE, COMPUTERS** (IDs 1-4)
   - Special token: **EOS** (End Of Sentence, ID 0)
   - Tokens are **both words and tokens** (simplification for demo)
   - Token IDs: **0-4** (reserved, do not use others without discussion)

2. **Model Structure**
   - Use **transition matrix** (n x n) for weights
   - Weights are **percentages (0-100)**
   - Matrix represents **first-order Markov chain**
   - **No neural networks** (too complex for demo)

3. **Sentence Support**
   - Must support: "I love computers"
   - Must support: "You love computers"
   - Must support: "I love you"
   - **No other sentences** required (for now)

4. **File Structure**
   - Source code: **src/demo_llm/**
   - Tests: **tests/**
   - Documentation: **docs/**
   - Project docs: **docs/prj/**
   - Objectives: **docs/doel/**

5. **External Services**
   - Documentation: **ReadTheDocs.org** (publicly accessible)
   - **Never** make sandbox resources publicly reachable
   - **Never** expose secrets or credentials

Violation Handling
------------------

1. **AI Violations**
   - If AI violates these rules, human **must correct**
   - AI must **acknowledge** the violation
   - AI must **explain** how it will prevent recurrence

2. **Human Violations**
   - If human violates these rules, AI **must point out**
   - AI must **suggest** the correct approach
   - AI must **not proceed** until corrected

3. **Dispute Resolution**
   - If disagreement occurs, **stop work** immediately
   - Human has **final decision** authority
   - Document the **resolution** in working agreements

.. todo::
    - Add plantUML diagram for architecture
    - Add contribution guidelines
    - Add code review checklist
