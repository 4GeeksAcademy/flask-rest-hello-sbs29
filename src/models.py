from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.first_name + ' ' + self.last_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.first_name + ' ' + self.last_name
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    gender = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(150), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "diameter" : self.diameter,
            "rotation_period" : self.rotation_period,
            "orbital_period" : self.orbital_period,
            "gravity" : self.gravity,
            "population" : self.population,
            "climate" : self.climate,
            "terrain" : self.terrain,
            "surface_water" : self.surface_water
        }


class FavoritePlanets(db.Model):
    __tablename__ = 'favorites_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), unique=True)
    user = db.relationship(User, backref="favorites_planets")
    planets = db.relationship(Planets)

    def __repr__(self):
        return f"${self.user.first_name} likes ${self.planet.name}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "planet": self.planets.name
        }


class FavoritePeople(db.Model):
    __tablename__ = 'favorites_people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), unique=True)
    user = db.relationship(User, backref="favorites_people")
    people = db.relationship(People)

    def __repr__(self):
        return f"${self.user.first_name} likes ${self.people.name}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "people": self.people.name,
            "people_image": f"https://starwars-visualguide.com/assets/img/characters/{self.people_id}.jpg"
        }