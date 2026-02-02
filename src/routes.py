from flask import Blueprint, jsonify, request
from models import User,db


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