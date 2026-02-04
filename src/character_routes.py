from flask import Blueprint, jsonify, request
from models import User, db, Character

character_api = Blueprint("character_api", __name__)


@character_api.route("/character", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    return jsonify([char.serialize() for char in characters]), 200

@character_api.route("/character/<int:char_id>", methods=["GET"])
def get_character(char_id):
    character = Character.query.get(char_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@character_api.route("/character/<int:char_id>", methods=["DELETE"])
def delete_character(char_id):
    character = Character.query.get(char_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"msg": "Character deleted from database"}), 200