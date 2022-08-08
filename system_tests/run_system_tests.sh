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

ENV_ID=$1
TAG_NAME=$2
LIST_FILE=$3
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ ! -f "${LIST_FILE}" ]]; then
    echo "File does not exist."
    exit 1
fi

while read line; do
    if grep "#" <<< "${line}" > /dev/null ; then
        continue
    fi

    if [[ -z "${line}" ]] ; then
        continue
    fi
    . $DIR/run_single_test.sh $line $ENV_ID $TAG_NAME
done < ${LIST_FILE}

echo
echo "List runs with command:"
echo
echo "gcloud builds list --filter \"tags='${TAG_NAME}'\" --format=\"table[box,margin=3,title='system tests'](id,status,tags,logUrl)\""
echo