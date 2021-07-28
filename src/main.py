"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

first_generation = [{"id": 1, "name": "Julio", "last-name": "Gómez", "age": 98, "children-ref-id": [3,4,5,6]}, {"id": 2, "name": "Marcela", "last-name": "Pérez", "age": 92, "children-ref-id": [3,4,5,6]}]
second_generation = [{"id": 3, "name": "Marcela", "last-name": "Gómez", "age": 58, "parent-ref-id": [1,2], "children-ref-id": 7}, {"id": 4, "name": "Guillermo", "last-name": "Gómez", "age": 56, "parent-ref-id": [1,2], "children-ref-id": 8}, {"id": 5, "name": "Viviana", "last-name": "Gómez", "age": 54, "parent-ref-id": [1,2], "children-ref-id": 9}, {"id": 6, "name": "Julio", "last-name": "Gómez", "age": 50, "parent-ref-id": [1,2], "children-ref-id": 10}]
third_generation = [{"id": 7, "name": "Marcela", "last-name": "Gómez", "age": 58, "parent-ref-id": 7}, {"id": 8, "name": "Guillermo", "last-name": "Gómez", "age": 56, "parent-ref-id": 4}, {"id": 9, "name": "Viviana", "last-name": "Gómez", "age": 54, "parent-ref-id": 5}, {"id": 10, "name": "Julio", "last-name": "Gómez", "age": 50, "parent-ref-id": 6}]
all_generations = first_generation + second_generation + third_generation

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/all', methods=['GET'])
def handle_all():
    all_members = jsonify(first_generation + second_generation + third_generation)
    return all_members

@app.route('/member/<int:id>', methods=['GET'])
def handle_member(id):
    match = []
    for member in all_generations:
        if member["id"] == id:
            match.append(member)

    return jsonify(match)
        
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)