
# pylint: disable=import-error

from flask import Flask
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

# Test the database connection during app startup
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("Database connected successfully!")
    connection.close()  # Close the connection after the test
except Exception as e:
    print(f"Database connection failed: {e}")
    # Continue running the app, but log the error
    app.logger.error(f"Database connection failed: {e}")

# Swagger configuration
app.config["API_TITLE"] = "User API"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Routes and additional setup
@app.route("/")
def home():
    return "Welcome to the User API. Visit /swagger to explore the API."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)