.DEFAULT_GOAL := help
export name
.PHONY: help install typecheck smoke new-service new-package format lint test check

install:  ## Install all workspace members and development tools
	uv sync --all-packages --locked

new-service:  ## Create a service: make new-service name=my-service
	@python3 scripts/scaffold.py service "$$name"

new-package:  ## Create a package: make new-package name=my-package
	@python3 scripts/scaffold.py package "$$name"

format:  ## Format Python code
	uv run --locked ruff format . $(args)

lint:  ## Lint Python code
	uv run --locked ruff check . $(args)

test:  ## Test scaffolding and every workspace member
	uv run --all-packages --locked python scripts/test_all.py $(args)

typecheck:  ## Check types across scripts, tests, and workspace members
	uv run --all-packages --locked ty check

smoke:  ## Generate, test, build, and install connected sample projects
	uv run --locked python scripts/smoke_test.py $(args)

check: lint typecheck test  ## Run lint, type, formatting, and test checks
	uv run --locked ruff format --check .

help:  ## Show available commands
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
