# Google Cloud Summary

## GCLOUD Commands

```bash
gcloud projects list
gcloud config set project [PROJECT_ID]
gcloud config get-value project

gcloud sql connect [INSTANCE_NAME] --user=[USERNAME]
gcloud sql connect skypostgre --user=skyroot --database=devdb

INSERT INTO users (name, email) VALUES ('steve kim', 'steve.kim@test.com');
\c devdb
\dt

curl -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    https://sqladmin.googleapis.com/v1/projects/sky-root/instances/skypostgre




gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=sky-flask-app" --limit=50

```

