
# pylint: disable=import-error

import datetime
import logging
import os

#from flask import Flask, render_template, request, Response
#import sqlalchemy

from connect_connector import connect_with_connector
from connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from connect_tcp import connect_tcp_socket
from connect_unix import connect_unix_socket
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import google.cloud.secretmanager as secretmanager

app = Flask(__name__)



# Function to access secrets
def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Fetching database credentials from Secret Manager
project_id = "sky-root"
db_user = access_secret_version("db_user")
db_password = access_secret_version("db_password")
db_name = "devdb" # os.getenv('DB_NAME', 'your_database')
sql_connection_name = "sky-root:us-central1:skypostgre"
#db_host ="localhost:5432" # os.getenv('DB_HOST', 'your_host')


def init_db_connection():
    db_config = {
        'pool_size': 5,
        'max_overflow': 2,
        'pool_timeout': 3, 
        'pool_recycle': 1800,
    }
    return init_unix_connection_engine(db_config)

def init_unix_connection_engine(db_config):
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgres+pg8000",
            #host=os.environ.get('DB_HOST'),
            #port=os.environ.get('DB_PORT'),
            username=db_user, #os.environ.get('DB_USER'),
            password=db_password, #os.environ.get('DB_PASS'),
            database=db_name, #os.environ.get('DB_NAME'),
            query={
                "unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(sql_connection_name
                    #os.environ.get('CLOUD_SQL_CONNECTION_NAME')
                )
            }
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool

db = init_db_connection()


# Configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

# Define the model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not User:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
