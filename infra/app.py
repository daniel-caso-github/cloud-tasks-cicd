#!/usr/bin/env python3
"""CDK entry point: instantiates the TasksStack (see wiki: cdk-stack)."""

import os

import aws_cdk as cdk

from stacks.tasks_stack import TasksStack

app = cdk.App()

# LocalStack has no real AWS account; fix a fake one so the CDK CLI does not
# try to resolve it via STS (see wiki: sin-despliegue-real). Overridable via
# CDK_DEFAULT_ACCOUNT/CDK_DEFAULT_REGION for a hypothetical real-AWS run.
env = cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT", "000000000000"),
    region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
)

TasksStack(app, "TasksStack", env=env)

app.synth()
