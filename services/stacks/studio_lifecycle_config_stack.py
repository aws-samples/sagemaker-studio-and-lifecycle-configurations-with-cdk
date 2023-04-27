# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    # Duration,
    NestedStack,
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
from services.constructs.sagemaker_studio_lifecycle_config_resource import (
    SageMakerStudioLifecycleConfigResource,
)


class StudioLifecycleConfigStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        domain_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # custom cf resource to deploy lifecycle
        aws_custom = SageMakerStudioLifecycleConfigResource(
            self,
            "studio-lifecycle-config-auto-shutdown",
            domain_id=domain_id,
            env_name=env_name,
        )
