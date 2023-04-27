# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_kms as kms,
    aws_s3 as s3,
    aws_sagemaker as sagemaker,
    CfnTag,
)
from constructs import Construct
import aws_cdk as cdk

import constants
from services.stacks.studio_lifecycle_config_stack import StudioLifecycleConfigStack
from services.stacks.studio_stack import StudioStack


class Services(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, env_name="sandbox", **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f"Building environment for {env_name}")

        # Get vpc to load connect studio to
        self.vpc = ec2.Vpc.from_lookup(
            self,
            "vpc-lookup",
            vpc_name=constants.SANDBOX_VPC_NAME
            if env_name == "sandbox"
            else constants.PROD_VPC_NAME,
            is_default=False,
        )

        print(f"VPC: {self.vpc.vpc_id}")

        sub = self.vpc.select_subnets(
            subnet_type=ec2.SubnetType[constants.SUBNET_DEPLOYMENT_TYPE]
        )
        self.private_subnet_ids = sub.subnet_ids

        print(f"Subnets to deploy to: {len(self.private_subnet_ids)}")

        self.sagemaker_studio_stack = StudioStack(
            self, "sagemaker-studio-stack", env_name, self.vpc, self.private_subnet_ids
        )

        self.studio_lifecycle_configs_nested_stack = StudioLifecycleConfigStack(
            self,
            "sagemaker-studio-lifecycle-config-nested-stack",
            env_name,
            self.sagemaker_studio_stack.cfn_domain.attr_domain_id,
        )

        self.studio_lifecycle_configs_nested_stack.add_dependency(
            self.sagemaker_studio_stack
        )
