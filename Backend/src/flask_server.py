from flask import Flask
from flask_cors import CORS
from src.app.utils.db import setup_database
from src.app.routes.register import register_routes

# Flask app
app = Flask(__name__)
CORS(app)

# DB
engine = setup_database()

# Routes
register_routes(app)

if __name__ == "__main__":
    # host/port identical to your original
    app.run(host="0.0.0.0", port=3344, debug=True)
