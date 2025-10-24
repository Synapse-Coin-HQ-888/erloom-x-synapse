# CRUSH.md

Build/Run  
- uv sync --extra all; uv pip install flash-attn --no-build-isolation  
- uv run main                      # CLI entry; see AGENT.md for modes  
- uv run main --dry --n 1 --debug  # Mock client dry run  
- uv run main <ware|loom> <dry|train|dump> [n] [opts]  

Test  
- uv run testslide errloom/test_synapseware_parse_testslide.py  # pre-commit hook path  
- uv run testslide tests/                                      # run all TestSlide tests  
- uv run pytest tests -q                                       # if pytest-based tests are added  
- Single test: uv run pytest tests/test_synapseware.py::test_basic -q  

Docs  
- (Sphinx in docs/) make -C docs html  

Lint/Typecheck  
- ruff/mypy not configured; if present use:  
  - uv run ruff check errloom  
  - uv run mypy errloom  

Style  
- Python 3.11–3.12, run via uv. No comments unless explicitly needed. Avoid kwargs except in public APIs. Prefer mutable data structures and classes over functional constructs. Use strong typing; only import from verified modules; do not assume external libraries not in pyproject.  
- Security: never log secrets or plaintext credentials. Logging handled via `errloom.lib.log` (RichHandler, color utilities). Use logger via `getLogger` or `setup_logging`. Keep console logs concise and file logs detailed.  
- Errors: raise explicit exceptions. In CLI contexts, call `show_help` on invalid args. Follow `log_design` principles from CLAUDE/AGENT.  
- Naming conventions: `snake_case` for variables/functions, `PascalCase` for classes, `UPPER_SNAKE` for constants.  
- Imports: use absolute imports within the package (e.g., `from errloom.*`) consistent with current structure.  
- Formatting: black-like (120 width common for logs), maintain readability.  
- CLI: prefer `uv run main` with argument definitions in `argp.py`.  
- Testing: use TestSlide where suitable; prefer mocks to external network calls.  

Cursor/Copilot Rules  
- Include `.cursor/rules/base.mdc` for coding and logging standards. Follow the Pair Programming and Work Standards defined in `CLAUDE.md` and `AGENT.md`.  

Notes  
- Project scripts: `[project.scripts]` includes `main` and `errl` in `pyproject.toml`.  
- VLLM and flash-attn are heavy dependencies — uv toolchain is strongly recommended.  
- The code automatically creates and uses `runs/` and `logs/` directories.  
