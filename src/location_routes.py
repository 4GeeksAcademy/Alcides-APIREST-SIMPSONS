from flask import Blueprint, jsonify, request
from models import db, Location

location_api = Blueprint("location_api", __name__)

@location_api.route("/location", methods=["GET"])
def get_locations():
    locations = Location.query.all()
    response =[location.serialize() for location in locations]
    return jsonify(response), 200

@location_api.route("/location/<int:location_id>", methods=["GET"])
def get_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return jsonify({"error": "Location not found"})
    return jsonify(location.serialize()), 200