# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# The AWS CDK application entry point
from aws_cdk import App, Aspects, Environment
import os
import constants
from services.component import Services
from dotenv import load_dotenv
from toolchain import Toolchain

load_dotenv()

app = App()

# Component sandbox stack
Services(
    app,
    "sagemaker-studio-deployment",
    stack_name=f"{constants.APP_NAME}-{constants.SANDBOX_ENV_NAME}",
    env_name=constants.SANDBOX_ENV_NAME,
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

# Toolchain stack (defines the continuous deployment pipeline)
Toolchain(
    app,
    "sagemaker-studio-deployment-toolchain",
    stack_name=constants.APP_NAME + "-toolchain",
    env=Environment(
        account=constants.TOOLCHAIN_ACCOUNT, region=constants.TOOLCHAIN_REGION
    ),
)

app.synth()
