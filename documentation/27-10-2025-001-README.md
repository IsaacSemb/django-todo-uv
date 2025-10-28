# UV Package Manager 101

A hands-on exploration of `uv` as a modern replacement for pip, focusing on dependency management and project workflow.

## Installation

Unlike pip, `uv` doesn't come with Python. Install it via curl:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Curl flags breakdown:**
- `-L` — follow redirects
- `-s` — silent mode (quiet output)
- `-S` — show errors even in silent mode
- `-f` — fail on HTTP errors
- `| sh` — execute the downloaded script

## Project Setup

Create a new project:
```bash
uv init <projectname>
```

This creates the basic project structure:
```
.
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

## Key Concepts

### Virtual Environment Management
- **No manual venv creation needed** — `uv` handles this automatically
- When you install your first dependency or run `uv run pip list`, `uv` creates the `.venv` directory
- A `uv.lock` file is generated (similar to `package-lock.json` in npm)
- **`pyproject.toml` = `package.json`** — your project configuration file

### Dependency Management
```bash
# Add dependencies
uv add requests

# View dependency tree
uv tree

# Sync/install everything
uv sync
```

### Running Code
Always prefix commands with `uv` to use the project's virtual environment:
```bash
uv run python main.py
```

### Script Entry Points
Create shortcuts in `pyproject.toml`:
```toml
[project.scripts]
joke = "main:get_joke"
```

Then sync and run:
```bash
uv sync
uv run joke
```

**Note:** Unlike npm's auto-sync, you need to explicitly run `uv sync` after adding script entry points.
