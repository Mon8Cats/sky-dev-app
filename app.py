#
# pylint: disable=import-error
#

from flask import Flask, request
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields
from flask.views import MethodView

app = Flask(__name__)
app.config["API_TITLE"] = "User API"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

blp = Blueprint("users", "users", url_prefix="/users", description="Operations on users")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)


# In-memory database
users = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
    {"id": 3, "name": "Alice Johnson", "email": "alice.johnson@example.com"},
    {"id": 4, "name": "Bob Brown", "email": "bob.brown@example.com"},
    {"id": 5, "name": "Charlie Davis", "email": "charlie.davis@example.com"}
]

user_id_counter = 6

def find_user(user_id):
    return next((user for user in users if user["id"] == user_id), None)

@blp.route("/")
class UserListResource(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get all users"""
        return users

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, new_user):
        """Create a new user"""
        global user_id_counter
        new_user["id"] = user_id_counter
        users.append(new_user)
        user_id_counter += 1
        return new_user

@blp.route("/<int:user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get a user by ID"""
        user = find_user(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, updated_user, user_id):
        """Update a user"""
        user = find_user(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.update(updated_user)
        return user

    def delete(self, user_id):
        """Delete a user"""
        user = find_user(user_id)
        if not user:
            return {"message": "User not found"}, 404
        users.remove(user)
        return {"message": "User deleted"}, 200

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
