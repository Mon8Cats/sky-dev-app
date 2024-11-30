# Cloud SQL

## Delete instance

```bash
gcloud sql instances patch <quickstart-instance> --no-deletion-protection
gcloud sql instances describe quickstart-instance
gcloud sql instances delete quickstart-instance

```

## Change Project

```bash
gcloud projects list
gcloud config set project PROJECT_ID
gcloud sql instances list --project PROJECT_ID

```

## Sync Terraform State

```bash
terraform state rm <resource_address>
terraform state rm google_sql_database_instance.my_instance
terraform refresh

```

## Connect to Cloud SQL (PostgreSQL) from Cloud Shell

```bash
gcloud services enable sqladmin.googleapis.com
gcloud sql connect myinstance --user=postgres

CREATE DATABASE guestbook;
\connect guestbook;

CREATE TABLE entries (guestName VARCHAR(255), content VARCHAR(255),
                        entryID SERIAL PRIMARY KEY);
INSERT INTO entries (guestName, content) values ('first guest', 'I got here!');
INSERT INTO entries (guestName, content) values ('second guest', 'Me too!');
SELECT * FROM entries;
```

### Connect to Cloud SQL from Cloud Run

```bash
gcloud services enable compute.googleapis.com \
    sqladmin.googleapis.com run.googleapis.com \
    containerregistry.googleapis.com cloudbuild.googleapis.com \ servicenetworking.googleapis.com

gcloud sql instances create quickstart-instance \
--database-version=POSTGRES_14 \
 --cpu=1 \
 --memory=4GB \
 --region=us-central \
 --root-password=DB_ROOT_PASSWORD 
```

Enable APIs
- Compute Engine API
- Cloud SQL Admin API
- Cloud Run API
- Container Registry API
- Cloud Build API
- Service Networking API

### Create Instance

```bash
gcloud sql instances create quickstart-instance \
--database-version=POSTGRES_14 \
 --cpu=1 \
 --memory=4GB \
 --region=us-central \
 --root-password=skyrootpassword


 # connection name: sky-root:us-central1:quickstart-instance
 # public IP Address: 35.224.186.196
```

### Create a Database

```bash
gcloud sql databases create quickstart-db --instance=quickstart-instance
```


### Create a User

```bash
gcloud sql users create skyroot \
--instance=quickstart-instance \
--password=skyrootpassword
```

### Configure a Cloud Run Service Account

```bash
gcloud iam service-accounts list

# compute engine service account
gcloud projects add-iam-policy-binding sky-root \
  --member="serviceAccount:262659146932-compute@developer.gserviceaccount.com" \
  --role="roles/cloudsql.client"


# https://github.com/GoogleCloudPlatform/python-docs-samples
# /cloudshell_open/python-docs-samples-1/cloud-sql/postgres/sqlalchemy/ code is here  

 gcloud builds submit --tag gcr.io/sky-root/run-sql

# deploy
gcloud run deploy run-sql --image gcr.io/sky-root/run-sql \
  --add-cloudsql-instances quickstart-instance \
  --set-env-vars INSTANCE_UNIX_SOCKET="/cloudsql/sky-root:us-central1:quickstart-instance" \
  --set-env-vars INSTANCE_CONNECTION_NAME="sky-root:us-central1:quickstart-instance" \
  --set-env-vars DB_NAME="quickstart-db" \
  --set-env-vars DB_USER="skyroot" \
  --set-env-vars DB_PASS="skyrootpassword"



```

