from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.app.utils.db import setup_database
from src.app.routes.register import register_routes
import os

# Flask app
app = Flask(__name__, static_folder="../../Frontend/dist")
CORS(app)

# DB
engine = setup_database()

# API Routes
register_routes(app)

# Serve frontend static files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    dist_dir = app.static_folder
    if path != "" and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, "index.html")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=6001, type=int)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)
