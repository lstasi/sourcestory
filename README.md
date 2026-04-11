# SourceStory

> Turning complex source code into engaging narratives.

SourceStory is a **local-first**, privacy-respecting Python tool that reads
source code and generates human-readable documentation using open-source LLMs.
Your code never leaves your machine.

## ✨ Features

- **Multiple output formats** — book chapters, podcast scripts, bullet-point
  summaries, and drop-in READMEs.
- **Pluggable LLM backends** — Ollama (default), llama.cpp, or HuggingFace
  Transformers.
- **AST-aware chunking** — uses Tree-sitter to split code into meaningful
  segments that fit within the model's context window.
- **Rich terminal UX** — progress bars, syntax highlighting, and streaming
  output powered by Rich.

## 📦 Installation

```bash
pip install sourcestory
```

Or install from source for development:

```bash
git clone https://github.com/lstasi/sourcestory.git
cd sourcestory
pip install -e ".[dev]"
```

### Prerequisites

- **Python 3.11+**
- **Ollama** (default backend) — install from [ollama.com](https://ollama.com)
  and pull a model:
  ```bash
  ollama pull mistral
  ```

## 🚀 Quick Start

```bash
# Generate a book-chapter narrative from a Python file
sourcestory generate my_project/main.py

# Generate a podcast script from a directory
sourcestory generate ./src --format podcast

# Use a different model
sourcestory generate app.py --model llama3

# List available formats and backends
sourcestory list-formats
sourcestory list-backends
```

## 🏗️ Architecture

SourceStory is a four-stage pipeline:

```
Ingestion → Chunking & Parsing → LLM Inference → Formatter / Output
```

See [`doc/architecture.md`](doc/architecture.md) for the full system design and
[`doc/technology-stack.md`](doc/technology-stack.md) for dependency decisions.

## 🧑‍💻 Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Run formatter
ruff format .

# Run type checker
mypy sourcestory/

# Run tests with coverage
pytest --cov=sourcestory --cov-report=term-missing

# Install pre-commit hooks
pre-commit install
```

## 🗺️ Roadmap

See [`TODO.md`](TODO.md) for the full phased development plan.

## 📄 License

[MIT](LICENSE)
