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
from models import db, User, Character, Film, Planet, Gender

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify({"users": serialized_users})

@app.route('/user', methods=["POST"])
def user_register():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)
    if email is None or password is None:
        return jsonify({"error": "Email and password required"}), 400
        
    user = User(email=email, password=password)

    try:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return jsonify({"message": f"{user.email} created!"}), 201
           
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify({"characters": serialized_characters})

@app.route("/character", methods=["POST"])
def create_character():
    body = request.json
    name = body.get("name", None)
    height = body.get("height", None)
    mass = body.get("mass", None)
    birth_year = body.get("birth_year", None)
    gender = body.get("gender", None)

    if name is None or height is None or mass is None or birth_year is None or gender is None:
        return jsonify({"error": "missing fields"}), 400
    
    character = Character(name=name, height=height, mass=mass, birth_year=birth_year, gender=Gender(gender))

    try:
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)

        return jsonify({"message": f"{character.name} created!"}), 201
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
@app.route("/character/<int:id>", methods=["GET"])
def get_character_by_id(id):
    try:
        character = Character.query.get(id)
        if character is None:
            return jsonify({'error': "Character not found!"}), 404
        return jsonify({"character": character.serialize()}), 200
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
@app.route("/user/<int:user_id>/favorites/character", methods=["GET"])
def get_favorite_characters(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': "User not found!"}), 404
        return jsonify(user.get_user_favorites_characters()), 200
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/planets', methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify({"planets": serialized_planets})


@app.route("/planet", methods=["POST"])
def create_planet():
    body = request.json
    name = body.get("name", None)
    rotation_period = body.get("rotation_period", None)
    diameter = body.get("diameter", None)
    climate = body.get("climate", None)
    population = body.get("population", None)

    if name is None or rotation_period is None or diameter is None or climate is None or population is None:
        return jsonify({"error": "missing fields"}), 400
    
    planet = Planet(name=name, rotation_period=rotation_period, diameter=diameter, climate=climate, population=population)

    try: 
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)

        return jsonify({"message": f"{planet.name} created!"}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
@app.route("/planet/<int:id>", methods=["GET"])
def get_planet_by_id(id):
    try: 
        planet = Planet.query.get(id)
        if planet is None:
            return jsonify({'error': "planet not found!"}), 404
        return jsonify({"planet": planet.serialize()}), 200

    except Exception as error:
        return jsonify({"error": f"{error}"}), 500    
    
@app.route("/user/<int:user_id>/favorites/planet", methods=["GET"])
def get_favorite_planets(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': "User not found!"}), 404
        return jsonify(user.get_user_favorites_planets()), 200
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500    

@app.route('/films', methods=["GET"])
def get_films():
    films = Film.query.all()
    serialized_films = [film.serialize() for film in films]
    return jsonify({"films": serialized_films})

@app.route("/film", methods=["POST"])
def create_film():
    body = request.json
    title = body.get("title", None)
    director = body.get("director", None)
    producer = body.get("producer", None)
    release_date = body.get("release_date", None)

    if title is None or director is None or producer is None or release_date is None:
        return jsonify({"error": "missing fields"}), 400
    
    film = Film(title=title, director=director, producer=producer, release_date=release_date)

    try: 
        db.session.add(film)
        db.session.commit()
        db.session.refresh(film)

        return jsonify({"message": f"{film.title} created!"}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)