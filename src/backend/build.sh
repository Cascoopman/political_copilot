\\ DEPLOY
gcloud ai index-endpoints deploy-index 6945474215172636672 \
    --deployed-index-id=political_endpoint \
    --display-name=political_endpoint \
    --index=6394812403703349248 \
    --min-replica-count=1 \
    --max-replica-count=2 \
    --region=europe-west1 \
    --project=cedar-talent-417009 \                             
    --machine-type=e2-standard-2


\\ UNDEPLOY
gcloud ai index-endpoints undeploy-index 6945474215172636672 \
    --deployed-index-id=political_endpoint \
    --region=europe-west1 \
    --project=cedar-talent-417009