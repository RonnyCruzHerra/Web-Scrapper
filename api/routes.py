from flask import Blueprint, request, jsonify, send_from_directory
from ilm.selector_generator import generar_selector
from db.db_connection import Session
from db.models import ScrapedData
import json
import os

# Importa el scraper dinámico de Amazon
from scraper.amazon_dynamic import scrape_amazon_dynamic

api = Blueprint("api", __name__)

# Ruta base absoluta del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

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

@api.route("/scraped-data", methods=["GET"])
def get_all_scraped():
    try:
        session = Session()
        data = session.query(ScrapedData).all()
        result = [item.to_dict() for item in data]
        session.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/scheduler-logs", methods=["GET"])
def get_scheduler_logs():
    try:
        log_path = os.path.join("logs", "scheduler_executions.json")
        if not os.path.exists(log_path):
            return jsonify([])
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/dashboard", methods=["GET"])
def serve_dashboard():
    return send_from_directory(FRONTEND_DIR, "index.html")

@api.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@api.route("/scraped-data-paged", methods=["GET"])
def get_scraped_data_paged():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        session = Session()
        query = session.query(ScrapedData)
        total = query.count()
        items = query.offset((page-1)*per_page).limit(per_page).all()
        result = [item.to_dict() for item in items]
        session.close()
        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "items": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/scrape-amazon-dynamic", methods=["POST"])
def run_amazon_dynamic_scraper():
    data = request.json or {}
    query = data.get("query", "laptop")
    pages = int(data.get("pages", 1))
    try:
        count = scrape_amazon_dynamic(query, pages)
        return jsonify({
            "status": "ok",
            "message": f"Scraping de '{query}' completado, {count} productos guardados"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500