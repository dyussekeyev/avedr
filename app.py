from flask import Flask, jsonify, request
import requests
import time
import os
import tempfile
from mwdblib import MWDB
from datetime import datetime

app = Flask(__name__)

config_api_url = "http://host.docker.internal:5000/api"
config_api_key = "your_api_key_here"

# Configuration: List of API Endpoints
API_ENDPOINTS = [
    {"name": "KVRT", "url": "http://kvrt:8000/scan"}
]

@app.route('/scan', methods=['GET'])
def scan():
    """Handles the GET request to scan using multiple endpoints."""
    hash_value = request.args.get('hash_value')
    
    if not hash_value:
        return jsonify({"error": "hash_value is required"}), 400

    temp_file = tempfile.NamedTemporaryFile(delete=False)

    headers = {
        'accept': 'application/octet-stream',
        'Authorization': f'Bearer {config_api_key}'
    }

    mwdb = MWDB(api_url=config_api_url, api_key=config_api_key)
    file = mwdb.query_file(hash_value)

    try:
        file_content = file.download()
        temp_file.write(file_content)
        temp_file.close()
    except Exception as e:
        return jsonify({
            "error": "Failed to download file",
            "message": str(e)
        }), 500

    analysis_date = int(time.time())
    analysis_results = {}

    for endpoint in API_ENDPOINTS:
        with open(temp_file.name, 'rb') as f:
            files = {'file': (os.path.basename(temp_file.name), f, 'application/octet-stream')}
            response = requests.post(endpoint["url"], files=files)
            if response.status_code != 200:
                os.remove(temp_file.name)
                return jsonify({
                    "error": f"Failed to scan file with {endpoint['name']}",
                    "status_code": response.status_code,
                    "response_text": response.text
                }), 500
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
    
    os.remove(temp_file.name)
    
    # Process final_result and call file.add_comment(comment)
    analysis_date_str = datetime.utcfromtimestamp(analysis_date).strftime('%Y-%m-%d %H:%M:%S UTC')
    comment_lines = [f"analysis_date: {analysis_date_str}"]
    for endpoint, results in analysis_results.items():
        comment_lines.append(f"{endpoint}: {results['result']}")
    comment = "\n".join(comment_lines)
    
    file.add_comment(comment)
    return jsonify({"message": "Comment added successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
