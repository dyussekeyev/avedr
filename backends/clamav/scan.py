from flask import Flask, request, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)
SCAN_DIR = '/tmp/share'

def run_clamav(directory):
    """Runs the clamscan program with specified parameters."""
    result = subprocess.run(
        ["clamscan", "-r", directory], 
        capture_output=True, text=True
    )
    return result.stdout

def parse_output(output, filename):
    """Parses the output to find the threat for the specified file."""
    if "FOUND" in output:
        return "malicious"
    return "undetected"

@app.route('/scan', methods=['POST'])
def scan():
    """Handles the POST request to scan a file."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    random_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    filepath = os.path.join(SCAN_DIR, random_filename)
    file.save(filepath)

    output = run_clamav(SCAN_DIR)
    category = parse_output(output, random_filename)

    response = {
        "category": category,
        "result": output
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    if not os.path.exists(SCAN_DIR):
        os.makedirs(SCAN_DIR)
    app.run(host='0.0.0.0', port=8000)
