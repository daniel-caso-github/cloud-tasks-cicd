.PHONY: help up down test lint cdk-deploy kind-up clean

help: ## Lista los targets disponibles
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Levanta el entorno local (LocalStack + api + worker) — Fase 2
	@echo "pendiente: Fase 2 (localstack)"

down: ## Baja el entorno local — Fase 2
	@echo "pendiente: Fase 2 (localstack)"

test: ## Corre la suite de tests unitarios (pytest -m unit)
	pytest -m unit

lint: ## Corre ruff sobre app/ e infra/
	ruff check app/ tests/

cdk-deploy: ## Sintetiza y aplica el stack CDK contra LocalStack — Fase 3
	@echo "pendiente: Fase 3 (cdk)"

kind-up: ## Crea el cluster kind y despliega los manifiestos — Fase 5
	@echo "pendiente: Fase 5 (kind)"

clean: ## Teardown completo del entorno local
	@echo "pendiente"
