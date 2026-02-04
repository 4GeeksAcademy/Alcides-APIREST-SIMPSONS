from flask import Blueprint, jsonify, request
from models import User, db, Character


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
        return jsonify({"error": "User not found"}), 400
    return jsonify(user.serialize()), 200


@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    new_user = User(
        email=data["email"],
        password=data["password"]
    )

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
      


@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200


@api.route("/characters/<int:char_id>", methods=["GET"])
def get_character(char_id):
    character = Character.query.get(char_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200


@api.route("/characters", methods=["POST"])
def create_character():
    data = request.get_json()
    if not data.get("name") or not data.get("quote") or not data.get("job") or not data.get("age"):
        return jsonify({"error": "Missing fields"}), 400

    new_character = Character(
        name=data["name"],
        quote=data["quote"],
        image=data["image"],
        job=data["job"],
        age=data["age"]
    )

    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@api.route("/characters/<int:char_id>", methods=["DELETE"])
def delete_char(char_id):
    character = Character.query.get(char_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify({"msg": "Character deleted succesfully"}), 200


@api.route("/users/favorites", methods=["GET"])
def get_userfavs():
    user = User.query.get(1)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user_data = user.serialize()
    favorites = user_data["favorites"]
    return jsonify(favorites), 200


@api.route("/favorite/character/<int:character_id>", methods=["POST"])
def add_fav(character_id):
    user = User.query.get(1)
    character = db.session.get(Character, character_id)
    if not character or not user:
        return jsonify({"msg": "User or character doesnt exist"})
    user.favorites.append(character)
    db.session.commit()
    return jsonify({"msg": f"Character {character.name} added to favorites"}), 200