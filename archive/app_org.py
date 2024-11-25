
# pylint: disable=import-error

from flask import Flask
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import config  # Import the database configuration
from config import SQLALCHEMY_DATABASE_URI
import logging



# Initialize the Flask app and SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["API_TITLE"] = "User API"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

db = SQLAlchemy(app)  # Database instance
api = Api(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test the database connection during app startup
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("Database connected successfully!")
    connection.close()  # Close the connection after the test
except Exception as e:
    print(f"Database connection failed: {e}")
    raise

# Define the User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Schema for validating and serializing User data
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)

blp = Blueprint("users", "users", url_prefix="/users", description="Operations on users")

@blp.route("/")
class UserListResource(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get all users"""
        return User.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, new_user_data):
        """Create a new user"""
        new_user = User(**new_user_data)
        db.session.add(new_user)
        db.session.commit()
        return new_user

@blp.route("/<int:user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get a user by ID"""
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, updated_user_data, user_id):
        """Update a user"""
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        for key, value in updated_user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

api.register_blueprint(blp)

if __name__ == "__main__":
    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8080, debug=False)
