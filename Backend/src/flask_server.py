from flask import Flask, jsonify
from flask_cors import CORS
from src.app.utils.db import setup_database
from src.app.routes.register import register_routes

# Flask app
app = Flask(__name__)
CORS(app)

# Database setup
engine = setup_database()

# Register existing routes
register_routes(app)

# ✅ Add health endpoint
@app.route('/api/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Running on all interfaces, port 6001, debug mode enabled
    app.run(host="0.0.0.0", port=6001, debug=True)
