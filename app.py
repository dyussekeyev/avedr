from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

# Configuration: List of API Endpoints
API_ENDPOINTS = [
    {"name": "KVRT", "url": "http://127.0.0.1:8000/scan"}
]

@app.route('/scan', methods=['POST'])
def scan():
    """Handles the POST request to scan using multiple endpoints."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    analysis_date = int(time.time())
    analysis_results = {}

    for endpoint in API_ENDPOINTS:
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(endpoint["url"], files=files)
        result = response.json()
        analysis_results[endpoint["name"]] = {
            "category": result.get("category", "undetected"),
            "result": result.get("result", "")
        }

    final_result = [
        {
            "analysis_date": analysis_date,
            "analysis_results": analysis_results
        }
    ]
    
    return jsonify(final_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
