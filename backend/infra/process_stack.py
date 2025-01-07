from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as event_targets,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as lambda_python,
)
from constructs import Construct


class ProcessStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        current_weather_lambda = lambda_python.PythonFunction(
            self,
            id=f"{construct_id}-current-weather",
            function_name=f"{construct_id}-current-weather",
            runtime=_lambda.Runtime.PYTHON_3_10,
            entry="src/lambda/current_weather",
        )

        every_hour_schedule = events.Schedule.cron(day="*", hour="*", minute="0")
        current_weather_target = event_targets.LambdaFunction(
            handler=current_weather_lambda
        )
        events.Rule(
            self,
            f"{construct_id}-current-weather-rule",
            rule_name=f"{construct_id}-current-weather-rule",
            description="Save current weather every hour",
            enabled=True,
            schedule=every_hour_schedule,
            targets=[current_weather_target],
        )
