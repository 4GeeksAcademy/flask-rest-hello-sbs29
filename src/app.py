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
from models import db, User , People , Planets , FavoritePeople , FavoritePlanets
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

###############################################################################################
######################################  USERS  ################################################
###############################################################################################
# ---------------------------------------------------------------------------------------------

@app.route('/user', methods=['GET'])
def get_all_user():

    users_query = User.query.all()
    users_list = list(map(lambda user: user.serialize(),users_query))

    return jsonify(users_list), 200

# ---------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------------------------

@app.route('/user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):

    user_db = User.query.filter_by(id=user_id).first()
    if user_db is None:
        return jsonify({"info":"Not Found"}), 404
    user_body = request.get_json()
    
    if "first_name" in user_body:
        user_db.first_name = user_body["first_name"]
    if "last_name" in user_body:
        user_db.last_name = user_body["last_name"]
    if "email" in user_body:
        user_db.email = user_body["email"]
    if "password" in user_body:
        user_db.password = user_body["password"]
    if "is_active" in user_body:
        user_db.is_active = user_body["is_active"]

    db.session.add(user_db)
    db.session.commit()
    return jsonify(user_db.serialize())

# ---------------------------------------------------------------------------------------------

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user_db = User.query.filter_by(id=user_id).first()
    if user_db is None:
        return jsonify({"info":"Not Found"}), 404
    db.session.delete(user_db)
    db.session.commit()
    return jsonify({"info":"User deleted"})
    
###############################################################################################
######################################  PEOPLE  ###############################################
###############################################################################################

# ---------------------------------------------------------------------------------------------

@app.route('/people', methods=['GET'])
def get_people():

    people_query = People.query.all()
    people_list = list(map(lambda people: people.serialize(),people_query))

    return jsonify(people_list), 200

# ---------------------------------------------------------------------------------------------

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):

    people = People.query.filter_by(id=people_id).first()
    if people is None:
        return jsonify({"info":"Not Found"}), 404

    return jsonify(people.serialize()), 200


# ---------------------------------------------------------------------------------------------

@app.route('/people', methods=['POST'])
def create_people():
    body = request.get_json()
    people_db = People(
        name = body["name"],
        gender = body["gender"],
        height = body["height"],
        mass = body["mass"],
        hair_color = body["hair_color"],
        skin_color = body["skin_color"],
        eye_color = body["eye_color"],
        birth_year = body["birth_year"]
        )
    db.session.add(people_db)
    db.session.commit()
    return jsonify(people_db.serialize()), 201

# ---------------------------------------------------------------------------------------------

@app.route('/people/<int:people_id>', methods=['PATCH'])
def update_people(people_id):

    people_db = People.query.filter_by(id=people_id).first()
    if people_db is None:
        return jsonify({"info":"Not Found"}), 404
    body = request.get_json()
    
    if "name" in body:
        people_db.name = body["name"]
    if "gender" in body:
        people_db.gender = body["gender"]
    if "height" in body:
        people_db.height = body["height"]
    if "mass" in body:
        people_db.mass = body["mass"]
    if "hair_color" in body:
        people_db.hair_color = body["hair_color"]
    if "skin_color" in body:
        people_db.skin_color = body["skin_color"]
    if "eye_color" in body:
        people_db.eye_color = body["eye_color"]
    if "birth_year" in body:
        people_db.birth_year = body["birth_year"]



    db.session.add(people_db)
    db.session.commit()
    return jsonify(people_db.serialize())

# ---------------------------------------------------------------------------------------------

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):

    people_db = People.query.filter_by(id=people_id).first()
    if people_db is None:
        return jsonify({"info":"Not Found"}), 404
    db.session.delete(people_db)
    db.session.commit()
    return jsonify({"info":"People deleted"})
    
###############################################################################################
######################################  PLANETS  ##############################################
###############################################################################################

# ---------------------------------------------------------------------------------------------

@app.route('/planets', methods=['GET'])
def get_planets():

    planets_query = Planets.query.all()
    planets_list = list(map(lambda planet: planet.serialize(),planets_query))

    return jsonify(planets_list), 200

# ---------------------------------------------------------------------------------------------

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planets(planet_id):

    planet = Planets.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"info":"Not Found"}), 404

    return jsonify(planet.serialize()), 200

# ---------------------------------------------------------------------------------------------

@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    planet_db = Planets(
        climate = body["climate"], 
        diameter = body["diameter"], 
        gravity = body["gravity"], 
        name = body["name"], 
        orbital_period = body["orbital_period"], 
        population = body["population"], 
        rotation_period = body["rotation_period"], 
        surface_water = body["surface_water"], 
        terrain = body["terrain"]
        )
    db.session.add(planet_db)
    db.session.commit()
    return jsonify(planet_db.serialize()), 201

# ---------------------------------------------------------------------------------------------

@app.route('/planets/<int:planet_id>', methods=['PATCH'])
def update_planet(planet_id):

    planet_db = Planets.query.filter_by(id=planet_id).first()
    if planet_db is None:
        return jsonify({"info":"Not Found"}), 404
    body = request.get_json()
    
    if "climate" in body:
        planet_db.climate = body["climate"]
    if "diameter" in body:
        planet_db.diameter = body["diameter"]
    if "gravity" in body:
        planet_db.gravity = body["gravity"]
    if "name" in body:
        planet_db.name = body["name"]
    if "orbital_period" in body:
        planet_db.orbital_period = body["orbital_period"]
    if "population" in body:
        planet_db.population = body["population"]
    if "rotation_period" in body:
        planet_db.rotation_period = body["rotation_period"]
    if "surface_water" in body:
        planet_db.surface_water = body["surface_water"]
    if "terrain" in body:
        planet_db.terrain = body["terrain"]



    db.session.add(planet_db)
    db.session.commit()
    return jsonify(planet_db.serialize())

# ---------------------------------------------------------------------------------------------

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet_db = Planets.query.filter_by(id=planet_id).first()
    if planet_db is None:
        return jsonify({"info":"Not Found"}), 404
    db.session.delete(planet_db)
    db.session.commit()
    return jsonify({"info":"Planet deleted"})

###############################################################################################
#####################################  FAVORITES  #############################################
###############################################################################################

# ---------------------------------------------------------------------------------------------

@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():

    favorite_planets = FavoritePlanets.query.filter_by(user_id=1)
    favorite_planets_list = list(map(lambda planet: planet.serialize(),favorite_planets))

    favorite_people = FavoritePeople.query.filter_by(user_id=1)
    favorite_people_list = list(map(lambda people: people.serialize(),favorite_people))

    return jsonify({"planets":favorite_planets_list,"people":favorite_people_list})

# ---------------------------------------------------------------------------------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
    body = request.get_json()
    favorite_planet_db = FavoritePlanets(
        user_id = body["user_id"],
        planet_id = planet_id
        )
    db.session.add(favorite_planet_db)
    db.session.commit()
    return jsonify(favorite_planet_db.serialize()), 201

# ---------------------------------------------------------------------------------------------

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_people(people_id):
    body = request.get_json()
    favorite_people_db = FavoritePeople(
        user_id = body["user_id"],
        people_id = people_id
        )
    db.session.add(favorite_people_db)
    db.session.commit()
    return jsonify(favorite_people_db.serialize()), 201

# ---------------------------------------------------------------------------------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet_db = FavoritePlanets.query.filter_by(id=planet_id, user_id=1).first()
    if favorite_planet_db is None:
        return jsonify({"info":"Not Found"}), 404
    db.session.delete(favorite_planet_db)
    db.session.commit()
    return jsonify({"info":"Favorite planet deleted"})

# ---------------------------------------------------------------------------------------------

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_people_db = FavoritePeople.query.filter_by(id=people_id, user_id=1).first()
    if favorite_people_db is None:
        return jsonify({"info":"Not Found"}), 404
    db.session.delete(favorite_people_db)
    db.session.commit()
    return jsonify({"info":"Favorite people deleted"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
