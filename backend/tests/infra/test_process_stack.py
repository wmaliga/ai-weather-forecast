import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.process_stack import ProcessStack


def test_lambda_function_created():
    app = core.App()
    stack = ProcessStack(app, "process")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "FunctionName": "process-current-weather",
        },
    )
