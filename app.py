# pylint: disable=import-error

import os
import psycopg2
from flask import Flask, jsonify, request
from google.cloud import secretmanager

app = Flask(__name__)

# Fetch secrets from Google Secret Manager
def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "sky-root")
    secret_path = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

# Database credentials
DB_USER = "skyroot" #get_secret("db_user")  # Fetch username
DB_PASSWORD = "skypassword" #get_secret("db_password")  # Fetch password
DB_NAME = "devdb"
DB_HOST = "104.154.194.173"  # Public IP of the Cloud SQL instance
DB_PORT = 5432  # Default PostgreSQL port

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# In-memory database
employees = [
    {"id": 1, "name": "AliceX", "title": "Engineer", "email": "alice@example.com", "department": "IT"},
    {"id": 2, "name": "BobX", "title": "Manager", "email": "bob@example.com", "department": "HR"},
    {"id": 3, "name": "CharlieX", "title": "Analyst", "email": "charlie@example.com", "department": "Finance"},
    {"id": 4, "name": "DianaX", "title": "Designer", "email": "diana@example.com", "department": "Marketing"},
    {"id": 5, "name": "EveX", "title": "Developer", "email": "eve@example.com", "department": "IT"},
]

# Get all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees;")
        rows = cursor.fetchall()
        conn.close()

        # Convert rows to a list of dictionaries
        employees = [
            {"id": row[0], "name": row[1], "title": row[2], "email": row[3], "department": row[4]}
            for row in rows
        ]
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    #return jsonify(employees), 200

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
