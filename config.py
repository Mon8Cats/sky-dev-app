#
# pylint: disable=import-error
#

from google.cloud import secretmanager
import os

def get_secret(secret_name):
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("PROJECT_ID")
        if not project_id:
            raise ValueError("Environment variable 'PROJECT_ID' is not set.")
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None

# Fetch secrets with error handling
DB_USER = get_secret("db_user") or "default_user"
DB_PASSWORD = get_secret("db_password") or "default_password"
DB_NAME = os.getenv("DB_NAME", "my_database")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

# Database connection configuration
DB_SOCKET_PATH = f'/cloudsql/{INSTANCE_CONNECTION_NAME}'

if not DB_USER or not DB_PASSWORD or not INSTANCE_CONNECTION_NAME:
    print("Missing required database configuration. Check your environment variables.")

SQLALCHEMY_DATABASE_URI = (
    f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}'
    f'?unix_sock={DB_SOCKET_PATH}/.s.PGSQL.5432'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
