# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from typing import Any

import boto3
import base64

client = boto3.client("sagemaker")


def on_event(event, context):
    print(event)
    request_type = event["RequestType"].lower()
    if request_type == "create":
        return on_create(event)
    if request_type == "update":
        return on_update(event)
    if request_type == "delete":
        return on_delete(event)
    raise Exception(f"Invalid request type: {request_type}")


def encode_file(file_name):
    data = open(file_name, "rb").read()
    base64_bytes = base64.b64encode(data).decode("ascii")
    return base64_bytes


def on_create(event):
    props = event["ResourceProperties"]
    print(f"create new resource with {props=}")

    # create the config
    response = client.create_studio_lifecycle_config(
        StudioLifecycleConfigName=f"sagemaker-studio-auto-shutdown-{props['domain_id']}",
        StudioLifecycleConfigContent=encode_file(
            "scripts/auto-shutdown/on-jupyter-server-start.sh"
        ),
        StudioLifecycleConfigAppType="JupyterServer",
    )
    physical_id = response["StudioLifecycleConfigArn"]
    # update the domain and attach the script
    client.update_domain(
        DomainId=props["domain_id"],
        DefaultUserSettings={
            "JupyterServerAppSettings": {
                "DefaultResourceSpec": {"LifecycleConfigArn": physical_id},
                "LifecycleConfigArns": [physical_id],
            }
        },
    )

    update_user_profiles(props["domain_id"], physical_id)

    # update existing user profiles
    return {"PhysicalResourceId": physical_id}


def on_update(event):
    props = event["ResourceProperties"]
    print(f"create new resource with {props=}")

    # delete the script
    client.delete_studio_lifecycle_config(
        StudioLifecycleConfigName=f"sagemaker-studio-auto-shutdown-{props['domain_id']}",
    )

    create_response = client.create_studio_lifecycle_config(
        StudioLifecycleConfigName=f"sagemaker-studio-auto-shutdown-{props['domain_id']}",
        StudioLifecycleConfigContent=encode_file(
            "scripts/auto-shutdown/on-jupyter-server-start.sh"
        ),
        StudioLifecycleConfigAppType="JupyterServer",
    )

    physical_id = create_response["StudioLifecycleConfigArn"]

    resp = client.update_domain(
        DomainId=props["domain_id"],
        DefaultUserSettings={
            "JupyterServerAppSettings": {
                "DefaultResourceSpec": {"LifecycleConfigArn": physical_id},
                "LifecycleConfigArns": [physical_id],
            }
        },
    )

    update_user_profiles(props["domain_id"], physical_id)

    return {"PhysicalResourceId": physical_id}


def get_users(domain_id):
    response = client.list_user_profiles(DomainIdEquals=domain_id)
    users = response["UserProfiles"]
    while "NextToken" in response:
        response = client.list_user_profiles(
            DomainIdEquals=domain_id, NextToken=users["NextToken"]
        )
        users.extend(response["UserProfiles"])

    return users


def on_delete(event):
    props = event["ResourceProperties"]
    print(f"create new resource with {props=}")

    client.delete_studio_lifecycle_config(
        StudioLifecycleConfigName=f"sagemaker-studio-auto-shutdown-{props['domain_id']}",
    )

    return {"PhysicalResourceId": None}


def update_user_profiles(domain_id, physical_id):
    users = get_users(domain_id)
    for user in users:
        client.update_user_profile(
            DomainId=domain_id,
            UserProfileName=user["UserProfileName"],
            UserSettings={
                "JupyterServerAppSettings": {
                    "DefaultResourceSpec": {"LifecycleConfigArn": physical_id},
                    "LifecycleConfigArns": [physical_id],
                }
            },
        )
