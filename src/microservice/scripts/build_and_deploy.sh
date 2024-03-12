#!/bin/bash

# Saner programming env: these switches turn some bugs into errors
set -o errexit -o pipefail -o noclobber -o nounset

# Argument parsing
while [[ "$#" -gt 0 ]]; do case $1 in
  -p|--project) project="$2"; shift;;
  -n|--name) name="$2"; shift;;
  --vpc-connector) connector="$2"; shift;;
  -sa-id|--service-account-id) service_account_id="$2"; shift;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

[ -n "${project-}" ] || (echo "Missing required argument '--project'" && exit 1)
[ -n "${name-}" ] || (echo "Missing required argument '--name'" && exit 1)
[ -n "${service_account_id-}" ] || service_account_id="svc-cloudrun"

optional_arguments=""
if [ -n "${connector-}" ]; then
  optional_arguments+=" --vpc-connector ${connector}"
  optional_arguments+=" --ingress internal"
fi

service_account="${service_account_id}@${project}.iam.gserviceaccount.com"

echo "Building the docker image..."
gcloud builds submit . -t europe-west1-docker.pkg.dev/${project}/${project}-default-repository/${name} --project ${project}

echo "Deploying the image to Cloud Run..."
gcloud run deploy ${name} \
    --image europe-west1-docker.pkg.dev/${project}/${project}-default-repository/${name} \
    --platform managed --region europe-west1 --quiet ${optional_arguments} \
    --service-account ${service_account}
