.DEFAULT_GOAL := help
.PHONY: help typecheck install format lint test

install:  ## Install
	@bash scripts/install.sh $(args)

format:  ## Format
	@bash scripts/format.sh $(args)

lint:  ## Lint
	@bash scripts/lint.sh $(args)

test:  ## Test
	@bash scripts/test.sh $(args)

typecheck:  ## Check Python types
	@bash scripts/typecheck.sh $(args)

help:  ## Show available commands
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
