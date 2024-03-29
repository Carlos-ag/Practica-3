from flask import Flask
from app.routes import bicimad_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bicimad_bp, url_prefix="/api/v1")
    return app
