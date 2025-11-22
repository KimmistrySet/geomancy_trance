from flask import Flask, jsonify
from autogen import run_pipeline_from_file

app = Flask(__name__)

@app.route("/api/pipeline/sculpture_garden")

def pipeline_sculpture_garden():
    data = run_pipeline_from_file("pipeline_sculpture_garden.json")
    return jsonify({"vertices": data})

@app.route("/api/pipeline/sculpture_garden_multi")
def pipeline_sculpture_garden_multi():
    data = run_pipeline_from_file("pipeline_sculpture_garden_multi.json")
    return jsonify(data)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})
