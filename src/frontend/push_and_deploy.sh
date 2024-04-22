#!/bin/bash

# Check if GCP_PROJECT_NAME environment variable is set
if [ -z "$GCP_PROJECT_NAME" ]; then
    echo "GCP_PROJECT_NAME environment variable is not set. Please set it and try again."
    exit 1
fi

# Goes pretty fast
echo "Deploying the frontend to App Engine..."
gcloud app deploy \
    --appyaml app.yaml \
    --project $GCP_PROJECT_NAME \
    --service-account svc-cloudrun@$GCP_PROJECT_NAME.iam.gserviceaccount.com