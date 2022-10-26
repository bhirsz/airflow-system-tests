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

Setup
----------------------

You can configure project used for test execution by running::

    gcloud config set project PROJECT_ID

Apache Airflow community uses ``apache-airflow-testing`` project.

It may be needed to re-authenticate::

    gcloud auth application-default login
    gcloud auth login

Before first run you need to build the image for building the Airflow CI images.
Run following from the ``test_runner_builder`` directory::

    gcloud builds submit .

This image needs to be build only once per project.

Running the tests
------------------

To run all system tests run from the ``system_tests`` directory::

    gcloud builds submit .

To run single or selected system tests override _TEST_PATTERN variable. This
variable is used to find pytest test files inside tests/system directory::

    gcloud builds submit . --substitutions=_TEST_PATTERN="example*gcs*.py"

from branch::

    gcloud builds submit . --substitutions=_BRANCH=<branch_name>

Tests overview
---------------
Cloud Build steps:
 - clone the Airflow repository
 - build test runner image
 - Discover tests to run
 - For every system test trigger separate Cloud Build:
   - Set test state in BigQuery ``system_tests_results.results`` table to IN PROGRESS
   - Run the test
   - Update test state in BigQuery ``system_tests_results.results`` table with test state

After the tests finish you can check their results in ``system_tests_results.results`` BigQuery table.
Individual test results are also visible in triggered Cloud Builds.
