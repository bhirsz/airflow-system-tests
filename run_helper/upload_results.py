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

import json
import subprocess
import sys
from datetime import datetime

RESULTS_TABLE = "airflow-system-tests-303516.system_tests_results.results"
QUERY_BUILDS_CMD = "gcloud builds list --filter tags='{build_id}' --format json(status,substitutions._TEST_NAME,timing.BUILD.startTime,timing.BUILD.endTime)"
INSERT_RESULTS_QUERY = "INSERT INTO `{table}` VALUES('{run_id}','{test_name}','{test_result}',TIMESTAMP('{start_time}'),TIMESTAMP('{end_time}'));"
BUILD_ID = sys.argv[1]
CMD = QUERY_BUILDS_CMD.format(build_id=BUILD_ID)


def get_builds():
    result = subprocess.run(CMD.split(), capture_output=True)
    if result.stderr:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def parse_timestamp(time_str):
    format_in = "%Y-%m-%dT%H:%M:%S.%f"
    format_out = "%Y-%m-%d %H:%M:%S"
    time_obj = datetime.strptime(time_str[:26], format_in)
    return time_obj.strftime(format_out)


builds = get_builds()
for build in builds:
    test_name = build["substitutions"]["_TEST_NAME"]
    status = build["status"]
    start_time = parse_timestamp(build["timing"]["BUILD"]["startTime"])
    end_time = parse_timestamp(build["timing"]["BUILD"]["endTime"])
    insert_query = INSERT_RESULTS_QUERY.format(
        table=RESULTS_TABLE,
        run_id=BUILD_ID,
        test_name=test_name,
        test_result=status,
        start_time=start_time,
        end_time=end_time,
    )
    insert_cmd = ["bq", "query", "--use_legacy_sql=false", insert_query]
    print(insert_cmd)
    subprocess.run(insert_cmd)
