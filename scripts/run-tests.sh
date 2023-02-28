#!/bin/bash

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

set -o errexit
set -o verbose

targets=(services tests app.py constants.py toolchain.py)

# Find common security issues (https://bandit.readthedocs.io)
bandit --recursive "${targets[@]}"

# Python code formatter (https://black.readthedocs.io)
black --check --diff "${targets[@]}"

# Report code complexity (https://radon.readthedocs.io)
radon mi "${targets[@]}"

# Exit with non-zero status if code complexity exceeds thresholds (https://xenon.readthedocs.io)
xenon --max-absolute A --max-modules A --max-average A "${targets[@]}"

# Run tests and measure code coverage (https://coverage.readthedocs.io)
coverage run --source "${PWD}" --omit "/venv/.venv/*,tests/*" -m unittest discover -v -s tests
