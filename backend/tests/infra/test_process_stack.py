from unittest.mock import MagicMock

import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.process_stack import ProcessStack


table_mock = MagicMock()
table_mock.table_name = "table-name"


def test_lambda_function_created():
    app = core.App()
    stack = ProcessStack(app, "process", table=table_mock)
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "FunctionName": "process-current-weather",
        },
    )
