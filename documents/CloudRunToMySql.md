# Cloud Run to My SQL

## Cloud SQL connections

- how to connect
  - an internal, VPC-only (private) IP address
  - an external, internet-accessible (public) IP address
- How to authorize
  - Cloud SQL Auth Proxy and Cloud SQL connector libraries
  - Self-managed SSL/TLS certificates
  - Authorized networks
- How to authenticate
  - Built-in database authentication - log in with a username/password
- Code Sample

```bash
# cloud sql auth proxy invocation statement
./cloud-sql-proxy INSTANCE_CONNECTION_NAME &

# code
import os

import sqlalchemy


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
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
    db_port = os.environ["DB_PORT"]  # e.g. 3306

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
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

## Set up a Cloud SQL instance

```bash
# https://cloud.google.com/sql/docs/mysql/connect-instance-cloud-shell

gcloud auth list
gcloud projects list
gcloud config set project [project_id]
gcloud config get-value project
gcloud services enable sqladmin.googleapis.com

# 1) create a cloud sql instance
myinstance, rootpassword
# create instance
public ip = 34.171.57.171
connection name = sky-root:us-central1:myinstance

# 2) connect to my instance 
gcloud sql connect myinstance --user=root
then enter password: 

CREATE DATABASE guestbook;

USE guestbook;
CREATE TABLE entries (guestName VARCHAR(255), content VARCHAR(255),
    entryID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(entryID));
    INSERT INTO entries (guestName, content) values ("first guest", "I got here!");
    INSERT INTO entries (guestName, content) values ("second guest", "Me too!");

SELECT * FROM entries;

quit

gcloud sql instances delete [INSTANCE_NAME]

```

## Connect to Cloud SQL for MySQL from Cloud Run

```bash
 gcloud sql instances create quickstart-instance \
--database-version=MYSQL_8_0 \
--cpu=1 \
--memory=4GB \
--region=us-central1 \
--root-password=rootpassword
# 35.226.128.51
# sky-root:us-central1:quickstart-instance


gcloud sql databases create quickstart-db --instance=quickstart-instance

gcloud sql users create quickstart-user \
--instance=quickstart-instance \
--password=userpassword

gcloud iam service-accounts list
# EMAIL: 262659146932-compute@developer.gserviceaccount.com


gcloud projects add-iam-policy-binding sky-root \
  --member="serviceAccount:262659146932-compute@developer.gserviceaccount.com" \
  --role="roles/cloudsql.client"

# Code
# clone https://github.com/GoogleCloudPlatform/python-docs-samples
# directory ~/cloudshell_open/python-docs-samples/cloud-sql/mysql/sqlalchemy 

# build
gcloud builds submit --tag gcr.io/sky-root/run-sql


# deploy
gcloud run deploy run-sql --image gcr.io/sky-root/run-sql \
  --add-cloudsql-instances sky-root:us-central1:quickstart-instance \
  --set-env-vars INSTANCE_UNIX_SOCKET="/cloudsql/sky-root:us-central1:quickstart-instance" \
  --set-env-vars INSTANCE_CONNECTION_NAME="sky-root:us-central1:quickstart-instance" \
  --set-env-vars DB_NAME="quickstart-db" \
  --set-env-vars DB_USER="quickstart-user" \
  --set-env-vars DB_PASS="userpassword"



```



### Update Password

```bash
gcloud secrets versions access latest --secret=db_password
echo -n "NEW_SECRET_VALUE" | gcloud secrets versions add db_password --data-file=-
gcloud secrets versions list db_password
gcloud secrets versions disable VERSION_ID --secret=db_password
gcloud secrets versions destroy VERSION_ID --secret=db_password



```



References

```bash
https://github.com/GoogleCloudPlatform/cloud-sql-python-connector
https://cloud.google.com/sql/docs/mysql/connect-run

```