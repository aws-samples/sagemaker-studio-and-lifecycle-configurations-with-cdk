#!/bin/bash
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# This script installs the idle notebook auto-checker server extension to SageMaker Studio
# The original extension has a lab extension part where users can set the idle timeout via a Jupyter Lab widget.
# In this version the script installs the server side of the extension only. The idle timeout
# can be set via a command-line script which will be also created by this create and places into the
# user's home folder
#
# Installing the server side extension does not require Internet connection (as all the dependencies are stored in the
# install tarball) and can be done via VPCOnly mode.

set -eux

# timeout in minutes
export TIMEOUT_IN_MINS=60

# Should already be running in user home directory, but just to check:
cd /home/sagemaker-user

# By working in a directory starting with ".", we won't clutter up users' Jupyter file tree views
mkdir -p .auto-shutdown

# Create the command-line script for setting the idle timeout
cat > .auto-shutdown/set-time-interval.sh << EOF
#!/opt/conda/bin/python
import json
import requests
TIMEOUT=${TIMEOUT_IN_MINS}
session = requests.Session()
# Getting the xsrf token first from Jupyter Server
response = session.get("http://localhost:8888/jupyter/default/tree")
# calls the idle_checker extension's interface to set the timeout value
response = session.post("http://localhost:8888/jupyter/default/sagemaker-studio-autoshutdown/idle_checker",
            json={"idle_time": TIMEOUT, "keep_terminals": False},
            params={"_xsrf": response.headers['Set-Cookie'].split(";")[0].split("=")[1]})
if response.status_code == 200:
    print("Succeeded, idle timeout set to {} minutes".format(TIMEOUT))
else:
    print("Error!")
    print(response.status_code)
EOF
chmod +x .auto-shutdown/set-time-interval.sh

#update the studio region to use the deployment region.  Currently its set to default which will fail in a no-internet environment
sudo -E sh -c 'echo $AWS_REGION > /etc/yum/vars/awsregion'

# "wget" is not part of the base Jupyter Server image, you need to install it first if needed to download the tarball
sudo yum install -y wget jq

# Get domain id to identify the environment
DOMAIN_ID=`cat /opt/ml/metadata/resource-metadata.json | jq .DomainId | sed -e 's/^"//' -e 's/"$//'`
DOMAIN_ARN=`cat /opt/ml/metadata/resource-metadata.json | jq .ResourceArn | sed -e 's/^"//' -e 's/"$//'`
DOMAIN_NAME=`aws sagemaker describe-domain --domain-id ${DOMAIN_ID} | jq .DomainName | sed -e 's/^"//' -e 's/"$//'`
# DEPLOYMENT_TYPE=`aws sagemaker list-tags --resource-arn ${DOMAIN_ARN} | jq .Tags | jq from_entries | jq .deployment-type | sed -e 's/^"//' -e 's/"$//'`
ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
DEPLOYMENT_BUCKET="${DOMAIN_NAME}-deployment-assets-${ACCOUNT_ID}-${AWS_REGION}"

# wget -O .auto-shutdown/extension.tar.gz https://github.com/aws-samples/sagemaker-studio-auto-shutdown-extension/raw/main/sagemaker_studio_autoshutdown-0.1.5.tar.gz

# Or instead, could serve the tarball from an S3 bucket in which case "wget" would not be needed:
aws s3 cp s3://${DEPLOYMENT_BUCKET}/deployment_assets/sagemaker_studio_autoshutdown-0.1.5.tar.gz .auto-shutdown/extension.tar.gz

# Installs the extension
cd .auto-shutdown
tar xzf extension.tar.gz
cd sagemaker_studio_autoshutdown-0.1.5

# Activate studio environment just for installing extension
export AWS_SAGEMAKER_JUPYTERSERVER_IMAGE="${AWS_SAGEMAKER_JUPYTERSERVER_IMAGE:-'jupyter-server'}"
if [ "$AWS_SAGEMAKER_JUPYTERSERVER_IMAGE" = "jupyter-server-3" ] ; then
    eval "$(conda shell.bash hook)"
    conda activate studio
fi;
pip install --no-dependencies --no-build-isolation -e .
pip install amazon-codewhisperer-jupyterlab-ext
jupyter serverextension enable --py sagemaker_studio_autoshutdown
jupyter server extension enable amazon_codewhisperer_jupyterlab_ext
if [ "$AWS_SAGEMAKER_JUPYTERSERVER_IMAGE" = "jupyter-server-3" ] ; then
    conda deactivate
fi;

# Restarts the jupyter server
nohup supervisorctl -c /etc/supervisor/conf.d/supervisord.conf restart jupyterlabserver

# Waiting for 30 seconds to make sure the Jupyter Server is up and running
sleep 30

# Calling the script to set the idle-timeout and active the extension
/home/sagemaker-user/.auto-shutdown/set-time-interval.sh
