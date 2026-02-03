from flask import Blueprint, jsonify, request
from models import Character

char_api = ("char_api", __name__)

@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200