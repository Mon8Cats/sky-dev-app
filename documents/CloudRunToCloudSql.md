# Cloud Run to Cloud SQL

## Enable APIs

```bash
gcloud services enable compute.googleapis.com sqladmin.googleapis.com run.googleapis.com \
containerregistry.googleapis.com cloudbuild.googleapis.com servicenetworking.googleapis.com


```

## Create a SQL instance 

```bash
# SQL Instance
gcloud sql instances create quickstart-instance \
--database-version=POSTGRES_14 \
 --cpu=1 \
 --memory=4GB \
 --region=us-central \
 --root-password=rootpassword

 # DB
 gcloud sql databases create quickstart-db --instance=quickstart-instance

# User
gcloud sql users create quickstart-user \
--instance=quickstart-instance \
--password=userpassword

```

## Configure Cloud Run Service Account

```bash
gcloud iam service-accounts list
# DISPLAY NAME: Default compute service account
# EMAIL: 262659146932-compute@developer.gserviceaccount.com

# add Cloud SQL Cient role
gcloud projects add-iam-policy-binding sky-root \
  --member="serviceAccount:262659146932-compute@developer.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

## Configure a Cloud SQL app

```bash
gcloud builds submit --tag gcr.io/sky-root/run-sql

# code: https://github.com/GoogleCloudPlatform/python-docs-samples

# cloudshell_open --repo_url "https://github.com/GoogleCloudPlatform/python-docs-samples" --dir "cloud-sql/postgres/sqlalchemy" --page "editor" --force_new_clone
# 2024/11/30 16:26:42 Cloning https://github.com/GoogleCloudPlatform/python-docs-samples into /home/stone2root/cloudshell_open/python-docs-samples
# Cloning into '/home/stone2root/cloudshell_open/python-docs-samples'...
# remote: Enumerating objects

# ~/cloudshell_open/python-docs-samples/cloud-sql/postgres/sqlalchemy

# Build a Docker container and publish it to Container Registry
gcloud builds submit --tag gcr.io/sky-root/run-sql

# Deploy the app
gcloud run deploy run-sql --image gcr.io/sky-root/run-sql \
  --add-cloudsql-instances sky-root:us-central1:quickstart-instance \
  --set-env-vars INSTANCE_UNIX_SOCKET="/cloudsql/sky-root:us-central1:quickstart-instance" \
  --set-env-vars INSTANCE_CONNECTION_NAME="sky-root:us-central1:quickstart-instance" \
  --set-env-vars DB_NAME="quickstart-db" \
  --set-env-vars DB_USER="quickstart-user" \
  --set-env-vars DB_PASS="userpassword"

gcloud run deploy run-sql --image gcr.io/sky-root/run-sql \
  --add-cloudsql-instances sky-root:us-central1:quickstart-instance \
  --set-env-vars INSTANCE_UNIX_SOCKET="/cloudsql/sky-root:us-central1:quickstart-instance" \
  --set-env-vars INSTANCE_CONNECTION_NAME="sky-root:us-central1:quickstart-instance" \
  --set-env-vars DB_NAME="quickstart-db" \
  --set-env-vars DB_USER="quickstart-user" \
  --set-env-vars DB_PASS="userpassword"


```


## Use My SQL

```bash
gcloud sql instances describe INSTANCE_NAME
gcloud run services describe CLOUD_RUN_SERVICE_NAME
--region CLOUD_RUN_SERVICE_REGION --format="value(spec.template.spec.serviceAccountName)"
   
# Service Account: Cloud SQL Client, Cloud SQL Admin, cloudsql.instances.connect, cloudsql.instances.get


gcloud run deploy \
  --image=IMAGE \
  --add-cloudsql-instances=INSTANCE_CONNECTION_NAME

gcloud run services update SERVICE_NAME \
  --add-cloudsql-instances=INSTANCE_CONNECTION_NAME


resource "google_cloud_run_v2_service" "default" {
  name     = "cloudrun-service"
  location = "us-central1"

  deletion_protection = false # set to "true" in production

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello:latest" # Image to deploy

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.default.connection_name]
      }
    }
  }
  client     = "terraform"
  depends_on = [google_project_service.secretmanager_api, google_project_service.cloudrun_api, google_project_service.sqladmin_api]
}

```

```bash
# public IP:
import os

import sqlalchemy


def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a Unix socket connection pool for a Cloud SQL instance of Postgres."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    unix_socket_path = os.environ[
        "INSTANCE_UNIX_SOCKET"
    ]  # e.g. '/cloudsql/project:region:instance'

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<INSTANCE_UNIX_SOCKET>/.s.PGSQL.5432
        # Note: Some drivers require the `unix_sock` query parameter to use a different key.
        # For example, 'psycopg2' uses the path set to `host` in order to connect successfully.
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_sock": f"{unix_socket_path}/.s.PGSQL.5432"},
        ),
        # ...
    )
    return pool

----- Cloud SQL connectors= language specific
import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

import sqlalchemy


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool


--- secret manager
gcloud run services update SERVICE_NAME \
  --add-cloudsql-instances=INSTANCE_CONNECTION_NAME
  --update-env-vars=INSTANCE_CONNECTION_NAME=INSTANCE_CONNECTION_NAME_SECRET \
  --update-secrets=DB_USER=DB_USER_SECRET:latest \
  --update-secrets=DB_PASS=DB_PASS_SECRET:latest \
  --update-secrets=DB_NAME=DB_NAME_SECRET:latest



--- private IP:
import os
import ssl

import sqlalchemy


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of Postgres."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_host = os.environ[
        "INSTANCE_HOST"
    ]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    db_port = os.environ["DB_PORT"]  # e.g. 5432

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
        # ...
    )
    return pool


```