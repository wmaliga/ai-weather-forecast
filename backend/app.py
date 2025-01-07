#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.storage_stack import StorageStack

stack_name = "ai-weather-forecast"

env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION"),
)

app = cdk.App()

StorageStack(app, f"{stack_name}-storage", env=env)

app.synth()
