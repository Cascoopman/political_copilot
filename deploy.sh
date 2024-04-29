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

# Deploying can take half an hour
# This is also the most expensive part
echo "Deploying the Vector Search endpoint..."
gcloud ai index-endpoints deploy-index $GCP_VS_ENDPOINT \
    --deployed-index-id=political_endpoint \
    --display-name=political_endpoint \
    --index=$GCP_VS_INDEX \
    --min-replica-count=1 \
    --region=europe-west1 \
    --project=$GCP_PROJECT_NAME \
    --machine-type=e2-standard-2

#deploying goes pretty fast
#echo "Deploying the backend image to Cloud Run..."
gcloud run deploy backend \
    --image europe-west1-docker.pkg.dev/$GCP_PROJECT_NAME/$GCP_PROJECT_NAME-default-repository/backend \
    --platform managed --region europe-west1 --quiet \
    --vpc-connector europe-west1 \
    --no-allow-unauthenticated \
    --ingress internal \
    --service-account svc-cloudrun@$GCP_PROJECT_NAME.iam.gserviceaccount.com

cd src/frontend

# Goes pretty fast
echo "Deploying the frontend to App Engine..."
gcloud app deploy \
    --appyaml app.yaml \
    --project $GCP_PROJECT_NAME \
    --service-account svc-cloudrun@$GCP_PROJECT_NAME.iam.gserviceaccount.com