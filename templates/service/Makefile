.DEFAULT_GOAL := help
.PHONY: help typecheck install format lint test run docker-build docker-run

install:  ## Install
	@bash scripts/install.sh $(args)

format:  ## Format
	@bash scripts/format.sh $(args)

lint:  ## Lint
	@bash scripts/lint.sh $(args)

test:  ## Test
	@bash scripts/test.sh $(args)

run:  ## Run
	@bash scripts/run.sh $(args)

docker-build:  ## Docker build
	@bash scripts/docker-build.sh $(args)

docker-run:  ## Docker run
	@bash scripts/docker-run.sh $(args)

typecheck:  ## Check Python types
	@bash scripts/typecheck.sh $(args)

help:  ## Show available commands
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
