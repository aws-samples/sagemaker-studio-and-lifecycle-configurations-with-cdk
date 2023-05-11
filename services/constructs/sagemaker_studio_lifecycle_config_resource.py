# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import aws_cdk as cdk
from aws_cdk import (
    aws_iam as iam,
    Stack,
    aws_lambda,
)
from aws_cdk.custom_resources import Provider
from constructs import Construct


class SageMakerStudioLifecycleConfigResource(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_id: str,
        env_name: str,
        timeout: cdk.Duration = cdk.Duration.minutes(5),
    ) -> None:
        super().__init__(scope, construct_id)

        account_id = Stack.of(self).account
        region = Stack.of(self).region
        stack = Stack.of(self)

        # create lambda role
        lambda_role = iam.Role(
            id="lifecycle-policy-lambda-role",
            scope=self,
            role_name=f"{construct_id}-{domain_id}-lambda-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "SagemakerStudioLifeCycleConfigProvisioningPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "sagemaker:CreateStudioLifecycleConfig",
                                "sagemaker:DeleteStudioLifecycleConfig",
                                "sagemaker:DescribeUserProfile",
                                "sagemaker:UpdateDomain",
                                "sagemaker:ListUserProfiles",
                                "sagemaker:UpdateUserProfile",
                            ],
                            resources=[
                                f"arn:aws:sagemaker:{region}:{account_id}:user-profile/{domain_id}/*",
                                f"arn:aws:sagemaker:{region}:{account_id}:domain/{domain_id}",
                                f"arn:aws:sagemaker:{region}:{account_id}:studio-lifecycle-config/sagemaker-studio-auto-shutdown-{domain_id}",
                            ],
                            effect=iam.Effect.ALLOW,
                        )
                    ]
                )
            },
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        event_handler = aws_lambda.Function(
            scope=self,
            id="lifecycle-policy-lambda-function",
            function_name=f"{construct_id}-{domain_id}-handler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset("lambda"),
            handler="custom-resource-studio-lifecycle-config.on_event",
            role=lambda_role,
            environment={"environment": env_name},
            timeout=timeout,
        )

        provider = Provider(
            scope=self,
            id="lifecycle-policy-lambda-function-provider",
            provider_function_name=f"{construct_id}-{domain_id}-provider",
            on_event_handler=event_handler,
        )

        cdk.CustomResource(
            scope=self,
            id=f"{construct_id}StudioLifecycleConfig",
            service_token=provider.service_token,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_type="Custom::StudioLifecycleConfig",
            properties={"domain_id": domain_id, "version": "5"},
        )
