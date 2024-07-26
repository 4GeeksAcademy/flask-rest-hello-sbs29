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

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/', methods=['GET'])
def get_all_user():

    users_query = User.query.all()
    users_list = list(map(lambda user: user.serialize(),users_query))

    return jsonify(users_list), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"info":"Not Found"}), 404
    
    print(user.favorites_planets)
    print(user.favorites_people)

    response = user.serialize()
    response["favorites_planets"] = list(
        map(lambda planet:planet.serialize(), user.favorites_planets))
    response["favorites_people"] = list(
        map(lambda people:people.serialize(), user.favorites_people))

    return jsonify(response), 200

@app.route('/user', methods=['POST'])
def create_user():
    user_body = request.get_json()
    user_db = User(first_name = user_body["first_name"],
                   last_name = user_body["last_name"],
                   email = user_body["email"],
                   password = user_body["password"],
                   is_active = user_body["is_active"])
    db.session.add(user_db)
    db.session.commit()
    return jsonify(user_db.serialize()), 201

@app.route('/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):

    user_db = User.query.filter_by(id=user_id).first()
    if user_db is None:
        return jsonify({"info":"Not Found"}), 404
    user_body = request.get_json()
    
    if "first_name" in user_body:
        user_db.first_name = user_body["first_name"]
    if "last_name" in user_body:
        user_db.first_name = user_body["last_name"]
    if "email" in user_body:
        user_db.first_name = user_body["email"]
    if "password" in user_body:
        user_db.first_name = user_body["password"]
    if "is_active" in user_body:
        user_db.first_name = user_body["is_active"]

    db.session.add(user_db)
    db.session.commit()
    return jsonify(user_db.serialize())

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user_db = User.query.filter_by(id=user_id).first()
    if user_db is None:
        return jsonify({"info":"Not Found"}), 404
    db.session.delete(user_db)
    db.session.commit()
    return jsonify({"info":"User deleted"})
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
