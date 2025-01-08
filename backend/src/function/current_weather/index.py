import os
import json
from decimal import Decimal

import boto3
import requests

TABLE_NAME = os.environ["TABLE_NAME"]
COORDINATE = os.environ["COORDINATE"]
LATITUDE, LONGITUDE = COORDINATE.split(",")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    print(f"Current weather for {COORDINATE}")

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast?"
        + f"latitude={LATITUDE}&"
        + f"longitude={LONGITUDE}&"
        + "current=temperature_2m,relative_humidity_2m,surface_pressure"
    )

    data = json.loads(response.text, parse_float=Decimal)
    print(data)

    item = {
        "coordinate": COORDINATE.replace(",", "#"),
        "timestamp": data["current"]["time"],
        "temperature": data["current"]["temperature_2m"],
        "humidity": data["current"]["relative_humidity_2m"],
        "pressure": data["current"]["surface_pressure"],
    }
    table.put_item(Item=item)

    return item
