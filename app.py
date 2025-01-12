from flask import Flask, jsonify, request
import requests
import time
import os
import tempfile

app = Flask(__name__)

config_api_url = "http://127.0.0.1:5000/api"
config_api_key = ""

# Configuration: List of API Endpoints
API_ENDPOINTS = [
    {"name": "KVRT", "url": "http://127.0.0.1:8000/scan"}
]

@app.route('/scan', methods=['GET'])
def scan():
    """Handles the POST request to scan using multiple endpoints."""

    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        headers = {
            'accept': 'application/octet-stream',
            'Authorization': f'Bearer {config_api_key}'
        }
        response = requests.get("$config_api_url/file/$hash_value/download", headers=headers, stream=True)
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to download file"}), 500
        
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                temp_file.write(chunk)
        
        temp_file.close()
        file_path = temp_file.name

        analysis_date = int(time.time())
        analysis_results = {}

        for endpoint in API_ENDPOINTS:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
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
    finally:
        os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
