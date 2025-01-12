from flask import Flask, jsonify, request
import requests
import time
import os
import tempfile

app = Flask(__name__)

API_ENDPOINTS = [
    {"name": "KVRT", "url": "http://kvrt:8000/scan"}
]

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({"error": "file is required"}), 400

    file = request.files['file']
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    temp_file.close()

    analysis_date = int(time.time())
    analysis_results = {}

    for endpoint in API_ENDPOINTS:
        with open(temp_file.name, 'rb') as f:
            response = requests.post(endpoint["url"], files={'file': (os.path.basename(temp_file.name), f, 'application/octet-stream')})
            if response.status_code != 200:
                os.remove(temp_file.name)
                return jsonify({"error": f"Failed to scan file with {endpoint['name']}", "status_code": response.status_code, "response_text": response.text}), 500
            result = response.json()
            analysis_results[endpoint["name"]] = {"category": result.get("category", "undetected"), "result": result.get("result", "")}

    os.remove(temp_file.name)
    return jsonify([{"analysis_date": analysis_date, "analysis_results": analysis_results}])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
