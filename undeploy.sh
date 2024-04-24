#!/bin/bash

# Check if GCP_PROJECT_NAME environment variable is set
if [ -z "$GCP_PROJECT_NAME" ]; then
    echo "GCP_PROJECT_NAME environment variable is not set. Please set it and try again."
    exit 1
fi

# Check if vector search index variable is set
if [ -z "$GCP_VS_INDEX" ]; then
    echo "GCP_VS_INDEX variable is not set. Please set it and try again."
    exit 1
fi

# Check if vector search index variable is set
if [ -z "$GCP_VS_ENDPOINT" ]; then
    echo "GCP_VS_ENDPOINT variable is not set. Please set it and try again."
    exit 1
fi

# Instant
echo "Undeploying the Vector Search endpoint..."
gcloud ai index-endpoints undeploy-index $GCP_VS_ENDPOINT \
    --deployed-index-id=political_endpoint \
    --region=europe-west1 \
    --project=$GCP_PROJECT_NAME

# Instant
echo "Undeploying the Backend Cloud Run..."
gcloud run services delete backend --platform=managed --region=europe-west1

# Takes a few minutes
echo "WARNING: To undeploy the Frontend App Engine you must manually disable it in settings."