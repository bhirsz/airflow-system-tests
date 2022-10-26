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

fetch_project_number() {
  project_number=$(\
    gcloud projects list \
      --filter="PROJECT_ID=$project_name" \
      --format="value(PROJECT_NUMBER)" \
  )
  echo "This project is going to be set up to support System Tests execution:"
  echo "${project_name} (${project_number})"
  echo ""
}

enable_required_apis() {
  echo "*** Enabling required APIs:"

  list_of_apis=(
    "artifactregistry.googleapis.com"
    "appengine.googleapis.com"
    "bigquery.googleapis.com"
    "bigquerystorage.googleapis.com"
    "cloudapis.googleapis.com"
    "cloudbuild.googleapis.com"
    "clouddebugger.googleapis.com"
    "cloudfunctions.googleapis.com"
    "cloudresourcemanager.googleapis.com"
    "cloudtrace.googleapis.com"
    "composer.googleapis.com"
    "compute.googleapis.com"
    "computescanning.googleapis.com"
    "container.googleapis.com"
    "containeranalysis.googleapis.com"
    "containerregistry.googleapis.com"
    "dataflow.googleapis.com"
    "datalineage.googleapis.com"
    "dataproc.googleapis.com"
    "datastore.googleapis.com"
    "deploymentmanager.googleapis.com"
    "firebaserules.googleapis.com"
    "firestore.googleapis.com"
    "iam.googleapis.com"
    "iamcredentials.googleapis.com"
    "logging.googleapis.com"
    "monitoring.googleapis.com"
    "oslogin.googleapis.com"
    "pubsub.googleapis.com"
    "replicapool.googleapis.com"
    "replicapoolupdater.googleapis.com"
    "resourceviews.googleapis.com"
    "servicemanagement.googleapis.com"
    "serviceusage.googleapis.com"
    "source.googleapis.com"
    "sql-component.googleapis.com"
    "sqladmin.googleapis.com"
    "storage-api.googleapis.com"
    "storage-component.googleapis.com"
  )

  for api_name in "${list_of_apis[@]}"; do
    echo "Enabling ${api_name}..."
    gcloud services enable "$api_name" "--project=${project_name}"
  done

  echo ""
}

setup_iam_policies() {
  echo "*** Setting up required IAM policies..."
  echo ""
  read -r -d '' iam_policy_yaml << END_OF_POLICY
bindings:
- members:
  - serviceAccount:${project_number}@cloudbuild.gserviceaccount.com
  role: roles/bigquery.admin
- members:
  - serviceAccount:${project_number}@cloudbuild.gserviceaccount.com
  - serviceAccount:${project_number}-compute@developer.gserviceaccount.com
  role: roles/storage.admin
- members:
  - serviceAccount:${project_number}@cloudbuild.gserviceaccount.com
  role: roles/cloudbuild.editor
- members:
  - serviceAccount:${project_number}-compute@developer.gserviceaccount.com
  - serviceAccount:${project_number}@cloudservices.gserviceaccount.com
  - serviceAccount:service-${project_number}@containerregistry.iam.gserviceaccount.com
  role: roles/editor
- members:
  - serviceAccount:${project_number}-compute@developer.gserviceaccount.com
  role: roles/container.admin
- members:
  - user:rafalbiegacz@google.com
  - user:bartomiejh@google.com
  role: roles/owner
- members:
  - user:kaxilnaik@apache.org
  - user:kosteev@google.com
  - user:wyszomirski@google.com
  - user:potiuk@apache.org
  - user:ash@apache.org
  role: roles/editor
END_OF_POLICY

  temporary_iam_policy_file_name=$(mktemp --suffix=".yaml")
  echo "${iam_policy_yaml}" >> "${temporary_iam_policy_file_name}"
  echo "This policy is going to be applied"
  echo "(reading from temporary file: '${temporary_iam_policy_file_name}'):"
  echo ""
  cat "${temporary_iam_policy_file_name}"

  gcloud projects set-iam-policy "${project_name}" \
    "${temporary_iam_policy_file_name}"

  echo ""
}

main() {
  fetch_project_number
  # enable_required_apis
  setup_iam_policies
}

project_name=$1
main
