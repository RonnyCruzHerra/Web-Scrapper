from flask import Flask
from api.routes import api  # 👈 IMPORTANTE: importar y registrar el blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix="/api")  # 👈 Esto activa todas tus rutas
    return app