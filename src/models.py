from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum

db = SQLAlchemy()

class Gender(PyEnum):
    FEMALE = "Female"
    MALE = "Male"
    OTHER ="Other"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)
    favorites_characters = db.relationship("FavoriteCharacter", back_populates="user", lazy=True)
    favorites_planets = db.relationship("FavoritePlanet", back_populates="user", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
    def get_user_favorites_characters(self):
        return [favorite_character.serialize() for favorite_character in self.favorites_characters]
    
    def get_user_favorites_planets(self):
        return [favorite_planet.serialize() for favorite_planet in self.favorites_planets]

    def __repr__(self):
        return f"<User: {self.email}>"
    
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    producer = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return{
            "id" : self.id,
            "title" : self.title,
            "director" : self.director,
            "producer" : self.producer,
            "release_date" : self.release_date,
            "planet": self.planet
        }
    
    def __repr__(self):
        return f"<Film {self.name}>"

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(5), nullable=False)
    mass = db.Column(db.String(5), nullable=False)
    birth_year = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    favorites = db.relationship("FavoriteCharacter", back_populates="character", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "birth_year": self.birth_year,
            "gender": self.gender.value, 
        }
    
    def __repr__(self):
        return "<Character %r>" % self.name
    
class Planet(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        rotation_period = db.Column(db.String(50), nullable=False)
        diameter = db.Column(db.String(50), nullable=False)
        climate = db.Column(db.String(50), nullable=False)
        population = db.Column(db.String(50), nullable=False)
        favorites = db.relationship("FavoritePlanet", back_populates="planet", lazy=True)
        

        def serialize(self):
            return {
                "id" : self.id, 
                "name" : self.name, 
                "rotation_period" : self.rotation_period,
                "diameter" : self.diameter,
                "climate" : self.climate,
                "population" : self.population,
            }
    
        def __repr__(self):
            return "<Planet %r>" % self.name

class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    character = db.relationship(Character)
    user = db.relationship(User)

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "user_email" : self.user.serialize()["email"],
            "character_id" : self.character_id,
            "character_name" : self.character.serialize()["name"]
        }
    
    def __repr__(self):
        return f'<FavoriteCharacter character: {self.character_id} user: {self.user_id}>'
    

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    planet = db.relationship(Planet)
    user = db.relationship(User)


    def serialize(self):
        return {
            "id" : self.id,
            "user_id": self.user.id,
            "user_email": self.user.serialize()["email"],
            "planet_id" : self.planet_id,
            "planet_name" : self.planet.serialize()["name"]
        }
    
    def __repr__(self):
        return f'<FavoritePlanet planet: {self.planet_id} user: {self.user_id}>'
