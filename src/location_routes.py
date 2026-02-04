from flask import Blueprint, jsonify, request
from models import db, Location

Location_api = Blueprint("location_api", __name__)