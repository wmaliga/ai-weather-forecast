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
    start_date = event["start_date"]
    end_date = event["end_date"]

    print(f"Historical weather for {COORDINATE}")
    print(f"Time range: {start_date} - {end_date}")

    response = requests.get(
        "https://archive-api.open-meteo.com/v1/era5?"
        + f"latitude={LATITUDE}&"
        + f"longitude={LONGITUDE}&"
        + f"start_date={start_date}&"
        + f"end_date={end_date}&"
        + "hourly=temperature_2m,relative_humidity_2m,surface_pressure"
    )

    data = json.loads(response.text, parse_float=Decimal)

    size = len(data["hourly"]["time"])

    print(f"Processing {size} items")

    items: list[dict] = []

    for i in range(size):
        items.append(
            {
                "coordinate": COORDINATE.replace(",", "#"),
                "timestamp": data["hourly"]["time"][i],
                "temperature": data["hourly"]["temperature_2m"][i],
                "humidity": data["hourly"]["relative_humidity_2m"][i],
                "pressure": data["hourly"]["surface_pressure"][i],
            }
        )

    print(f"Saving {size} items in the database")

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    return items
