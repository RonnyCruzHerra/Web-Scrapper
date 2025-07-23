from flask import Blueprint, request, jsonify
from ilm.selector_generator import generar_selector
import json
import os

api = Blueprint("api", __name__)

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

@api.route("/data/<filename>", methods=["GET"])
def get_scraped_data(filename):
    try:
        path = os.path.join("data", filename)
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@api.route("/", methods=["GET"])
def index():
    return {"message": "API Flask funcionando correctamente"}, 200