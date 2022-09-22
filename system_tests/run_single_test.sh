#!/usr/bin/env bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

TEST_PATH=$1
ENV_ID=$2
TAG_NAME=$3
TEST_FILENAME="${TEST_PATH##*/}"
TEST_WITHOUT_PY="${TEST_FILENAME%.py}"

echo "Running test: ${TEST_WITHOUT_PY}"

gcloud builds submit . \
    --config run_single_test.yaml \
    --timeout=7200 \
    --substitutions _TEST="${TEST_PATH}",_ENV_ID="${ENV_ID}",_TEST_NAME="${TEST_WITHOUT_PY}",_TAG_NAME="${TAG_NAME}" \
    --async