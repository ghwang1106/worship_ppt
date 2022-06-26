# README

## Development

```sh
# 1. Format Setting
pre-commit install
pre-commit run --all-files
python3 -m venv venv

# 2. Run using docker-compose
docker-compose up --build
```

## Deployment

```sh
# 1. Push simage
docker-compose build
docker-compose push

# 2. Deploy image
gcloud run deploy worship-ppt \
  --image gcr.io/seanhwangg/worship_ppt \
  --region us-central1
```
