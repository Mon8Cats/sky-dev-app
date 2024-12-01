# Cloud SQL Connections

## Overview

- pulbic (internet) or private (VPC) or both
- own connection code or tools (Cloud SQL Auth Proxy or mysql client)
- unencrypted traffic or encryption (SSL/TLS)
- how to connect?
    - public ip or private ip
- how to authorize?
    - Cloud SQL Auth Proxy, Cloud SQL connector librarires
    - Self-managed SSL/TSL certificates
    - Authorized networks
- how to authenticate?
    - Build-in database authentication


## Cloud Auth Proxy

```bash
# ./cloud-sql-proxy INSTANCE_CONNECTION_NAME & # invocation statement - use when, where?
# ./cloud-sql-proxy --unix-socket /cloudsql INSTANCE_CONNECTION_NAME &

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


## Unix Socket

```bash
# ./cloud-sql-proxy --unix-socket /cloudsql INSTANCE_CONNECTION_NAME 


import os

import sqlalchemy


def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
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
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": unix_socket_path},
        ),
        # ...
    )
    return pool

```

## Authorize with authorized networks

Client application' IP address or address range must be configured as authorized networks for the colloing conditions
- Client application is connecting directly to a Cloud SQL instance on its public IP address.
- Client application is connecting direltyl to a Cloud SQL instance on its privet IP address, and the client's IP address is a non-RFC 1918 address

```bash
gcloud sql instances patch INSTANCE_ID \
--authorized-networks=NETWORK_RANGE_1,NETWORK_RANGE_2...
    
resource "google_sql_database_instance" "instance" {
  name             = "mysql-instance-with-authorized-network"
  region           = "us-central1"
  database_version = "MYSQL_8_0"
  settings {
    tier = "db-f1-micro"
    ip_configuration {
      authorized_networks {
        name            = "Network Name"
        value           = "192.0.2.0/24"
        expiration_time = "3021-11-15T16:19:00.094Z"
      }
    }
  }
  # set `deletion_protection` to true, will ensure that one cannot accidentally delete this instance by
  # use of Terraform whereas `deletion_protection_enabled` flag protects this instance at the GCP level.
  deletion_protection = false
}
```

### Cloud Run and Cloud SQL

```bash

logger = logging.getLogger()

def init_db_connection():
    db_config = {
        'pool_size': 5,
        'max_overflow': 2,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
    return init_unix_connection_engine(db_config)

def init_unix_connection_engine(db_config):
    pool = sqlalchemy.create_engine()   
        sqlalchemy.engine.url.URL(
            dirivername="postgres+pg800",
            #host=os.environ.get('DB_HOST'),
            #port=os.environ.get('DB_PORT'),
            username=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_NAME'),
            query = {
                "unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(
                    os.environ.get('CLOUD_SQL_CONNECTION_NAME')
                )
            }
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool

db = init_db_connection()


gcloud builds submit \
    --tag gcr.io$PROJECT_ID/poll \
    --project $PROJECT_ID


gcloud run deploy poll \
    --image gcr.io/$PROJECT_ID/poll \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --add-cloudsql-instances $CONNECTION_NAME \
    --project $PROJECT_ID


```