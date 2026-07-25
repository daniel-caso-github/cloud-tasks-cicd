.PHONY: help up down test lint cdk-deploy kind-up clean

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Start the local environment (LocalStack + api + worker) — Phase 2
	@echo "pending: Phase 2 (localstack)"

down: ## Stop the local environment — Phase 2
	@echo "pending: Phase 2 (localstack)"

test: ## Run the unit test suite (pytest -m unit)
	pytest -m unit

lint: ## Run ruff over app/ and infra/
	ruff check app/ tests/

cdk-deploy: ## Synthesize and apply the CDK stack against LocalStack — Phase 3
	@echo "pending: Phase 3 (cdk)"

kind-up: ## Create the kind cluster and deploy the manifests — Phase 5
	@echo "pending: Phase 5 (kind)"

clean: ## Full teardown of the local environment
	@echo "pending"
