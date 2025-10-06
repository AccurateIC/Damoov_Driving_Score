from flask import Flask, send_from_directory
from flask_cors import CORS
from src.app.utils.db import setup_database
from src.app.routes.register import register_routes
import os

# Flask app
app = Flask(__name__, static_folder='../Frontend/dist')
CORS(app)

# DB
engine = setup_database()

# Routes
register_routes(app)

# Serve frontend static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, debug=True)
