# SourceStory — TODO / Development Plan

A phased task list for building SourceStory from the ground up.
Check off items as they are completed.

---

## Phase 0 — Repository Setup ✅

- [x] Initialise repository with README, LICENSE, and `.gitignore`
- [x] Define system architecture (`doc/architecture.md`)
- [x] Define technology stack and ADRs (`doc/technology-stack.md`)
- [x] Create this TODO plan

---

## Phase 1 — Project Scaffolding

- [ ] Create `pyproject.toml` with project metadata, dependencies, and entry point
- [ ] Create the `sourcestory/` Python package skeleton (`__init__.py`, `cli.py`)
- [ ] Set up `tests/` directory with a basic `conftest.py`
- [ ] Configure **Ruff** for linting and formatting (add `ruff.toml` or `[tool.ruff]` in `pyproject.toml`)
- [ ] Configure **mypy** for type checking
- [ ] Add **pre-commit** config (`.pre-commit-config.yaml`)
- [ ] Add GitHub Actions CI workflow (`.github/workflows/ci.yml`)
  - Lint (ruff)
  - Type-check (mypy)
  - Tests (pytest with coverage gate ≥ 80 %)

---

## Phase 2 — Ingestion Layer

- [ ] Implement `SourceFile` dataclass (path, language, content, metadata)
- [ ] Implement `FileReader` — read single file or directory tree
- [ ] Implement `GitReader` — shallow-clone a remote Git repo and ingest files
- [ ] Add language auto-detection from file extension
- [ ] Write unit tests for ingestion layer (mock filesystem + git)

---

## Phase 3 — Chunking & Parsing Layer

- [ ] Integrate **tree-sitter** with pre-built language grammars
- [ ] Implement `ASTChunker` — split files into function/class-level chunks
- [ ] Implement line-based fallback `PlainChunker` for unsupported languages
- [ ] Implement `TokenCounter` utility (use model tokeniser or tiktoken proxy)
- [ ] Ensure chunks include provenance metadata (file, start/end line, symbol name)
- [ ] Write unit tests for chunking (Python and JS fixtures)

---

## Phase 4 — LLM Inference Layer

- [ ] Define `LLMBackend` abstract base class (interface contract)
- [ ] Implement `OllamaBackend` (default) using the `ollama` Python client
- [ ] Implement `LlamaCppBackend` using `llama-cpp-python` (optional dep)
- [ ] Implement `HuggingFaceBackend` using `transformers` + `torch` (optional dep)
- [ ] Add backend auto-selection logic (detect installed runtime)
- [ ] Implement streaming response support with Rich live display
- [ ] Write unit tests for backends (mock HTTP responses / model calls)

---

## Phase 5 — Prompt Templates

- [ ] Create `sourcestory/templates/` directory
- [ ] Write `book_chapter.j2` — formal prose, section headings, code callouts
- [ ] Write `podcast.j2` — two-host dialogue script, conversational tone
- [ ] Write `summary.j2` — high-level bullet-point overview
- [ ] Write `readme.j2` — drop-in README.md generation
- [ ] Unit-test template rendering with mock chunk data

---

## Phase 6 — Formatter / Output Layer

- [ ] Implement `Renderer` — merge LLM responses into a `NarrativeDocument`
- [ ] Support Markdown output (default)
- [ ] Support optional HTML/PDF output via **pandoc** (graceful fallback if not installed)
- [ ] Write unit tests for renderer

---

## Phase 7 — CLI

- [ ] Implement `cli.py` using **Typer**
- [ ] Core command: `sourcestory generate <source> --format <fmt> --model <model> --output <file>`
- [ ] Add `--backend` flag (ollama | llamacpp | hf)
- [ ] Add `--language` flag for stdin input
- [ ] Add `--list-formats` and `--list-models` helper commands
- [ ] Add Rich progress bar and streaming output
- [ ] Write integration tests for CLI (invoke via `typer.testing.CliRunner`)

---

## Phase 8 — Examples & Documentation

- [ ] Add `examples/` directory with sample input files (Python, Go, Rust)
- [ ] Generate and commit example output files (book chapter, podcast, summary)
- [ ] Expand `README.md` with installation, quick-start, and usage guide
- [ ] Add `CONTRIBUTING.md` with development workflow instructions
- [ ] Add `CHANGELOG.md`

---

## Phase 9 — Packaging & Release

- [ ] Ensure `pyproject.toml` is complete and PEP 517 compliant
- [ ] Publish to **PyPI** (`pip install sourcestory`)
- [ ] Add GitHub Actions release workflow (tag → build → publish)
- [ ] Create GitHub Release with changelog notes

---

## Backlog / Nice-to-Have

- [ ] VS Code extension for right-click → "Explain with SourceStory"
- [ ] Support for multi-file cross-reference analysis (call graph context)
- [ ] Interactive mode — Q&A about the code after initial narrative generation
- [ ] Web UI (Gradio or Streamlit) for non-CLI users
- [ ] Docker image for zero-install usage
- [ ] Benchmark suite — evaluate narrative quality across models
