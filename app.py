from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# Configuration: List of API Endpoints
API_ENDPOINTS = [
    {"name": "KVRT", "url": "http://127.0.0.1:8000/scan"}
]

@app.route('/scan', methods=['GET'])
def scan():
    """Handles the GET request to scan using multiple endpoints."""
    analysis_date = int(time.time())
    analysis_results = {}

    for endpoint in API_ENDPOINTS:
        response = requests.get(endpoint["url"])
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
