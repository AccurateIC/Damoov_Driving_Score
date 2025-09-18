from flask import Blueprint
from src.app.controllers import summary_controller as c

summary_bp = Blueprint("summary", __name__)

summary_bp.route("/safe_driving_summary", methods=["GET"])(c.safe_driving_summary)
summary_bp.route("/eco_driving_summary", methods=["GET"])(c.eco_driving_summary)
summary_bp.route("/safety_dashboard_summary", methods=["GET"])(c.safety_dashboard_summary)
summary_bp.route("/performance_summary", methods=["GET"])(c.performance_summary)
summary_bp.route("/user_safety_dashboard_summary", methods=["GET"])(c.user_safety_dashboard_summary)
summary_bp.route("/fetch_top_drivers", methods=["GET"])(c.fetch_top_drivers)
summary_bp.route("/assign_badges", methods=["GET"])(c.assign_badges)
summary_bp.route("/badge_aggregates", methods=["GET"])(c.assign_badges_api)
