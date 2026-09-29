.. (C) Albert Mietus -- mostly made by codeAI=mistral-medium-3-5

Project Goals
=============

Purpose
-------

The **DemoLLM** project is a **demonstration-only** implementation of a minimalistic
Language Model (LLM) system. Its **primary purpose** is to:

1. **Educate** - Show how modern generative AI systems work at a fundamental level
2. **Demonstrate** - Provide a tangible, inspectable example of LLM components
3. **Experiment** - Allow exploration of individual LLM components in isolation
4. **Collaborate** - Serve as a shared workspace for human-AI collaboration

.. warning::
    This is **NOT** a production-ready LLM. It is intentionally simplified and
    limited in scope. Do not use this for any real-world applications.

Core Objectives
---------------

1. **Minimalism**
   - Implement the **smallest possible** working LLM
   - Use only **4 base tokens** (I, YOU, LOVE, COMPUTERS) + EOS
   - Support only **3 valid English sentences**:
     - "I love computers"
     - "You love computers"
     - "I love you"

2. **Architectural Completeness**
   - Include **all major LLM components** in minimal form:
     - Tokenizer (word-level, tokens = words)
     - Model weights (hardcoded transition matrix)
     - Inference loop (generation)
     - Caching mechanisms (future)
   - Components must be **separable** and **inspectable**

3. **Engineering Excellence**
   - Follow **strict TDD** (Test-Driven Development)
   - Apply **SOLID principles** rigorously
   - Use **Uncle Bob's clean code** standards
   - Maintain **100% test coverage** for all implemented features

4. **Documentation**
   - All code must be **fully documented** using Sphinx/rst
   - Include **plantUML diagrams** for architecture
   - Document **all design decisions** using ADR (Architecture Decision Records)
   - Maintain **project documentation** for progress tracking

5. **Extensibility**
   - Design must allow for **future expansion**:
     - More tokens
     - More complex models
     - Additional features (caching, attention, etc.)
   - **No hardcoding** of demo-specific logic in core classes

6. **Dual-Licensing**
   - Use **EUPL v1.2** for European public sector alignment
   - Use **BSD 3-Clause** for commercial integration
   - Support **European digital sovereignty**

Non-Objectives
--------------

The following are **explicitly NOT goals** of this project:

- Creating a **useful** LLM for any real purpose
- Training models from data
- Supporting large vocabularies
- Optimizing for performance
- Creating a production-ready system
- Supporting non-English languages (for now)

Success Criteria
---------------

The project is considered successful when:

✅ All core LLM components are implemented and working
✅ All code is tested with TDD (tests written first)
✅ All code is documented in Sphinx/rst format
✅ Documentation is published on ReadTheDocs
✅ Human and AI collaborators can work together without repetition
✅ All agreements and decisions are documented and accessible

.. todo::
    - Implement tokenizer module
    - Implement inference loop
    - Add caching mechanism
    - Add plantUML diagrams
    - Expand to support more sentences
