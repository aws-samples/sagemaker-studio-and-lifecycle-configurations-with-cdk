# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    # Duration,
    NestedStack,
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
from ..ref import jupyter_versions


class StudioStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env_name: str,
        vpc: ec2.Vpc,
        private_subnet_ids,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id = Stack.of(self).account
        region = Stack.of(self).region
        stack = Stack.of(self)
        jp_version_string = jupyter_versions.get_version(
            region=region, version=constants.JUPYTERLAB_DEFAULT
        )

        # add kms for sagemaker domain
        sagemaker_studio_kms_key = kms.Key(
            self,
            "sm-studio-kms-key",
            alias=f"{constants.SAGEMAKER_DOMAIN_NAME_PREFIX}-{env_name}-sm-studio-kms-key",
            enable_key_rotation=True,
        )

        sagemaker_studio_sharing_s3_bucket = s3.Bucket(
            self,
            "s3-bucket-sms-sharing",
            encryption_key=sagemaker_studio_kms_key,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
        )

        # Setup roles and policies
        policy_sagemaker_studio_domain = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListBucket",
                    ],
                    resources=["arn:aws:s3:::*"],
                    effect=iam.Effect.ALLOW,
                )
            ]
        )

        policy_sagemaker_studio_kms = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "kms:Decrypt",
                        "kms:Encrypt",
                        "kms:CreateGrant",
                        "kms:DescribeKey",
                    ],
                    resources=[sagemaker_studio_kms_key.key_arn],
                    effect=iam.Effect.ALLOW,
                )
            ]
        )

        role_principal = (
            iam.CompositePrincipal(
                iam.ServicePrincipal("sagemaker.amazonaws.com"),
                iam.ServicePrincipal("glue.amazonaws.com"),
            )
            if constants.ADD_GLUE_PERMISSION
            else iam.ServicePrincipal("sagemaker.amazonaws.com")
        )

        role_sagemaker_studio_domain = iam.Role(
            self,
            "role-for-sagemaker-studio-users",
            assumed_by=role_principal,
            role_name=f"{constants.SAGEMAKER_DOMAIN_NAME_PREFIX}-{env_name}-role-sagemaker-studio-users",
            inline_policies={
                "policy_sagemaker_studio_domain": policy_sagemaker_studio_domain,
                "policy_sagemaker_studio_kms": policy_sagemaker_studio_kms,
            },
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    id="SagemakerFullAccess",
                    managed_policy_arn="arn:aws:iam::aws:policy/AmazonSageMakerFullAccess",
                )
            ],
        )

        if constants.ADD_GLUE_PERMISSION:
            # Policy for Glue
            policy_sagemaker_studio_glue_interactive_sessions = iam.PolicyStatement(
                actions=["sts:GetCallerIdentity", "iam:GetRole", "iam:Passrole"],
                resources=["*"],
                effect=iam.Effect.ALLOW,
            )

            role_sagemaker_studio_domain.add_to_policy(
                policy_sagemaker_studio_glue_interactive_sessions
            )

            role_sagemaker_studio_domain.add_managed_policy(
                iam.ManagedPolicy.from_managed_policy_arn(
                    self,
                    id="AwsGlueSessionUserRestrictedServiceRole",
                    managed_policy_arn="arn:aws:iam::aws:policy/service-role/AwsGlueSessionUserRestrictedServiceRole",
                )
            )

        # Create security groups
        sagemaker_security_group = ec2.SecurityGroup(
            self,
            "security-group-for-sagemaker-studio",
            vpc=vpc,
            security_group_name=f"{constants.SAGEMAKER_DOMAIN_NAME_PREFIX}-{env_name}-sagemaker-studio-sg",
            allow_all_outbound=True,
        )
        sagemaker_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(cidr_ip=vpc.vpc_cidr_block),
            connection=ec2.Port.all_tcp(),
        )

        self.security_groups = [sagemaker_security_group.security_group_id]

        self.cfn_domain = sagemaker.CfnDomain(
            self,
            "sagemaker-studio-domain",
            auth_mode=constants.AUTH_TYPE,
            default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
                execution_role=role_sagemaker_studio_domain.role_arn,
                security_groups=self.security_groups,
                sharing_settings=sagemaker.CfnDomain.SharingSettingsProperty(
                    notebook_output_option="Allowed",
                    s3_kms_key_id=sagemaker_studio_kms_key.key_id,
                    s3_output_path=f"s3://{sagemaker_studio_sharing_s3_bucket.bucket_name}/shared_notebooks/",
                ),
                jupyter_server_app_settings=sagemaker.CfnDomain.JupyterServerAppSettingsProperty(
                    default_resource_spec=sagemaker.CfnDomain.ResourceSpecProperty(
                        sage_maker_image_arn=jp_version_string
                    )
                ),
            ),
            domain_name=constants.SAGEMAKER_DOMAIN_NAME_PREFIX + "-" + env_name,
            subnet_ids=private_subnet_ids,
            vpc_id=vpc.vpc_id,
            # the properties below are optional
            app_network_access_type="VpcOnly",
            kms_key_id=sagemaker_studio_kms_key.key_id,
            tags=[CfnTag(key="project", value="analytics-environment")],
        )

        self.domain_id = cdk.CfnOutput(
            self,
            "sagemaker_studio_domain_id",
            # API doesn't disable create_default_stage, hence URL will be defined
            value=self.cfn_domain.attr_domain_id,  # type: ignore
        )
