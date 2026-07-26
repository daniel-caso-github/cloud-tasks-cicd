# Cloud Tasks CI/CD Lab

FastAPI task microservice, 100% local, against AWS emulated with LocalStack (DynamoDB, S3, SQS),
infrastructure as code with CDK, packaged in Docker, orchestrated on local Kubernetes (kind), and
validated by a GitHub Actions pipeline.

> Work in progress — see the phase plan in the project's LLM Wiki.

## Infrastructure: two coexisting paths

The DynamoDB table, S3 bucket and SQS queue can be created two ways, and both are valid at the
same time (same resource names, both idempotent):

1. **Bootstrap script (Phase 2)** — `scripts/bootstrap-localstack.sh` runs automatically as a
   LocalStack init hook every time `make up` starts the stack.
2. **AWS CDK (Phase 3)** — `infra/` declares the same resources as code (`TasksStack`), applied to
   LocalStack with `cdklocal`:

   ```bash
   npm install -g aws-cdk aws-cdk-local
   pip install -r infra/requirements.txt
   make up                 # or: docker compose up -d localstack
   make cdk-deploy          # cdklocal deploy, from infra/
   make cdk-destroy         # cdklocal destroy, from infra/
   ```

   `cdklocal synth` (no LocalStack needed) is confirmed working in this repo. `cdklocal deploy`
   against a real LocalStack container could not be fully verified in the development environment
   used to build Phase 3: the installed `aws-cdk` CLI (a very recent 2.x release) fails to resolve
   AWS account/credentials against LocalStack's fake `000000000000` account even with dummy
   `test`/`test` credentials exported (`Need to perform AWS calls for account 000000000000, but no
   credentials have been configured`), which looks like a compatibility gap between that CLI
   version and `aws-cdk-local`. The stack code itself is standard CDK (no LocalStack-specific
   hacks) and should deploy normally with a compatible CLI version. If you hit the same error,
   try pinning an older `aws-cdk` release.
