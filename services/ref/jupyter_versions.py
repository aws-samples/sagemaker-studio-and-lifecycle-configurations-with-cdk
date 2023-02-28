# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

jupyter_lab_versions_map = [
    {
        "Region": "us-east-1",
        "JL1": "arn:aws:sagemaker:us-east-1:081325390199:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:us-east-1:081325390199:image/jupyter-server-3",
    },
    {
        "Region": "us-east-2",
        "JL1": "arn:aws:sagemaker:us-east-2:429704687514:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:us-east-2:429704687514:image/jupyter-server-3",
    },
    {
        "Region": "us-west-1",
        "JL1": "arn:aws:sagemaker:us-west-1:742091327244:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:us-west-1:742091327244:image/jupyter-server-3",
    },
    {
        "Region": "us-west-2",
        "JL1": "arn:aws:sagemaker:us-west-2:236514542706:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:us-west-2:236514542706:image/jupyter-server-3",
    },
    {
        "Region": "af-south-1",
        "JL1": "arn:aws:sagemaker:af-south-1:559312083959:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:af-south-1:559312083959:image/jupyter-server-3",
    },
    {
        "Region": "ap-east-1",
        "JL1": "arn:aws:sagemaker:ap-east-1:493642496378:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ap-east-1:493642496378:image/jupyter-server-3",
    },
    {
        "Region": "ap-south-1",
        "JL1": "arn:aws:sagemaker:ap-south-1:394103062818:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ap-south-1:394103062818:image/jupyter-server-3",
    },
    {
        "Region": "ap-northeast-2",
        "JL1": "arn:aws:sagemaker:ap-northeast-2:806072073708:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ap-northeast-2:806072073708:image/jupyter-server-3",
    },
    {
        "Region": "ap-southeast-1",
        "JL1": "arn:aws:sagemaker:ap-southeast-1:492261229750:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ap-southeast-1:492261229750:image/jupyter-server-3",
    },
    {
        "Region": "ap-southeast-2",
        "JL1": "arn:aws:sagemaker:ap-southeast-2:452832661640:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ap-southeast-2:452832661640:image/jupyter-server-3",
    },
    {
        "Region": "ap-northeast-1",
        "JL1": "arn:aws:sagemaker:ap-northeast-1:102112518831:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ap-northeast-1:102112518831:image/jupyter-server-3",
    },
    {
        "Region": "ca-central-1",
        "JL1": "arn:aws:sagemaker:ca-central-1:310906938811:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:ca-central-1:310906938811:image/jupyter-server-3",
    },
    {
        "Region": "eu-central-1",
        "JL1": "arn:aws:sagemaker:eu-central-1:936697816551:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:eu-central-1:936697816551:image/jupyter-server-3",
    },
    {
        "Region": "eu-west-1",
        "JL1": "arn:aws:sagemaker:eu-west-1:470317259841:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:eu-west-1:470317259841:image/jupyter-server-3",
    },
    {
        "Region": "eu-west-2",
        "JL1": "arn:aws:sagemaker:eu-west-2:712779665605:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:eu-west-2:712779665605:image/jupyter-server-3",
    },
    {
        "Region": "eu-west-3",
        "JL1": "arn:aws:sagemaker:eu-west-3:615547856133:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:eu-west-3:615547856133:image/jupyter-server-3",
    },
    {
        "Region": "eu-north-1",
        "JL1": "arn:aws:sagemaker:eu-north-1:243637512696:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:eu-north-1:243637512696:image/jupyter-server-3",
    },
    {
        "Region": "eu-south-1",
        "JL1": "arn:aws:sagemaker:eu-south-1:592751261982:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:eu-south-1:592751261982:image/jupyter-server-3",
    },
    {
        "Region": "sa-east-1",
        "JL1": "arn:aws:sagemaker:sa-east-1:782484402741:image/jupyter-server",
        "JL3": "arn:aws:sagemaker:sa-east-1:782484402741:image/jupyter-server-3",
    },
]


def get_version(region, version="JL3"):
    return next(
        (
            item[version]
            for item in jupyter_lab_versions_map
            if item["Region"] == region
        ),
        None,
    )
