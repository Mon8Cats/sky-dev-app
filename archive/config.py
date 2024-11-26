#
# pylint: disable=import-error
#

from google.cloud import secretmanager
import os

# Function to fetch a secret from Google Cloud Secret Manager
def get_secret(secret_name):
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("PROJECT_ID")
        if not project_id:
            raise ValueError("Environment variable 'PROJECT_ID' is not set.")
        # Construct the secret path
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None

# Fetch database secrets and other configurations
DB_USER = get_secret("db_user")  # Replace 'db_user' with your actual secret name in GCP
DB_PASSWORD = get_secret("db_password")  # Replace 'db_password' with your actual secret name in GCP
#DB_NAME = os.getenv("DB_NAME", "my_database")  # Default to 'my_database' if not set
#INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")  # Cloud SQL instance connection name
DB_NAME = os.getenv("DB_NAME", "my_database")  # Defaults to 'my_database' if not set
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")  # No default, must be provided
DB_SOCKET_PATH = f'/cloudsql/{INSTANCE_CONNECTION_NAME}'  # Unix socket path for Cloud SQL

# Ensure required configurations are available
if not DB_USER or not DB_PASSWORD or not INSTANCE_CONNECTION_NAME:
    raise RuntimeError(
        "Missing required database configuration. Ensure secrets and environment variables are properly set."
    )

# SQLAlchemy database URI for Cloud SQL over Unix socket
SQLALCHEMY_DATABASE_URI = (
    f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}'
    f'?unix_sock={DB_SOCKET_PATH}/.s.PGSQL.5432'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources

