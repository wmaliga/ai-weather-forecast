from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class StorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dynamodb.Table(
            self,
            f"{construct_id}-table",
            table_name=f"{construct_id}-table",
            partition_key=dynamodb.Attribute(
                name="coordinate",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING,
            ),
        )
