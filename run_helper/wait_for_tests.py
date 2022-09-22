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
import time

QUERY_BUILDS_CMD = "gcloud builds list --filter tags='{build_id}' --format json(status,substitutions._TEST_NAME,timing.BUILD.startTime,timing.BUILD.endTime)"
BUILD_ID = sys.argv[1]
CMD = QUERY_BUILDS_CMD.format(build_id=BUILD_ID)


def get_builds():
    result = subprocess.run(CMD.split(), capture_output=True)
    if result.stderr:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def all_builds_completed(builds):
    for build in builds:
        if build["status"] not in ("FAILURE", "SUCCESS"):
            return False
    return True


print("Waiting for tests to complete...")
while True:
    builds = get_builds()
    if all_builds_completed(builds):
        break
    time.sleep(5)
