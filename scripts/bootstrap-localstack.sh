#!/usr/bin/env bash
# Creates the DynamoDB table, S3 bucket and SQS queue used by the app against LocalStack.
# Idempotent: re-running (e.g. on every `docker compose up`) must not fail (see wiki:
# idempotencia-infra). Runs automatically as a LocalStack init hook
# (/etc/localstack/init/ready.d/), where `awslocal` is available.

set -euo pipefail

TASKS_TABLE="${TASKS_TABLE:-tasks-local}"
ATTACHMENTS_BUCKET="${ATTACHMENTS_BUCKET:-attachments-local}"
EVENTS_QUEUE="${EVENTS_QUEUE:-task-events-local}"

echo "Bootstrapping LocalStack resources..."

awslocal dynamodb create-table \
  --table-name "$TASKS_TABLE" \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  || echo "Table $TASKS_TABLE already exists, skipping."

awslocal s3 mb "s3://$ATTACHMENTS_BUCKET" \
  || echo "Bucket $ATTACHMENTS_BUCKET already exists, skipping."

awslocal sqs create-queue --queue-name "$EVENTS_QUEUE" \
  || echo "Queue $EVENTS_QUEUE already exists, skipping."

echo "LocalStack bootstrap done."
