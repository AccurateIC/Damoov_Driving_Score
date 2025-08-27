from .summary_routes import summary_bp
from .trips_routes import trips_bp
from .charts_routes import charts_bp
from flask import Blueprint
#from src.app.controllers import system_controller

def register_routes(app):
    # core blueprints
    app.register_blueprint(summary_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(charts_bp)
