# SourceStory — Technology Stack

## Language & Runtime

| Concern          | Choice              | Rationale                                                  |
|------------------|---------------------|------------------------------------------------------------|
| Primary language | **Python 3.11+**    | Rich ML ecosystem, widespread developer familiarity        |
| Package manager  | **pip / pyproject** | Standard; no extra toolchain required                      |
| Optional extras  | `uv` for fast installs | Drop-in pip replacement for CI speed                   |

---

## Core Dependencies

### CLI

| Library   | Version | Purpose                                      |
|-----------|---------|----------------------------------------------|
| **Typer** | ≥ 0.12  | Modern, typed CLI builder on top of Click    |
| **Rich**  | ≥ 13    | Terminal output — progress bars, syntax highlighting, streaming text |

### Source Parsing

| Library            | Version | Purpose                                         |
|--------------------|---------|-------------------------------------------------|
| **tree-sitter**    | ≥ 0.22  | Language-agnostic AST parsing                   |
| **tree-sitter-languages** | ≥ 1.10 | Pre-built grammars (Python, JS, TS, Go, Rust, C, Java) |
| **gitpython**      | ≥ 3.1.33 | Clone remote Git repositories as input sources  |

### LLM Inference

| Library                   | Version | Purpose                                      |
|---------------------------|---------|----------------------------------------------|
| **ollama**                | ≥ 0.2   | Python client for the Ollama local server (default backend) |
| **llama-cpp-python**      | ≥ 0.2   | Direct GGUF model loading (optional backend) |
| **transformers** (HuggingFace) | ≥ 4.40 | GPU path via HF Hub models (optional backend) |
| **torch**                 | ≥ 2.2   | Required only with HuggingFace backend       |

### Templating & Output

| Library    | Version | Purpose                                         |
|------------|---------|-------------------------------------------------|
| **Jinja2** | ≥ 3.1   | Prompt templates and output document rendering  |

### Testing

| Library          | Version | Purpose                              |
|------------------|---------|--------------------------------------|
| **pytest**       | ≥ 8     | Test runner                          |
| **pytest-cov**   | ≥ 5     | Coverage reporting                   |
| **responses**    | ≥ 0.25  | HTTP mocking for Ollama backend tests |

### Optional / Dev

| Library          | Purpose                                           |
|------------------|---------------------------------------------------|
| **ruff**         | Linter + formatter (replaces flake8 + black)      |
| **mypy**         | Static type checking                              |
| **pre-commit**   | Git hooks for linting before commit               |
| **pandoc** (system) | Markdown → HTML / PDF conversion (opt-in)    |

---

## Supported LLM Models

The following open-source models have been evaluated as good fits for code explanation:

| Model             | Size    | Backend     | Notes                                       |
|-------------------|---------|-------------|---------------------------------------------|
| **Mistral 7B**    | ~4 GB   | Ollama / llama.cpp | Strong instruction-following, fast on CPU |
| **Llama 3 8B**    | ~5 GB   | Ollama / llama.cpp | Meta's latest, excellent code context       |
| **CodeLlama 13B** | ~8 GB   | Ollama / llama.cpp | Fine-tuned on code; best for detailed explanations |
| **DeepSeek-Coder 6.7B** | ~4 GB | Ollama  | Specialised code understanding model        |
| **Phi-3 Mini**    | ~2 GB   | Ollama / llama.cpp | Fits comfortably in low-RAM environments   |

Default model shipped with the tool: **Mistral 7B Instruct** (via Ollama tag `mistral`).

---

## Supported Input Languages

Tree-sitter grammars are available for all of the following, giving SourceStory
AST-level code understanding:

- Python
- JavaScript / TypeScript
- Go
- Rust
- C / C++
- Java
- Ruby (partial)

Plain-text / line-based fallback is used for all other languages.

---

## Infrastructure & CI

| Concern         | Choice             | Notes                                          |
|-----------------|--------------------|------------------------------------------------|
| CI              | **GitHub Actions** | Lint, type-check, and unit-test on every push  |
| Python versions | 3.11, 3.12         | Tested matrix                                  |
| OS matrix       | ubuntu-latest, macos-latest | Cover Linux dev + Mac dev environments |
| Coverage gate   | ≥ 80 %             | Enforced via `pytest-cov` + `--cov-fail-under` |

---

## Architecture Decision Records (ADR)

### ADR-001: Ollama as the Default LLM Backend

**Decision:** Ollama is the out-of-the-box LLM runtime.  
**Rationale:** Single `ollama pull <model>` command for setup; exposes a simple REST
API; actively maintained; runs on CPU without CUDA drivers.  
**Trade-off:** Requires a separate daemon process. Power users can opt out in favour
of `llama-cpp-python` for a pure-Python experience.

### ADR-002: Tree-sitter for Parsing

**Decision:** Use Tree-sitter rather than language-specific parsers.  
**Rationale:** One dependency covers all target languages; bindings are mature in
Python; incremental parsing is fast enough for files up to ~10 k lines.  
**Trade-off:** Grammar packages add ~30 MB to the install; fallback to line splitting
is needed for unsupported languages.

### ADR-003: Jinja2 for Prompt Templates

**Decision:** Store prompt templates as `.j2` files, rendered at runtime by Jinja2.  
**Rationale:** Separates prompt engineering from Python logic; allows non-developers
to customise prompts without touching code; easy to unit-test templates in isolation.  
**Trade-off:** Adds a templating dependency; templates must be shipped with the package.

### ADR-004: Markdown as Primary Output Format

**Decision:** All output documents are Markdown by default.  
**Rationale:** Universal format readable in terminals, GitHub, IDEs, and can be
converted to HTML/PDF via pandoc as an optional step.  
**Trade-off:** Rich formatting (tables, diagrams) is limited without conversion.
