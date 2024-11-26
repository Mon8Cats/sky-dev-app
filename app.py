#
# pylint: disable=import-error
#

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
employees = [
    {"id": 1, "name": "Alice", "title": "Engineer", "email": "alice@example.com", "department": "IT"},
    {"id": 2, "name": "Bob", "title": "Manager", "email": "bob@example.com", "department": "HR"},
    {"id": 3, "name": "Charlie", "title": "Analyst", "email": "charlie@example.com", "department": "Finance"},
    {"id": 4, "name": "Diana", "title": "Designer", "email": "diana@example.com", "department": "Marketing"},
    {"id": 5, "name": "Eve", "title": "Developer", "email": "eve@example.com", "department": "IT"},
]

# Get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees), 200

# Get an employee by ID
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if employee:
        return jsonify(employee), 200
    return jsonify({"error": "Employee not found"}), 404

# Add a new employee
@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.json
    if not all(key in data for key in ["name", "title", "email", "department"]):
        return jsonify({"error": "Missing required fields"}), 400
    new_employee = {
        "id": max(emp["id"] for emp in employees) + 1 if employees else 1,
        "name": data["name"],
        "title": data["title"],
        "email": data["email"],
        "department": data["department"],
    }
    employees.append(new_employee)
    return jsonify(new_employee), 201

# Update an existing employee
@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    data = request.json
    for key in ["name", "title", "email", "department"]:
        if key in data:
            employee[key] = data[key]
    return jsonify(employee), 200

# Delete an employee
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    global employees
    employees = [emp for emp in employees if emp["id"] != employee_id]
    return jsonify({"message": "Employee deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
