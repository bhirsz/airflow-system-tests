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

set -exo pipefail

cd system_tests/airflow/

python3.7 -m pipx install --editable ./dev/breeze/
python3.7 -m pipx ensurepath

export DOCKER_BUILDKIT=1
PATH=$PATH:/builder/home/.local/bin
# TODO replace latest with commit SHA
# TODO pass whole tag from cloudbuild.yaml?
breeze ci-image build --tag-as-latest