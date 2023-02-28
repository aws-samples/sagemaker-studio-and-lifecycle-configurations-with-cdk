# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import unittest

import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import assertions
from aws_cdk import aws_ec2 as ec2
import constants

from services.stacks.studio_stack import StudioStack


class APITestCase(unittest.TestCase):
    def test_sagemaker_domain_creation(self) -> None:
        stack = cdk.Stack()

        vpc = ec2.Vpc(stack, "test-vpc")

        private_subnet_ids = [
            private_subnet.subnet_id for private_subnet in vpc.private_subnets
        ]

        studio_stack = StudioStack(
            stack,
            "StudioStack",
            vpc=vpc,
            private_subnet_ids=private_subnet_ids,
            env_name="sandbox",
        )
        template = assertions.Template.from_stack(studio_stack)

        template.resource_count_is("AWS::SageMaker::Domain", 1)


if __name__ == "__main__":
    unittest.main()
