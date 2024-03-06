# Deployment Guide


## Set the project in gcloud

```
gcloud config set project to-be-decided
```


### Deploy to Cloud Run

To deploy the API to Cloud Run, run the included `build_and_deploy.sh` script:
```
./scripts/build_and_deploy.sh --project to-be-decided --name microservice --service-account-id svc-cloudrun \
    --service-account-esp-id svc-cloudrun-esp
```

