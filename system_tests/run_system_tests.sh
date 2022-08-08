#!/usr/bin/env bash
set -e

ENV_ID=$1
TAG_NAME=$2
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LIST_FILE=$DIR/tests.txt

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