from flask import Flask, request, jsonify
import os
import subprocess
import re
import uuid

app = Flask(__name__)
SCAN_DIR = '/tmp/share'

def run_kvrt(directory):
    """Runs the kvrt.run program with specified parameters."""
    result = subprocess.run(
        ["./kvrt.run", "--allowuser", "--", "-accepteula", "-silent", "-customonly", "-custom", directory], 
        capture_output=True, text=True
    )
    return result.stdout

def parse_output(output, filename):
    """Parses the output to find the threat for the specified file."""
    match = re.search(r'Threat <(.*?)> is detected on object </.*{}>'.format(re.escape(filename)), output)
    if match:
        return True, match.group(1)
    return False, ""

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

    output = run_kvrt(SCAN_DIR)
    threat_detected, threat_name = parse_output(output, random_filename)
    
    category = "malicious" if threat_detected else "undetected"

    response = {
        "av_product": "KVRT",
        "category": category,
        "result": threat_name
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    if not os.path.exists(SCAN_DIR):
        os.makedirs(SCAN_DIR)
    app.run(host='0.0.0.0', port=8000)
