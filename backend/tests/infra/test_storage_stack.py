import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.storage_stack import StorageStack


def test_dynamodb_table_created():
    app = core.App()
    stack = StorageStack(app, "storage")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "TableName": "storage-table",
            "KeySchema": [
                {"AttributeName": "coordinate", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
        },
    )
