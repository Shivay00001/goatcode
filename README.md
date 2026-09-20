# GOATCODE

> A Python coding-agent framework for project-aware planning, tool execution, validation, and multi-provider LLM workflows.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Package](https://img.shields.io/badge/package-goatcode-blue)](./setup.py)
[![Status](https://img.shields.io/badge/status-beta-yellow)](https://github.com/Shivay00001/goatcode)
[![Ollama](https://img.shields.io/badge/local%20models-Ollama-black?logo=ollama)](https://ollama.com/)
[![License](https://img.shields.io/badge/license-VisionQuantech%20Custom-orange)](./LICENSE)

GOATCODE is an experimental, tool-augmented coding agent designed to work with an existing project instead of generating isolated snippets. It analyzes project context, creates an implementation plan, invokes registered tools, validates changes, and reports the resulting files and checks.

## What it does

GOATCODE focuses on the engineering loop around code generation:

- **Project context:** inspect files, directories, dependencies, and framework signals.
- **Planning:** break a request into implementation and validation steps.
- **Tool execution:** read and write files, search code, inspect diffs, run tests, lint, and type checks.
- **Validation loop:** test → diagnose → fix → retry, with bounded attempts.
- **Provider abstraction:** use local Ollama models or hosted OpenAI and Anthropic models.
- **Memory hooks:** store and retrieve reusable resolution patterns.
- **CLI-first workflow:** interactive sessions for development and batch mode for automation.

> **Status:** GOATCODE is currently classified as **Beta** in its Python package metadata. Review generated diffs and run tests in a disposable branch or workspace before applying changes to important codebases.

## Architecture

```text
User request
     │
     ▼
CLI / Python API
     │
     ▼
Core orchestrator
 ├── intent and project-context analysis
 ├── risk analysis and implementation planning
 ├── LLM provider interface
 ├── tool registry
 ├── memory lookup / storage
 └── validation and retry loop
     │
     ▼
Files, diffs, validation report, and execution status
```

### Repository layout

```text
goatcode/
├── cli/                 # Command-line entry point
├── core/                # Agent orchestration and execution state
├── llm/                 # Provider interfaces and routing
├── tools/               # File, search, test, lint, typecheck, and Git tools
├── examples/            # Python usage examples
├── requirements.txt     # Runtime and development dependencies
├── setup.py             # Package metadata and goatcode CLI entry point
├── install.sh           # Linux/macOS setup helper
└── docker-compose.yml   # Development container definition
```

## Quick start

### Requirements

- Python **3.9 or newer**
- An LLM provider:
  - [Ollama](https://ollama.com/) for local models, or
  - an OpenAI or Anthropic API key
- Git for project inspection and diff workflows

### Install from source

```bash
git clone https://github.com/Shivay00001/goatcode.git
cd goatcode

python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Or use the helper on Linux/macOS:

```bash
chmod +x install.sh
./install.sh
```

Confirm the CLI is available:

```bash
goatcode --help
# Equivalent module invocation:
python -m goatcode --help
```

## Run with a local model

Install Ollama, start its service, and pull a coding model:

```bash
ollama pull codellama
# Or use another model available in your Ollama installation.

goatcode --provider ollama --model codellama
```

Interactive commands include `/help`, `/status`, `/models`, and `/exit`.

## Run with hosted providers

Pass credentials through your shell environment rather than committing them:

```bash
export OPENAI_API_KEY="..."
goatcode --provider openai --model gpt-4 --project ./my-project
```

```bash
export ANTHROPIC_API_KEY="..."
goatcode --provider anthropic --model claude-3-opus --project ./my-project
```

Provider and model names depend on the installed SDKs and the provider account. Use `goatcode --help` for the options supported by the current CLI implementation.

## Batch mode

Submit one task and save the result:

```bash
goatcode \
  --provider ollama \
  --model codellama \
  --project ./my-project \
  -p "Add error handling to the JSON parser and write tests" \
  -o result.json
```

The agent may modify files in the selected project. Use a clean Git branch, inspect `git diff`, and validate the result before merging.

## Python API

The package exposes an agent factory for scripted workflows:

```python
import asyncio
from goatcode import create_agent


async def main() -> None:
    agent = create_agent(
        llm_provider="ollama",
        llm_model="codellama",
    )
    result = await agent.execute(
        "Add validation and tests for the user model",
        project_path="./my-project",
    )
    print(result.status.value)


if __name__ == "__main__":
    asyncio.run(main())
```

See [`examples/usage.py`](./examples/usage.py) for additional provider, batch, and fallback examples.

## Available tools

The tool registry documents support for operations such as:

- `read_file` and `write_file`
- `list_directory` and `search_project`
- `run_tests`, `run_linter`, and `run_typecheck`
- `git_diff`
- `semantic_search` integration hooks
- `memory_lookup` and `memory_store`

Tool availability and framework detection should be verified against the current implementation before relying on a capability in automation.

## Development

Install the repository dependencies, then run the checks available in your environment:

```bash
python -m pytest tests/
python -m flake8 goatcode/
python -m mypy goatcode/
```

The dependency file includes optional integrations for vector search and advanced AST parsing. They are commented out by default and are not required for the baseline CLI workflow.

## Security and safe operation

A coding agent can read and modify a workspace and can execute developer tooling. Operate it with least privilege:

- Run it in a disposable branch, sandbox, or container.
- Never provide production credentials or unrestricted secrets.
- Review generated diffs before committing or deploying.
- Restrict the project path to the intended workspace.
- Run tests, linters, type checks, and security scans independently.
- Treat model output and generated code as untrusted until reviewed.
- Prefer local models when source confidentiality requires it; hosted providers may receive submitted context.

GOATCODE is not a substitute for code review, security review, or deployment approvals.

## Production-readiness assessment

### Strengths

- Clear separation between orchestration, LLM providers, tools, CLI, and memory.
- Local-model option supports privacy-sensitive development workflows.
- Validation and retry concepts are appropriate for agentic code generation.
- Package metadata provides an installable `goatcode` console command.

### Priority improvements before production use

1. Add and publish a reproducible automated test suite with coverage thresholds.
2. Pin dependencies with a lockfile and run vulnerability/license checks in CI.
3. Enforce workspace boundaries, path traversal protection, command allowlists, and execution timeouts.
4. Add structured audit logs for prompts, tool calls, file changes, and validation results, with secret redaction.
5. Make retry, token, cost, and model-fallback policies explicit and configurable.
6. Add integration tests for each provider and deterministic mock-provider tests for offline CI.
7. Harden the Docker and Compose workflows with a non-root user, resource limits, and documented volumes.
8. Align package classifiers and documentation with the custom commercial license before publishing to PyPI.

## Roadmap

The existing project roadmap includes:

- [ ] FAISS/ChromaDB vector search
- [ ] AST-aware diff patching
- [ ] Web interface
- [ ] VS Code extension
- [ ] CI/CD integrations
- [ ] Team collaboration and advanced memory/RAG
- [ ] Multi-file refactoring and code-review mode

## Contributing

1. Open an issue describing the change.
2. Create a focused feature branch.
3. Add or update tests and documentation.
4. Run the relevant checks locally.
5. Inspect generated diffs for unintended or unsafe changes.
6. Open a pull request with provider, tool, and security implications documented.

## License

GOATCODE is distributed under the [VisionQuantech Custom Commercial License](./LICENSE), not the MIT License. Read the complete license before using it for revenue-generating, business, or enterprise work. Contact the repository owner for commercial licensing questions.

## Links

- [Issues](https://github.com/Shivay00001/goatcode/issues)
- [Source code](https://github.com/Shivay00001/goatcode)
