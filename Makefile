.PHONY: help up down test smoke lint cdk-deploy kind-up clean

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Start the local environment (LocalStack + api + worker)
	docker compose up -d --wait

down: ## Stop the local environment
	docker compose down

test: ## Run the unit test suite (pytest -m unit)
	pytest -m unit

smoke: ## End-to-end smoke test against the environment started by `make up`
	./scripts/smoke-test.sh

lint: ## Run ruff over app/ and infra/
	ruff check app/ tests/

cdk-deploy: ## Synthesize and apply the CDK stack against LocalStack — Phase 3
	@echo "pending: Phase 3 (cdk)"

kind-up: ## Create the kind cluster and deploy the manifests — Phase 5
	@echo "pending: Phase 5 (kind)"

clean: ## Full teardown of the local environment
	@echo "pending"
