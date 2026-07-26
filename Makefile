.PHONY: help up down test smoke lint cdk-deploy cdk-destroy kind-up clean

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Start the local environment (LocalStack + api + worker)
	docker compose up -d --wait

down: ## Stop the local environment and remove its volumes
	docker compose down -v

test: ## Run the unit test suite (pytest -m unit)
	pytest -m unit

smoke: ## End-to-end smoke test against the environment started by `make up`
	./scripts/smoke-test.sh

lint: ## Run ruff over app/ and infra/
	ruff check app/ tests/

# CDK (Phase 3) is an alternative, code-based path to create the same DynamoDB
# table / S3 bucket / SQS queue that scripts/bootstrap-localstack.sh (Phase 2)
# creates automatically on `make up`. Both are idempotent and share the same
# resource naming, so it does not matter which one runs first. Requires
# LocalStack up (`make up`, or `docker compose up -d localstack`) and
# `pip install -r infra/requirements.txt` + `npm install -g aws-cdk aws-cdk-local`.
cdk-deploy: ## Synthesize and apply the CDK stack against LocalStack — Phase 3
	cd infra && AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=$${AWS_REGION:-us-east-1} cdklocal deploy --require-approval never

cdk-destroy: ## Destroy the CDK-managed resources in LocalStack
	cd infra && AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=$${AWS_REGION:-us-east-1} cdklocal destroy --force

kind-up: ## Create the kind cluster and deploy the manifests — Phase 5
	@echo "pending: Phase 5 (kind)"

clean: ## Full teardown of the local environment
	@echo "pending"
