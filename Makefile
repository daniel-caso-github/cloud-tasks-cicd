.PHONY: help up down test lint cdk-deploy kind-up clean

help: ## Lista los targets disponibles
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Levanta el entorno local (LocalStack + api + worker) — Fase 2
	@echo "pendiente: Fase 2 (localstack)"

down: ## Baja el entorno local — Fase 2
	@echo "pendiente: Fase 2 (localstack)"

test: ## Corre la suite de tests (pytest) — Fase 1
	@echo "pendiente: Fase 1 (app)"

lint: ## Corre ruff sobre app/ e infra/ — Fase 1
	@echo "pendiente: Fase 1 (app)"

cdk-deploy: ## Sintetiza y aplica el stack CDK contra LocalStack — Fase 3
	@echo "pendiente: Fase 3 (cdk)"

kind-up: ## Crea el cluster kind y despliega los manifiestos — Fase 5
	@echo "pendiente: Fase 5 (kind)"

clean: ## Teardown completo del entorno local
	@echo "pendiente"
