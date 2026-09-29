# DemoLLM - Agent Guidelines

<!-- (C) Albert Mietus -- mostly made by codeAI=mistral-medium-3-5 -->

## Purpose

This file serves as a **quick reference** for AI agents (and human collaborators) working on the DemoLLM project. It points to the authoritative documentation files that contain all agreements, objectives, and standards.

.. note::
    **ALWAYS CHECK THE RST FILES IN /docs/ FOR THE MOST CURRENT AND COMPLETE INFORMATION.**
    This file is a pointer, not the source of truth.

---

## 📚 Documentation Structure Overview

The DemoLLM project uses a **strict separation** between different types of documentation:

```
demoLLM/
├── AGENTS.md                    # This file - quick reference for agents
├── LICENSE                     # Dual-license (EUPL v1.2 + BSD 3-Clause)
├── README.md                   # Project overview (for external readers)
├── pyproject.toml              # Project configuration
├── .readthedocs.yaml           # ReadTheDocs configuration
├── src/
│   └── demo_llm/               # Source code (see modules.rst for API docs)
├── tests/                      # Test files (see test documentation)
└── docs/
    ├── index.rst               # Main documentation entry point
    ├── conf.py                 # Sphinx configuration
    ├── Makefile                # Documentation build file
    ├── requirements.txt        # Documentation dependencies
    │
    ├── doel/                   # **PRODUCT DOCUMENTATION** - What we build
    │   ├── index.rst
    │   └── project_goals.rst   # ✅ Authoritative: Project objectives, scope, success criteria
    │
    ├── adr/                    # **PRODUCT DOCUMENTATION** - Architecture decisions
    │   ├── index.rst
    │   └── adr_001_llm_model_design.rst  # ✅ Authoritative: Model design decisions
    │
    ├── modules.rst             # **PRODUCT DOCUMENTATION** - API documentation
    ├── demo_llm.rst            # Auto-generated from source code
    └── demo_llm.model.rst      # Auto-generated from model.py
    │
    └── prj/                    # **PROJECT DOCUMENTATION** - How we work
        ├── index.rst
        │
        ├── tests/              # Test results and coverage
        │   ├── index.rst
        │   └── test_001_llm_model.rst
        │
        ├── progress/           # Progress tracking
        │   ├── index.rst
        │   └── progress_2026_09_29.rst
        │
        ├── design/             # Design notes (future)
        │   └── index.rst
        │
        └── working_agreements/  # ✅ Authoritative: Collaboration rules
            ├── index.rst
            └── collaboration_rules.rst
```

---

## 🎯 What Goes Where

### Product Documentation (`/docs/doel/`, `/docs/adr/`, `/docs/modules.rst`)

**Purpose**: Describes **WHAT** we are building and **WHY**.

**Contains**:
- Project goals and objectives
- Scope and non-goals
- Architecture decisions (ADRs)
- API documentation (auto-generated from code)
- Technical specifications
- Design patterns and principles

**Audience**:
- End users of the library
- Developers who want to understand the system
- Anyone who needs to know **what** DemoLLM does

**Authoritative Files**:
- [`docs/doel/project_goals.rst`](docs/doel/project_goals.rst) - **MUST READ** for understanding project purpose
- [`docs/adr/adr_001_llm_model_design.rst`](docs/adr/adr_001_llm_model_design.rst) - **MUST READ** for understanding model architecture
- [`docs/modules.rst`](docs/modules.rst) - API documentation index

---

### Project Documentation (`/docs/prj/`)

**Purpose**: Describes **HOW** we work together and **WHAT** we have done.

**Contains**:
- Working agreements and collaboration rules
- Progress tracking and status updates
- Test results and coverage reports
- Design notes and brainstorming
- Meeting notes (if applicable)

**Audience**:
- Project collaborators (human and AI)
- Anyone who needs to know **how** we work
- Anyone tracking project progress

**Authoritative Files**:
- [`docs/prj/working_agreements/collaboration_rules.rst`](docs/prj/working_agreements/collaboration_rules.rst) - **MUST READ** for all collaborators
- [`docs/prj/progress/progress_2026_09_29.rst`](docs/prj/progress/progress_2026_09_29.rst) - Current project status
- [`docs/prj/tests/test_001_llm_model.rst`](docs/prj/tests/test_001_llm_model.rst) - Test results

---

## ✅ Quick Reference for Agents

### Before Starting Any Work

1. **Read the objectives**: [`docs/doel/project_goals.rst`](docs/doel/project_goals.rst)
   - Understand what DemoLLM is and is NOT
   - Know the scope and constraints

2. **Read the working agreements**: [`docs/prj/working_agreements/collaboration_rules.rst`](docs/prj/working_agreements/collaboration_rules.rst)
   - Follow all rules strictly
   - **NEVER GUESS** - always ask for clarification

3. **Check current progress**: [`docs/prj/progress/`](docs/prj/progress/)
   - See what has been done
   - See what is planned

### During Work

- **For architectural decisions**: Check [`docs/adr/`](docs/adr/) first
- **For implementation details**: Check [`docs/modules.rst`](docs/modules.rst) (API docs)
- **For testing requirements**: Check [`docs/prj/tests/`](docs/prj/tests/)
- **When in doubt**: Ask and reference the relevant documentation file

### After Completing Work

- **Update progress**: Add entry to [`docs/prj/progress/`](docs/prj/progress/)
- **Update tests**: Add test results to [`docs/prj/tests/`](docs/prj/tests/)
- **Document decisions**: Create ADR in [`docs/adr/`](docs/adr/) if architectural

---

## 🔍 Documentation Hierarchy (What to Read First)

```
1. AGENTS.md (this file) → Quick reference
   │
   ├── 2. docs/doel/project_goals.rst → WHAT we build
   │       │
   │       ├── Purpose and scope
   │       ├── Core objectives
   │       └── Success criteria
   │
   ├── 3. docs/prj/working_agreements/collaboration_rules.rst → HOW we work
   │       │
   │       ├── General principles
   │       ├── Communication rules
   │       ├── Development process
   │       └── Project-specific agreements
   │
   ├── 4. docs/adr/adr_001_llm_model_design.rst → Architecture decisions
   │
   └── 5. docs/modules.rst → API documentation
```

---

## 📝 Repository Directory Structure

```
demoLLM/
├── AGENTS.md                    # Agent quick reference (THIS FILE)
├── LICENSE                     # Dual-license (EUPL v1.2 + BSD 3-Clause)
├── README.md                   # External project overview
├── pyproject.toml              # Project configuration and dependencies
├── .readthedocs.yaml           # ReadTheDocs build configuration
│
├── src/
│   └── demo_llm/
│       ├── __init__.py         # Package initialization
│       └── model.py            # LLM model implementation
│
├── tests/
│   ├── __init__.py
│   └── test_001_llm_model.py    # TDD tests for LLM model
│
└── docs/
    ├── index.rst               # Main Sphinx documentation entry
    ├── conf.py                 # Sphinx configuration
    ├── Makefile                # Documentation build script
    ├── requirements.txt        # Documentation dependencies
    │
    ├── doel/                   # PRODUCT: Objectives and scope
    │   ├── index.rst
    │   └── project_goals.rst
    │
    ├── adr/                    # PRODUCT: Architecture decisions
    │   ├── index.rst
    │   └── adr_001_llm_model_design.rst
    │
    ├── prj/                    # PROJECT: Working agreements and progress
    │   ├── index.rst
    │   ├── tests/
    │   │   ├── index.rst
    │   │   └── test_001_llm_model.rst
    │   ├── progress/
    │   │   ├── index.rst
    │   │   └── progress_2026_09_29.rst
    │   ├── design/
    │   │   └── index.rst
    │   └── working_agreements/
    │       ├── index.rst
    │       └── collaboration_rules.rst
    │
    └── modules.rst             # PRODUCT: API documentation index
```

---

## ⚠️ Important Notes

1. **All documentation is in English** (as per working agreements)
2. **All files must have copyright header**: `(C) Albert Mietus -- mostly made by codeAI=<model>`
3. **All changes must be documented** in the appropriate location
4. **Never assume** - if it's not in the documentation, ask for clarification
5. **The RST files are the source of truth** - this AGENTS.md is a convenience pointer

---

## 🎯 Summary: What to Remember

| Question | Answer | Where to Find It |
|----------|--------|------------------|
| What are we building? | Minimal LLM demo with 4 tokens | [`docs/doel/project_goals.rst`](docs/doel/project_goals.rst) |
| How do we work together? | TDD, SOLID, no guessing | [`docs/prj/working_agreements/collaboration_rules.rst`](docs/prj/working_agreements/collaboration_rules.rst) |
| What decisions have been made? | Architecture, design choices | [`docs/adr/`](docs/adr/) |
| What has been done? | Progress tracking | [`docs/prj/progress/`](docs/prj/progress/) |
| What tests exist? | Test results | [`docs/prj/tests/`](docs/prj/tests/) |
| What's the API? | Auto-generated docs | [`docs/modules.rst`](docs/modules.rst) |

---

**Last Updated**: 2026-09-29
**Maintainer**: Albert Mietus (with AI assistance)
