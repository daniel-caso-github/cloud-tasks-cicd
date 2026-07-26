"""TasksStack: DynamoDB table, S3 bucket and SQS queue for the Cloud Tasks app.

Resource names come from CDK context or environment variables, never hardcoded
(see wiki: naming-recursos), matching the names the app reads via
app/config.py. All resources use RemovalPolicy.DESTROY: this is a lab, nothing
survives a destroy (see wiki: teardown-y-costos, idempotencia-infra).
"""

import os

from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class TasksStack(Stack):
    """Declares the tasks table, attachments bucket and events queue."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        tasks_table_name = self._resource_name("tasksTable", "TASKS_TABLE", "tasks-local")
        attachments_bucket_name = self._resource_name(
            "attachmentsBucket", "ATTACHMENTS_BUCKET", "attachments-local"
        )
        events_queue_name = self._resource_name("eventsQueue", "EVENTS_QUEUE", "task-events-local")

        table = dynamodb.Table(
            self,
            "TasksTable",
            table_name=tasks_table_name,
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        bucket = s3.Bucket(
            self,
            "AttachmentsBucket",
            bucket_name=attachments_bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        queue = sqs.Queue(
            self,
            "EventsQueue",
            queue_name=events_queue_name,
            visibility_timeout=Duration.seconds(30),
            removal_policy=RemovalPolicy.DESTROY,
        )

        CfnOutput(self, "TasksTableName", value=table.table_name)
        CfnOutput(self, "AttachmentsBucketName", value=bucket.bucket_name)
        CfnOutput(self, "EventsQueueName", value=queue.queue_name)
        CfnOutput(self, "EventsQueueUrl", value=queue.queue_url)

    def _resource_name(self, context_key: str, env_var: str, default: str) -> str:
        """Resolve a resource name: CDK context, then env var, then the `*-local` default.

        Mirrors the precedence app/config.py uses for the same names (see wiki:
        naming-recursos).
        """
        return self.node.try_get_context(context_key) or os.environ.get(env_var, default)
