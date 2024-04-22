#!/bin/bash

# Check if GCP_PROJECT_NAME environment variable is set
if [ -z "$GCP_PROJECT_NAME" ]; then
    echo "GCP_PROJECT_NAME environment variable is not set. Please set it and try again."
    exit 1
fi

# Building takes few minutes, 
echo "Building the docker image..."
gcloud builds submit . -t europe-west1-docker.pkg.dev/$GCP_PROJECT_NAME/$GCP_PROJECT_NAME-default-repository/backend --project $GCP_PROJECT_NAME
