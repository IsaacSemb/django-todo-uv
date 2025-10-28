# SAMPLE YAML FILE FOR CI CD 
```yaml

name: CI (Django + uv)

on:
  push:
    branches: [ main, master ]
    paths-ignore: [ "**.md", "**.png", "**.jpg" ]
  pull_request:
    branches: [ "**" ]

jobs:
  lint:
    name: Lint & Static Checks
    runs-on: ubuntu-latest
    env:
      PYTHONUNBUFFERED: "1"
      PIP_DISABLE_PIP_VERSION_CHECK: "1"
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv (fast Python pkg manager)
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH
          uv --version

      - name: Cache uv
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/uv
            .venv
          key: uv-${{ runner.os }}-${{ hashFiles('uv.lock', 'pyproject.toml', 'requirements*.txt') }}-py311
          restore-keys: |
            uv-${{ runner.os }}-

      - name: Sync dependencies (pyproject or requirements)
        run: |
          if [ -f pyproject.toml ]; then
            uv venv --seed --python 3.11
            uv sync --all-extras --dev
          elif [ -f requirements.txt ]; then
            uv venv --seed --python 3.11
            uv pip install -r requirements.txt
            if [ -f requirements-dev.txt ]; then uv pip install -r requirements-dev.txt; fi
          else
            echo "No pyproject.toml or requirements.txt found" && exit 1
          fi
          . .venv/bin/activate
          python -V
          pip list

      - name: Ruff (lint)
        run: |
          . .venv/bin/activate
          ruff --version || uv pip install ruff
          ruff check .

      - name: Black (format check)
        run: |
          . .venv/bin/activate
          black --version || uv pip install black
          black --check .

      - name: Mypy (optional strictness)
        run: |
          . .venv/bin/activate
          mypy --version || uv pip install mypy
          mypy --ignore-missing-imports || true  # relax to non-blocking if you’re ramping up

  test:
    name: Unit Tests (Postgres)
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports: [ "5432:5432" ]
        options: >-
          --health-cmd="pg_isready -U test_user -d test_db"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    env:
      PYTHONUNBUFFERED: "1"
      DJANGO_SETTINGS_MODULE: yourproject.settings
      SECRET_KEY: dummy
      DEBUG: "0"
      # Prefer DATABASE_URL to match prod-style config
      DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
      # Make TZ explicit to catch brittle tests
      TZ: Europe/London

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install system packages (if you need Pillow/libpq/etc.)
        run: |
          sudo apt-get update
          sudo apt-get install -y libpq-dev build-essential libjpeg-dev zlib1g-dev

      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH
          uv --version

      - name: Cache uv
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/uv
            .venv
          key: uv-${{ runner.os }}-${{ hashFiles('uv.lock', 'pyproject.toml', 'requirements*.txt') }}-py311
          restore-keys: |
            uv-${{ runner.os }}-

      - name: Sync dependencies (pyproject or requirements)
        run: |
          if [ -f pyproject.toml ]; then
            uv venv --seed --python 3.11
            uv sync --all-extras --dev
          elif [ -f requirements.txt ]; then
            uv venv --seed --python 3.11
            uv pip install -r requirements.txt
            if [ -f requirements-dev.txt ]; then uv pip install -r requirements-dev.txt; fi
          else
            echo "No pyproject.toml or requirements.txt found" && exit 1
          fi

      - name: Django sanity checks
        run: |
          . .venv/bin/activate
          python -m django --version
          python manage.py check --deploy

      - name: Check for missing migrations
        run: |
          . .venv/bin/activate
          python manage.py makemigrations --check --dry-run

      - name: Run migrations
        run: |
          . .venv/bin/activate
          python manage.py migrate --noinput

      - name: Build static files (catches pipeline misconfig)
        run: |
          . .venv/bin/activate
          python manage.py collectstatic --noinput

      - name: Run tests with coverage (pytest if present else Django test)
        run: |
          . .venv/bin/activate
          uv pip install coverage pytest pytest-django || true
          if [ -f pytest.ini ] || [ -f pyproject.toml ] && grep -q "\[tool.pytest.ini_options\]" pyproject.toml; then
            coverage run -m pytest -q
          else
            coverage run manage.py test -v 2
          fi
          coverage xml
          coverage report -m

      - name: Upload coverage.xml
        uses: actions/upload-artifact@v4
        with:
          name: coverage-xml
          path: coverage.xml

      - name: Upload junit (if pytest created it)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: junit
          path: "**/junit*.xml"
          if-no-files-found: ignore


```