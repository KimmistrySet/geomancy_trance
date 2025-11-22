# app.py
from flask import Flask, jsonify
from autogen import run_pipeline_from_file

app = Flask(__name__)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/pipeline/sculpture_garden")
def pipeline_sculpture_garden():
    try:
        data = run_pipeline_from_file("pipeline_sculpture_garden.json")
        return jsonify({"vertices": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pipeline/sculpture_garden_multi")
def pipeline_sculpture_garden_multi():
    try:
        data = run_pipeline_from_file("pipeline_sculpture_garden_multi.json")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: root route so / doesn't 404
@app.route("/")
def index():
    return "Backend is running. Try /api/health"
