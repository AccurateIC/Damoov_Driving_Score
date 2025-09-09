from flask import Blueprint
from ..controllers import charts_controller as c

charts_bp = Blueprint("charts", __name__)

charts_bp.route("/summary_graph", methods=["POST"])(c.summary_graph)
charts_bp.route("/driver_distribution", methods=["POST"])(c.driver_distribution)
charts_bp.route("/safety_params", methods=["POST"])(c.safety_params)
charts_bp.route("/safety_graph_trend", methods=["POST"])(c.safety_graph_trend)
charts_bp.route("/mileage_daily", methods=["POST"])(c.mileage_daily)
charts_bp.route("/driving_time_daily", methods=["POST"])(c.driving_time_daily)
charts_bp.route("/overall_analytics_summary", methods=["POST"])(c.overall_analytics_summary)
charts_bp.route("/driving_trips_daily", methods=["POST"])(c.driving_trips_daily)
charts_bp.route("/speeding_analysis", methods=["POST"])(c.speeding_analysis)