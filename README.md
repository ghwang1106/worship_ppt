# README

## Development

```sh
# 1. Format Setting
pre-commit install
pre-commit run --all-files
python3 -m venv venv

# 2: Run using docker-compose
docker-compose up --build -d
```

## Deployment

```sh
docker-compose build
docker-compose push

gcloud run deploy worship-ppt
  --image gcr.io/seanhwangg/worship_ppt \
  --region us-central1 --platform "managed" \
  --service-account firebase-adminsdk-h70pe@seanhwangg.iam.gserviceaccount.com
```
