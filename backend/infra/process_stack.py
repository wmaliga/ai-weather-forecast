from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_events as events,
    aws_events_targets as event_targets,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as lambda_python,
)
from constructs import Construct


class ProcessStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, table: dynamodb.Table, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### Current weather lambda
        current_weather_lambda = lambda_python.PythonFunction(
            self,
            id=f"{construct_id}-current-weather",
            function_name=f"{construct_id}-current-weather",
            runtime=_lambda.Runtime.PYTHON_3_10,
            entry="src/function/current_weather",
            environment={
                "TABLE_NAME": table.table_name,
                "COORDINATE": "53.11,15.81",
            },
        )

        table.grant_write_data(current_weather_lambda)

        ### Historical weather lambda
        historical_weather_lambda = lambda_python.PythonFunction(
            self,
            id=f"{construct_id}-historical-weather",
            function_name=f"{construct_id}-historical-weather",
            runtime=_lambda.Runtime.PYTHON_3_10,
            entry="src/function/historical_weather",
            timeout=Duration.minutes(15),
            environment={
                "TABLE_NAME": table.table_name,
                "COORDINATE": "53.11,15.81",
            },
        )

        table.grant_write_data(historical_weather_lambda)

        # Scheduled events
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
