# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
PRODUCTION_ENV_ACCOUNT = "" # which region would you like to deploy the production studio
PRODUCTION_ENV_REGION = "" # which region would you like to deploy the production studio

TOOLCHAIN_ACCOUNT = "" # which account should your cicd pipelines go in.
TOOLCHAIN_REGION = "" # which region should your cicd pipelines go in.

VPC_NAME = "" # update to the VPC you will install SageMaker Studio into.

# Environment variables
APP_NAME = "sagemaker-studio"
SAGEMAKER_DOMAIN_NAME_PREFIX = "sms"
SANDBOX_ENV_NAME = "sandbox"
PRODUCTION_ENV_NAME = "prod"

# auth
AUTH_TYPE = "SSO"  # alternative is IAM
ADD_GLUE_PERMISSION = True

# studio settings
JUPYTERLAB_DEFAULT = "JL3"  # alternative is JL1

CODECOMMIT_REPO = APP_NAME + "-" + "config-repo"
CODECOMMIT_TRUNK_BRANCH = "main"
