 .. Copyright 2022 Google LLC

 .. Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

 .. Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Airflow System Tests
======================

This repository contains scripts for running Airflow system tests in CI.
Your local environment need to have gcloud tool and you need to be authenticated
to gcloud project. This project will be used to run the tests.

To run all system tests run from ``system_tests`` directory::

    gcloud builds submit .

To run single or selected system tests override _TEST_PATTERN variable. This
variable is used to find pytest test files inside tests/system directory::

    gcloud builds submit . --substitutions=_TEST_PATTERN="example*gcs*.py"

from branch: