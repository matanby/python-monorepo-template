install:  ## Install the package
	@bash scripts/install.sh $(args)

format:  ## Format the code
	@bash scripts/format.sh $(args)

lint:  ## Lint the code
	@bash scripts/lint.sh $(args)

test:  ## Run the tests
	@bash scripts/test.sh $(args)

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
