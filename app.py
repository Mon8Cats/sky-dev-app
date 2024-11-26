# pylint: disable=import-error

from flask import Flask
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields
from flask.views import MethodView  # Import MethodView

# Initialize Flask App
app = Flask(__name__)

# Configuration for Swagger (OpenAPI)
app.config["API_TITLE"] = "Employee API"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize Flask-Smorest API
api = Api(app)

# Blueprint for Employees API
blp = Blueprint("employees", "employees", url_prefix="/employees", description="Operations on employees")
api.register_blueprint(blp)

# In-memory database
employees = [
    {"id": 1, "name": "Alice", "title": "Engineer", "email": "alice@example.com", "department": "IT"},
    {"id": 2, "name": "Bob", "title": "Manager", "email": "bob@example.com", "department": "HR"},
    {"id": 3, "name": "Charlie", "title": "Analyst", "email": "charlie@example.com", "department": "Finance"},
    {"id": 4, "name": "Diana", "title": "Designer", "email": "diana@example.com", "department": "Marketing"},
    {"id": 5, "name": "Eve", "title": "Developer", "email": "eve@example.com", "department": "IT"},
]

# Schema for Employee
class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)  # ID is read-only
    name = fields.Str(required=True)  # Name is required
    title = fields.Str(required=True)  # Job title is required
    email = fields.Email(required=True)  # Valid email is required
    department = fields.Str(required=True)  # Department is required

# Routes
@blp.route("/")
class EmployeeListResource(MethodView):  # Inherit from MethodView
    @blp.response(200, EmployeeSchema(many=True))
    def get(self):
        """Get all employees"""
        return employees

    @blp.arguments(EmployeeSchema)
    @blp.response(201, EmployeeSchema)
    def post(self, new_employee):
        """Add a new employee"""
        new_employee["id"] = len(employees) + 1
        employees.append(new_employee)
        return new_employee


@blp.route("/<int:employee_id>")
class EmployeeResource(MethodView):  # Inherit from MethodView
    @blp.response(200, EmployeeSchema)
    def get(self, employee_id):
        """Get an employee by ID"""
        employee = next((e for e in employees if e["id"] == employee_id), None)
        if not employee:
            return {"message": "Employee not found"}, 404
        return employee

    @blp.arguments(EmployeeSchema)
    @blp.response(200, EmployeeSchema)
    def put(self, updated_employee, employee_id):
        """Update an existing employee"""
        employee = next((e for e in employees if e["id"] == employee_id), None)
        if not employee:
            return {"message": "Employee not found"}, 404
        employee.update(updated_employee)
        return employee

    @blp.response(200, description="Employee deleted")
    def delete(self, employee_id):
        """Delete an employee"""
        global employees
        employees = [e for e in employees if e["id"] != employee_id]
        return {"message": "Employee deleted"}, 200


# Register the Blueprint
api.register_blueprint(blp)

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
