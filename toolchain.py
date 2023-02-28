# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import pathlib
from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codecommit as codecommit
import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import pipelines
from constructs import Construct

import constants
from services.component import Services


class Toolchain(cdk.Stack):
    def __init__(self, scope: Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        repository = codecommit.Repository(
            self, "code-commit-repo", repository_name=constants.CODECOMMIT_REPO
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            cli_version=Toolchain._get_cdk_cli_version(),
            cross_account_keys=True,
            docker_enabled_for_synth=False,
            docker_enabled_for_self_mutation=False,
            publish_assets_in_parallel=False,
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(
                    repository=repository, branch=constants.CODECOMMIT_TRUNK_BRANCH
                ),
                commands=[
                    "chmod +x ./scripts/install-deps.sh",
                    "chmod +x ./scripts/run-tests.sh",
                    "./scripts/install-deps.sh",
                    "./scripts/run-tests.sh",
                    "cdk synth",
                ],
                primary_output_directory="cdk.out",
            ),
        )

        Toolchain._add_production_stage(pipeline)

        self.repo_url = cdk.CfnOutput(
            self,
            "smstudio-codecommit-repo-arn",
            value=repository.repository_arn,  # type: ignore
        )

        self.repo_clone_url_grc = cdk.CfnOutput(
            self,
            "smstudio-codecommit-repo-clone-url-grc",
            value=repository.repository_clone_url_grc,  # type: ignore
        )

        self.repo_clone_url_ssh = cdk.CfnOutput(
            self,
            "smstudio-codecommit-repo-clone-url-ssh",
            value=repository.repository_clone_url_ssh,  # type: ignore
        )

        self.repo_clone_url_http = cdk.CfnOutput(
            self,
            "smstudio-codecommit-repo-clone-url-http",
            value=repository.repository_clone_url_http,  # type: ignore
        )

    @staticmethod
    def _get_cdk_cli_version() -> str:
        package_json_path = (
            pathlib.Path(__file__).parent.joinpath("package.json").resolve()
        )
        with open(package_json_path, encoding="utf_8") as package_json_file:
            package_json = json.load(package_json_file)
        cdk_cli_version = str(package_json["devDependencies"]["aws-cdk"])
        return cdk_cli_version

    @staticmethod
    def _add_production_stage(pipeline: pipelines.CodePipeline) -> None:
        pipeline.add_stage(
            PipelineStage(
                pipeline,
                f"{constants.APP_NAME}-{constants.PRODUCTION_ENV_NAME}-pipeline-stage",
            )
        )

        # domain_id_env_var_name = "DOMAIN_ID"
        # smoke_test_commands = [f"aws sagemaker describe-domain --domain-id ${domain_id_env_var_name}"]
        # smoke_test = pipelines.ShellStep(
        #     "SmokeTest",
        #     env_from_cfn_outputs={domain_id_env_var_name: backend.sagemaker_studio_stack.domain_id},
        #     commands=smoke_test_commands,
        # )
        # pipeline.add_stage(production, post=[smoke_test])


class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Services(
            self,
            constants.APP_NAME + "-" + constants.PRODUCTION_ENV_NAME,
            env=cdk.Environment(
                account=constants.PRODUCTION_ENV_ACCOUNT,
                region=constants.PRODUCTION_ENV_REGION,
            ),
            env_name=constants.PRODUCTION_ENV_NAME,
            stack_name=constants.APP_NAME + "-" + constants.PRODUCTION_ENV_NAME,
        )
