#!/usr/bin/env bash
# End-to-end smoke test against the environment started by `make up`:
# create a task -> upload an attachment -> poll until the worker marks it `processed`.

set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"
POLL_ATTEMPTS="${POLL_ATTEMPTS:-15}"
POLL_INTERVAL="${POLL_INTERVAL:-2}"

echo "Creating task..."
CREATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "smoke test task", "description": "created by scripts/smoke-test.sh"}')
CREATE_STATUS=$(echo "$CREATE_RESPONSE" | tail -n1)
CREATE_BODY=$(echo "$CREATE_RESPONSE" | sed '$d')

if [ "$CREATE_STATUS" != "201" ]; then
  echo "FAIL: expected 201 creating task, got $CREATE_STATUS"
  echo "$CREATE_BODY"
  exit 1
fi

TASK_ID=$(echo "$CREATE_BODY" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')
echo "Task created: $TASK_ID"

echo "Uploading attachment..."
ATTACHMENT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "$API_URL/tasks/$TASK_ID/attachment" \
  -F "file=@scripts/smoke-test.sh")

if [ "$ATTACHMENT_STATUS" != "200" ]; then
  echo "FAIL: expected 200 uploading attachment, got $ATTACHMENT_STATUS"
  exit 1
fi
echo "Attachment uploaded."

echo "Waiting for the worker to mark the task as processed..."
for attempt in $(seq 1 "$POLL_ATTEMPTS"); do
  STATUS=$(curl -s "$API_URL/tasks/$TASK_ID" | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])')
  if [ "$STATUS" = "processed" ]; then
    echo "Task $TASK_ID is processed."
    echo "SMOKE TEST PASSED"
    exit 0
  fi
  echo "Attempt $attempt/$POLL_ATTEMPTS: status=$STATUS, retrying in ${POLL_INTERVAL}s..."
  sleep "$POLL_INTERVAL"
done

echo "FAIL: task $TASK_ID was not marked processed after $POLL_ATTEMPTS attempts"
exit 1
