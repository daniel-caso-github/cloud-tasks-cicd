# Cloud Tasks CI/CD Lab

FastAPI task microservice, 100% local, against AWS emulated with LocalStack (DynamoDB, S3, SQS),
infrastructure as code with CDK, packaged in Docker, orchestrated on local Kubernetes (kind), and
validated by a GitHub Actions pipeline.

> Work in progress — see the phase plan in the project's LLM Wiki.

## Infrastructure: two alternative paths

The DynamoDB table, S3 bucket and SQS queue can be created two ways. They use the same resource
names and are both idempotent, but they are **alternatives for a given LocalStack instance**, not
meant to run back-to-back against the same running container (see conflict note below):

1. **Bootstrap script (Phase 2)** — `scripts/bootstrap-localstack.sh` runs automatically as a
   LocalStack init hook every time `make up` starts the stack.
2. **AWS CDK (Phase 3)** — `infra/` declares the same resources as code (`TasksStack`), applied to
   LocalStack with `cdklocal`:

   ```bash
   npm install -g aws-cdk aws-cdk-local
   pip install -r infra/requirements.txt
   make up                 # starts LocalStack (with sts/cloudformation/ssm/iam enabled) + api + worker
   make cdk-deploy          # cdklocal bootstrap + cdklocal deploy, from infra/
   make cdk-destroy         # cdklocal destroy, from infra/
   ```

   Requires `AWS_ACCESS_KEY_ID=test`, `AWS_SECRET_ACCESS_KEY=test`, `AWS_REGION` and
   `CDK_DEFAULT_ACCOUNT=000000000000` in the environment — `make cdk-deploy`/`cdk-destroy` already
   export sensible defaults, override `AWS_REGION`/`CDK_DEFAULT_ACCOUNT` if needed.

   **Known conflict**: because `make up` already runs the bootstrap script automatically, running
   `make cdk-deploy` right after against the *same* LocalStack instance fails —
   CloudFormation tries to `CreateTable`/`CreateBucket`/`CreateQueue` for names the script already
   created outside of CDK's control (`ResourceInUseException: Table already exists`). To exercise
   the CDK path cleanly, start LocalStack **without** the bootstrap init hook (e.g.
   `docker run -e SERVICES=dynamodb,s3,sqs,sts,cloudformation,ssm,iam -p 4566:4566
   localstack/localstack:3`, skipping the volume mount that injects
   `scripts/bootstrap-localstack.sh`) and run `make cdk-deploy` against that. Once resources exist
   (created by either path), the app itself does not care who created them — it only reads the
   names from env.

   The S3 bucket does **not** use CDK's `auto_delete_objects`: that feature relies on a
   CDK-generated Lambda custom resource whose runtime (`nodejs24.x`) is newer than what LocalStack
   Community's Lambda emulation supports, and pulling in the `lambda` service just for that adds an
   extra failure surface. `RemovalPolicy.DESTROY` still applies to the bucket itself.
