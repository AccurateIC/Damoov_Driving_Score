
from flask import Blueprint
from ..controllers import trips_controller as c

trips_bp = Blueprint("trips", __name__)

trips_bp.route("/trips", methods=["GET"])(c.list_trips)
trips_bp.route("/trips/<int:unique_id>", methods=["GET"])(c.trip_details)
trips_bp.route("/trips/stats/<int:unique_id>", methods=["GET"])(c.trip_stats)
trips_bp.route("/trips/location/<int:unique_id>", methods=["GET"])(c.trip_location)
trips_bp.route("/locations/<int:unique_id>", methods=["GET"])(c.raw_locations)
trips_bp.route("/trips/map/<int:track_id>", methods=["GET"])(c.trip_map)
trips_bp.route("/users", methods=["GET"])(c.list_users)