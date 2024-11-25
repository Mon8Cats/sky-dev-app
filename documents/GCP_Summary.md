# Google Cloud Summary

## GCLOUD Commands

```bash
gcloud projects list
gcloud config set project [PROJECT_ID]
gcloud config get-value project

gcloud sql connect [INSTANCE_NAME] --user=[USERNAME]
gcloud sql connect skypostgre --user=skyroot --database=[DATABASE_NAME]

INSERT INTO users (name, email) VALUES ('steve kim', 'steve.kim@test.com');
\c devdb
\dt
```

