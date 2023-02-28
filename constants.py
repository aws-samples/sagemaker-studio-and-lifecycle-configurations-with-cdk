# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Environment variables
APP_NAME = "sagemaker-studio"
SAGEMAKER_DOMAIN_NAME_PREFIX = "sms"
SANDBOX_ENV_NAME = "sandbox"
PRODUCTION_ENV_NAME = "prod"
PRODUCTION_ENV_ACCOUNT = ""
PRODUCTION_ENV_REGION = ""

# networking
VPC_NAME = "analytics-vpc"

# auth
AUTH_TYPE = "SSO"  # alternative is IAM
ADD_GLUE_PERMISSION = True

# studio settings
JUPYTERLAB_DEFAULT = "JL3"  # alternative is JL1

# which account should your cicd pipelines go in.
TOOLCHAIN_ACCOUNT = ""
TOOLCHAIN_REGION = ""

CODECOMMIT_REPO = APP_NAME + "-" + "config-repo"
CODECOMMIT_TRUNK_BRANCH = "main"
