from flask import Flask
from api.routes import api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def home():
        return "¡API Flask funcionando!"

    return app