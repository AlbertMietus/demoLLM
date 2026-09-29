# DemoLLM

A minimalistic LLM implementation for demonstration purposes.

## Overview

DemoLLM is a very small, demo-only Language Model written in pure Python. It is designed to be readable and demonstrate how generative AI works. All code is written with TDD (using pytest) and follows modern software engineering principles like SOLID.

## Features

- Minimal LLM model with hardcoded weights
- Supports 5 tokens: I, YOU, LOVE, COMPUTERS, EOS
- Can generate simple English sentences:
  - "I love computers"
  - "You love computers"
  - "I love you"
- Fully tested with TDD
- Documented with Sphinx

## Project Structure

```
demoLLM/
├── src/
│   └── demo_llm/
│       ├── __init__.py
│       └── model.py      # LLM class and factory function
├── tests/
│   └── test_001_llm_model.py  # TDD tests
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── adr/
│   │   └── adr_001_llm_model_design.rst
│   └── modules.rst
├── pyproject.toml
└── README.md
```

## Installation

```bash
pip install -e .
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Building Documentation

```bash
cd docs
make html
```

## Architecture

The LLM model is implemented as a simple dataclass with:
- Token to ID mapping
- ID to token mapping
- Weights matrix (transition probabilities)

See the [ADRs](docs/adr/index.rst) for detailed design decisions.

## License

MIT
