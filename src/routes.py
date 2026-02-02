from flask import Blueprint, jsonify
from models import User,db


api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200


@api.route("/users/<int:user_id>", methods=["GET"])
def get_user():
    user = User.query.all(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 400
    return jsonify(user.serialize()), 200