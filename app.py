from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import json
import glob

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")  # Ensure ES is running

@app.route("/add", methods=["POST"])
def add_status():
    file = request.files['file']
    data = json.load(file)
    es.index(index="rbcapp-status", document=data)
    return jsonify({"message": "Data inserted"}), 200

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    result = es.search(index="rbcapp-status", size=1000, sort="@timestamp:desc")
    app_status = "UP"
    for hit in result["hits"]["hits"]:
        if hit["_source"]["service_status"] == "DOWN":
            app_status = "DOWN"
            break
    return jsonify({"application": "rbcapp1", "status": app_status})

@app.route("/healthcheck/<service_name>", methods=["GET"])
def service_status(service_name):
    query = {
        "query": {
            "match": {
                "service_name": service_name
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}],
        "size": 1
    }
    result = es.search(index="rbcapp-status", body=query)
    if result["hits"]["hits"]:
        status = result["hits"]["hits"][0]["_source"]["service_status"]
        return jsonify({"service": service_name, "status": status})
    return jsonify({"error": "Service not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)