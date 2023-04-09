install:  ## Install dependencies
	@bash scripts/install.sh

run:  ## Run the service
	@bash scripts/run.sh

format:  ## Format the code
	@bash scripts/format.sh

lint:  ## Lint the code
	@bash scripts/lint.sh

test:  ## Run the tests
	@bash scripts/test.sh

docker-build:  ## Build the docker image
	@bash scripts/docker-build.sh

docker-run:  ## Run the docker image
	@bash scripts/docker-run.sh

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
