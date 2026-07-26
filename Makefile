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

lint: ## Run ruff over app/, tests/ and infra/
	ruff check app/ tests/ infra/

# CDK (Phase 3) is an alternative, code-based path to create the same DynamoDB
# table / S3 bucket / SQS queue that scripts/bootstrap-localstack.sh (Phase 2)
# creates automatically on `make up`. Both are idempotent and share the same
# resource naming, so it does not matter which one runs first. Requires
# LocalStack up (`make up`, or `docker compose up -d localstack`) with the
# sts/cloudformation/ssm/iam services enabled (see docker-compose.yml), and
# `pip install -r infra/requirements.txt` + `npm install -g aws-cdk aws-cdk-local`.
CDK_ENV = AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_REGION=$${AWS_REGION:-us-east-1} AWS_DEFAULT_REGION=$${AWS_REGION:-us-east-1} CDK_DEFAULT_ACCOUNT=$${CDK_DEFAULT_ACCOUNT:-000000000000} CDK_DEFAULT_REGION=$${AWS_REGION:-us-east-1}

cdk-deploy: ## Bootstrap (idempotent) and deploy the CDK stack against LocalStack — Phase 3
	cd infra && $(CDK_ENV) cdklocal bootstrap
	cd infra && $(CDK_ENV) cdklocal deploy --require-approval never

cdk-destroy: ## Destroy the CDK-managed resources in LocalStack
	cd infra && $(CDK_ENV) cdklocal destroy --force

kind-up: ## Create the kind cluster and deploy the manifests — Phase 5
	@echo "pending: Phase 5 (kind)"

clean: ## Full teardown of the local environment
	@echo "pending"
