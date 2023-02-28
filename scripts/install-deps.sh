#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

set -o errexit
set -o verbose

npm install -g aws-cdk

echo "Install NPM Deps"
# Install AWS CDK Toolkit locally
npm install

echo "Install Python Deps"
# Install project dependencies
pip install -r requirements.txt -r requirements-dev.txt
