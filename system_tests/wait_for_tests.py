import sys
import subprocess
import json
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

