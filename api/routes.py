from flask import Blueprint, request, jsonify, send_from_directory
from ilm.selector_generator import generar_selector
from db.db_connection import Session
from db.models import ScrapedData
import json
import os

api = Blueprint("api", __name__)

# Ruta base absoluta del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Ruta: Generación de selector con LLM
@api.route("/generate-selector", methods=["POST"])
def selector():
    data = request.json
    html = data.get("html")
    target = data.get("target")
    if not html or not target:
        return jsonify({"error": "html y target son requeridos"}), 400
    try:
        selector = generar_selector(html, target)
        return jsonify({"selector": selector})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta: Leer archivo JSON scrapeado
@api.route("/data/<filename>", methods=["GET"])
def get_scraped_data(filename):
    try:
        path = os.path.join("data", filename)
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta: Prueba base de la API
@api.route("/", methods=["GET"])
def index():
    return {"message": "API Flask funcionando correctamente"}, 200

# Ruta: Obtener todos los datos de la BD
@api.route("/scraped-data", methods=["GET"])
def get_all_scraped():
    try:
        session = Session()
        data = session.query(ScrapedData).all()
        result = [item.to_dict() for item in data]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================
# 🆕 Nuevas rutas para frontend
# ============================

# Ruta: Servir dashboard (index.html)
@api.route("/dashboard", methods=["GET"])
def serve_dashboard():
    return send_from_directory(FRONTEND_DIR, "index.html")

# Ruta: Servir archivos estáticos (JS, CSS)
@api.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)
