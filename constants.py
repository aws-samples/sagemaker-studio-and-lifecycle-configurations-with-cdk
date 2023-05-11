# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Environment variables
APP_NAME = "sagemaker-studio"
SAGEMAKER_DOMAIN_NAME_PREFIX = "sms"
SANDBOX_ENV_NAME = "sandbox"
MAIN_ENV_NAME = "dev"
MAIN_ENV_ACCOUNT = ""  # which region would you like to deploy the production studio
MAIN_ENV_REGION = ""  # which region would you like to deploy the production studio

# which account should your cicd pipelines go in
TOOLCHAIN_ACCOUNT = ""  # which account should your cicd pipelines go in.
TOOLCHAIN_REGION = ""  # which region should your cicd pipelines go in.

#networking
VPC_NAME = ""  # update to the VPC you will install SageMaker Studio into.

SUBNET_DEPLOYMENT_TYPE = "PRIVATE_WITH_NAT"
USE_S3_FOR_ASSETS = True

# auth
AUTH_TYPE = "SSO"  # alternative is IAM
ADD_GLUE_PERMISSION = True

# studio settings
JUPYTERLAB_DEFAULT = "JL3"  # alternative is JL1

CODECOMMIT_REPO = APP_NAME + "-" + "config-repo"
CODECOMMIT_TRUNK_BRANCH = "main"
