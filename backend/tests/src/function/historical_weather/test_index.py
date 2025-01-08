import json
import os

import boto3
import pytest
from moto import mock_aws

os.environ["TABLE_NAME"] = "table-name"
os.environ["COORDINATE"] = "50.00,15.00"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"


@pytest.fixture(scope="function")
def dynamodb_table(aws_credentials):
    with mock_aws():
        conn = boto3.resource("dynamodb")
        table = conn.create_table(
            TableName="table-name",
            AttributeDefinitions=[
                {"AttributeName": "coordinate", "AttributeType": "S"},
                {"AttributeName": "timestamp", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "coordinate", "KeyType": "HASH"},
                {"AttributeName": "timestamp", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield table


@pytest.fixture(autouse=True)
def get_request_mock(requests_mock):
    requests_mock.get(
        "https://archive-api.open-meteo.com/v1/era5?"
        + "latitude=50.00&"
        + "longitude=15.00&"
        + "start_date=2025-01-01&"
        + "end_date=2025-01-01&"
        + "hourly=temperature_2m,relative_humidity_2m,surface_pressure",
        text=json.dumps(
            {
                "hourly": {
                    "time": [
                        "2025-01-01T00:00",
                        "2025-01-01T01:00",
                    ],
                    "temperature_2m": [
                        20.0,
                        20.1,
                    ],
                    "relative_humidity_2m": [
                        50.0,
                        50.1,
                    ],
                    "surface_pressure": [
                        980.0,
                        980.1,
                    ],
                }
            }
        ),
    )


@mock_aws
def test_handler(dynamodb_table):
    from src.function.historical_weather.index import handler

    items = handler(
        {
            "start_date": "2025-01-01",
            "end_date": "2025-01-01",
        },
        {},
    )

    assert items == [
        {
            "coordinate": "50.00#15.00",
            "timestamp": "2025-01-01T00:00",
            "temperature": 20.0,
            "humidity": 50.0,
            "pressure": 980.0,
        },
        {
            "coordinate": "50.00#15.00",
            "timestamp": "2025-01-01T01:00",
            "temperature": 20.1,
            "humidity": 50.1,
            "pressure": 980.1,
        },
    ]
