from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from sqlalchemy import text
from src.app.db_queries import get_user_by_email, insert_user, get_engine
from src.app.utils.db import setup_database, CONFIG

auth_bp = Blueprint("auth", __name__)
db_cfg = CONFIG.get("database", {})
users_table = db_cfg.get("users_table", "users")
SECRET_KEY = "your_secret_key"  # keep in env var

def get_engine():
    return setup_database()

# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    remember_me = data.get("remember_me", False)

    if not email or not password or not confirm_password:
        return jsonify({"error": "Missing required fields"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    engine = get_engine()
    with engine.connect() as conn:
        existing = get_user_by_email(conn, users_table, email)
        if existing:
            return jsonify({"error": "Email already registered"}), 409

        hashed_pw = generate_password_hash(password)
        user_id = insert_user(conn, users_table, email, hashed_pw)
        conn.commit()

    token_expiry = datetime.timedelta(days=30 if remember_me else 1)
    token = jwt.encode(
        {"user_id": user_id, "exp": datetime.datetime.utcnow() + token_expiry},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Signup successful",
        "user_id": user_id,
        "token": token
    }), 201


# ---------- SIGNIN ----------
@auth_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    engine = get_engine()
    with engine.connect() as conn:
        user = get_user_by_email(conn, users_table, email)

        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Signin successful",
        "user_id": user.id,
        "token": token
    })


# ---------- FORGOT PASSWORD ----------
@auth_bp.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    engine = get_engine()
    with engine.connect() as conn:
        user = get_user_by_email(conn, users_table, email)
        if not user:
            return jsonify({"error": "Email not registered"}), 404

    reset_token = jwt.encode(
        {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Password reset link sent to email",
        "reset_token": reset_token  # in real-world send via email
    })
