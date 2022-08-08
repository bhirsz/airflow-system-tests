#!/usr/bin/env bash
set -e

TEST_PATH=$1
ENV_ID=$2
TAG_NAME=$3
TEST_FILENAME="${TEST_PATH##*/}"
TEST_WITHOUT_PY="${TEST_FILENAME%.py}"

echo "Running test: ${TEST_WITHOUT_PY}"

gcloud builds submit . \
    --config run_single_test.yaml \
    --timeout=3600 \
    --substitutions _TEST="${TEST_PATH}",_ENV_ID="${ENV_ID}",_TEST_NAME="${TEST_WITHOUT_PY}",_TAG_NAME="${TAG_NAME}" \
    --async