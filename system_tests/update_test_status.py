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

import subprocess
import sys
from datetime import datetime

BUILD_ID = sys.argv[1]
TEST_NAME = sys.argv[2]
TEST_STATUS = sys.argv[3]


RESULTS_TABLE = "airflow-system-tests-303516.system_tests_results.results"
INSERT_RESULTS_QUERY = "INSERT INTO `{table}` VALUES('{run_id}','{test_name}','{test_result}',TIMESTAMP('{start_time}'),TIMESTAMP('{end_time}'));"
UPDATE_RESULTS_QUERY = "UPDATE `{table}` SET status = '{test_result}', end_time = '{end_time}' WHERE execution_id = '{run_id}' AND test = '{test_name}';"


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if TEST_STATUS == "IN PROGRESS":
    query = INSERT_RESULTS_QUERY.format(
        table=RESULTS_TABLE,
        run_id=BUILD_ID,
        test_name=TEST_NAME,
        test_result=TEST_STATUS,
        start_time=get_timestamp(),
        end_time=get_timestamp(),
    )
else:
    query = UPDATE_RESULTS_QUERY.format(
        table=RESULTS_TABLE,
        run_id=BUILD_ID,
        test_name=TEST_NAME,
        test_result=TEST_STATUS,
        end_time=get_timestamp(),
    )

bq_query = ["bq", "query", "--use_legacy_sql=false", query]
subprocess.run(bq_query)
