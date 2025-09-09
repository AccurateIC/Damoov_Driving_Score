from flask import Flask
from flask_cors import CORS
from webapp.app.utils.db import setup_database
from webapp.app.routes.register import register_routes

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Flask app
app = Flask(__name__)
CORS(app)

# DB
engine = setup_database()

# Routes
register_routes(app)

if __name__ == "__main__":
    # host/port identical to your original
    app.run(host="0.0.0.0", port=5000, debug=True)
