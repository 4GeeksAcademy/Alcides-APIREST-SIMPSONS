from flask import Blueprint, jsonify, request
from models import User, db, Character, Location

api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@api.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user = User.query.get(1)
    if not user:
        return jsonify({"error": "User not found"}), 404
    response = [fav.serialize() for fav in user.favorites]
    return jsonify(response), 200

@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    new_user = User(email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200

@api.route("/favorite/character/<int:character_id>", methods=["POST"])
def add_fav_character(character_id):
    user = User.query.get(1)
    character = db.session.get(Character, character_id)
    if not character or not user:
        return jsonify({"msg": "User or character doesnt exist"}), 404
    if character in user.favorites:
        return jsonify({"msg": "Already in favorites"}), 400
    user.favorites.append(character)
    db.session.commit()
    return jsonify({"msg": f"Character {character.name} added to favorites"}), 201

@api.route("/favorite/location/<int:location_id>", methods=["POST"])
def add_fav_location(location_id):
    user = User.query.get(1)
    location = db.session.get(Location, location_id)
    if not location or not user:
        return jsonify({"msg": "User or location doesnt exist"}), 404
    if location in user.favorites:
        return jsonify({"msg": "Already in favorites"}), 400
    user.favorites.append(location)
    db.session.commit()
    return jsonify({"msg": f"Location {location.name} added to favorites"}), 201

@api.route("/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_fav_character(character_id):
    user = User.query.get(1)
    character = db.session.get(Character, character_id)
    if not character or not user:
        return jsonify({"msg": "User or character doesnt exist"}), 404
    if character not in user.favorites:
        return jsonify({"msg": "This character is not in your favorites"}), 400
    user.favorites.remove(character)
    db.session.commit()
    return jsonify({"msg": f"{character.name} has been deleted from favorites"}), 200

@api.route("/favorite/location/<int:location_id>", methods=["DELETE"])
def delete_fav_location(location_id):
    user = User.query.get(1)
    location = db.session.get(Location, location_id)
    if not location or not user:
        return jsonify({"msg": "User or location doesnt exist"}), 404
    if location not in user.favorites:
        return jsonify({"msg": "This location is not in your favorites"}), 400
    user.favorites.remove(location)
    db.session.commit()
    return jsonify({"msg": f"{location.name} has been deleted from favorites"}), 200