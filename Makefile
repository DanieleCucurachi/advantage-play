.DEFAULT_GOAL := help
.PHONY: help install notebooks hooks lint format typecheck test test-fast cov check docs docs-live build clean

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Create the environment and install all dev dependencies
	uv sync

notebooks: ## Install notebook tooling as well
	uv sync --group notebooks

hooks: ## Install git hooks (pre-commit + pre-push)
	uv run pre-commit install

lint: ## Lint and check formatting
	uv run ruff check .
	uv run ruff format --check .

format: ## Auto-fix lint issues and format code
	uv run ruff check --fix .
	uv run ruff format .

typecheck: ## Static type check
	uv run mypy

test: ## Run the full test suite
	uv run pytest -n auto

test-fast: ## Run tests excluding slow Monte Carlo ones
	uv run pytest -n auto -m "not slow"

cov: ## Run tests with a coverage report
	uv run pytest -n auto --cov --cov-report=term-missing --cov-report=html

check: lint typecheck test-fast ## Everything CI checks (fast tests)

docs: ## Build the HTML docs into docs/_build/html (warnings are errors)
	uv run --group docs sphinx-build -W --keep-going -b html docs docs/_build/html

docs-live: ## Serve the docs locally with auto-reload
	uv run --group docs sphinx-autobuild docs docs/_build/html

build: ## Build sdist and wheel into dist/
	uv build

clean: ## Remove caches and build/experiment artifacts
	rm -rf dist build docs/_build docs/api htmlcov .coverage coverage.xml .pytest_cache .mypy_cache .ruff_cache .hypothesis
	find . -type d -name __pycache__ -not -path './.venv/*' -prune -exec rm -rf {} +
