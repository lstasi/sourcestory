# SourceStory — System Architecture

## Overview

SourceStory is a pipeline-based Python application. Raw source code enters one end
and human-readable narratives come out the other. The design is intentionally modular
so that each stage can be developed, tested, and swapped independently.

```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐     ┌────────────────┐
│   Ingestion  │────▶│   Chunking &  │────▶│   LLM Inference  │────▶│    Formatter   │
│    Layer     │     │  Parsing Layer│     │      Layer       │     │    / Output    │
└──────────────┘     └───────────────┘     └──────────────────┘     └────────────────┘
       │                    │                       │                        │
  File / stdin         Tree-sitter             Local model             Book Chapter
  Git repo clone       AST walker           (Ollama / llama.cpp)      Podcast Script
  Directory scan       Token counter          Prompt templates         Summary Doc
```

---

## Layers

### 1. Ingestion Layer

**Responsibility:** Accept source code from various input sources and normalise it
into an internal `SourceFile` data model.

| Input Source        | Mechanism                                  |
|---------------------|--------------------------------------------|
| Single file         | `--file` CLI argument / Python API         |
| Directory           | Recursive glob with language filter        |
| Git repository URL  | `gitpython` shallow-clone to `/tmp`        |
| Stdin               | Piped input with explicit `--language` tag |

Outputs a list of `SourceFile(path, language, content, metadata)` objects.

---

### 2. Chunking & Parsing Layer

**Responsibility:** Break large files into semantically meaningful segments so they
fit within the LLM context window.

- Uses **Tree-sitter** to produce an AST for supported languages (Python, JS, TS,
  Go, Rust, C/C++, Java).
- Falls back to line-based splitting for unsupported languages.
- Each chunk carries provenance metadata (file, start_line, end_line, symbol name).
- A `TokenCounter` utility estimates token count using the model's tokeniser and
  splits chunks that exceed the configured `max_tokens` threshold.

---

### 3. LLM Inference Layer

**Responsibility:** Send chunks + prompt templates to an open-source LLM and collect
generated text.

- **Runtime options** (pluggable via an `LLMBackend` abstract class):
  - **Ollama** — default, zero-config local server (`ollama serve`)
  - **llama.cpp** — direct GGUF model file loading via `llama-cpp-python`
  - **HuggingFace Transformers** — GPU-friendly path for larger models
- **Prompt templates** are Jinja2 files stored in `sourcestory/templates/`.
  Each output format has its own template (see Formatter section).
- Responses are streamed when possible to give live feedback to the user.

---

### 4. Formatter / Output Layer

**Responsibility:** Combine generated text segments into the requested output format
and write the result to disk or stdout.

| Format          | Description                                                 |
|-----------------|-------------------------------------------------------------|
| `book_chapter`  | Formal prose, section headings, code callouts               |
| `podcast`       | Two-host dialogue script, conversational tone               |
| `summary`       | High-level bullet-point overview                            |
| `readme`        | Drop-in README.md for the analysed project                  |

Output is rendered via **Jinja2** templates and written as Markdown by default.
An optional `--format html|pdf` flag converts Markdown using **pandoc** (optional dep).

---

## Key Data Flow

```
SourceFile list
  └─▶ ChunkList  (per file, AST-aware)
        └─▶ PromptBatch  (template + chunk + context)
              └─▶ LLMResponse list  (streamed text)
                    └─▶ NarrativeDocument  (merged, formatted)
                          └─▶ Output file / stdout
```

---

## Project Directory Structure (planned)

```
sourcestory/
├── sourcestory/            # Main Python package
│   ├── __init__.py
│   ├── cli.py              # Entry point (Typer)
│   ├── ingestion/          # Ingestion layer
│   │   ├── __init__.py
│   │   ├── file_reader.py
│   │   └── git_reader.py
│   ├── parsing/            # Chunking & parsing layer
│   │   ├── __init__.py
│   │   ├── ast_chunker.py
│   │   └── token_counter.py
│   ├── llm/                # LLM inference layer
│   │   ├── __init__.py
│   │   ├── base.py         # Abstract LLMBackend
│   │   ├── ollama_backend.py
│   │   ├── llamacpp_backend.py
│   │   └── hf_backend.py
│   ├── formatter/          # Output formatting layer
│   │   ├── __init__.py
│   │   └── renderer.py
│   └── templates/          # Jinja2 prompt & output templates
│       ├── book_chapter.j2
│       ├── podcast.j2
│       ├── summary.j2
│       └── readme.j2
├── tests/                  # Pytest test suite
├── doc/                    # Project documentation & analysis
├── examples/               # Sample inputs and generated outputs
├── TODO.md
├── README.md
├── pyproject.toml
└── .gitignore
```

---

## Design Principles

1. **Local-first** — no outbound API calls required; all inference runs on the
   developer's machine.
2. **Privacy by default** — source code never leaves the local environment.
3. **Pluggable backends** — swap LLM runtime without changing any other code.
4. **Streaming UX** — show progress token-by-token so users aren't staring at a
   blank terminal.
5. **Testable in isolation** — each layer can be unit-tested with mocked
   dependencies.
