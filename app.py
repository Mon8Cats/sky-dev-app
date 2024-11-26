# pylint: disable=import-error

from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, title="Employee API", description="A simple CRUD API for managing employees")

# Namespace for organizing APIs
employee_ns = api.namespace("employees", description="Operations related to employees")

# In-memory database
employees = [
    {"id": 1, "name": "Alice", "title": "Engineer", "email": "alice@example.com", "department": "IT"},
    {"id": 2, "name": "Bob", "title": "Manager", "email": "bob@example.com", "department": "HR"},
    {"id": 3, "name": "Charlie", "title": "Analyst", "email": "charlie@example.com", "department": "Finance"},
    {"id": 4, "name": "Diana", "title": "Designer", "email": "diana@example.com", "department": "Marketing"},
    {"id": 5, "name": "Eve", "title": "Developer", "email": "eve@example.com", "department": "IT"},
]

# Model for Employee
employee_model = api.model(
    "Employee",
    {
        "id": fields.Integer(readOnly=True, description="The unique ID of the employee"),
        "name": fields.String(required=True, description="The name of the employee"),
        "title": fields.String(required=True, description="The job title of the employee"),
        "email": fields.String(required=True, description="The email of the employee"),
        "department": fields.String(required=True, description="The department of the employee"),
    },
)

# Routes
@employee_ns.route("/")
class EmployeeList(Resource):
    @employee_ns.marshal_with(employee_model, as_list=True)
    def get(self):
        """Get all employees"""
        return employees

    @employee_ns.expect(employee_model, validate=True)
    @employee_ns.marshal_with(employee_model, code=201)
    def post(self):
        """Add a new employee"""
        data = request.json
        new_employee = {
            "id": max(emp["id"] for emp in employees) + 1 if employees else 1,
            **data,
        }
        employees.append(new_employee)
        return new_employee, 201


@employee_ns.route("/<int:employee_id>")
@employee_ns.response(404, "Employee not found")
class Employee(Resource):
    @employee_ns.marshal_with(employee_model)
    def get(self, employee_id):
        """Get an employee by ID"""
        employee = next((emp for emp in employees if emp["id"] == employee_id), None)
        if not employee:
            api.abort(404, "Employee not found")
        return employee

    @employee_ns.expect(employee_model, validate=True)
    @employee_ns.marshal_with(employee_model)
    def put(self, employee_id):
        """Update an employee"""
        employee = next((emp for emp in employees if emp["id"] == employee_id), None)
        if not employee:
            api.abort(404, "Employee not found")
        data = request.json
        for key in data:
            employee[key] = data[key]
        return employee

    @employee_ns.response(200, "Employee deleted")
    def delete(self, employee_id):
        """Delete an employee"""
        global employees
        employees = [emp for emp in employees if emp["id"] != employee_id]
        return {"message": "Employee deleted"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
