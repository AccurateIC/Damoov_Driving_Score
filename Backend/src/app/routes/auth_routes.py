from flask import Blueprint
from src.app.controllers import auth_controllers as a 

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/signup", methods=["POST"])(a.signup)
auth_bp.route("/signin", methods=["POST"])(a.signin)
auth_bp.route("/forgot_password", methods=["POST"])(a.forgot_password)
auth_bp.route("/jenkins/build-number", methods=["GET"])(a.get_build_number)


