from flask import Flask, request, jsonify
import os

app = Flask(__name__)
scan_dir = '/tmp/share'

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filepath = os.path.join(scan_dir, file.filename)
    file.save(filepath)
    return jsonify({"message": "File saved successfully", "path": filepath}), 200

if __name__ == '__main__':
    if not os.path.exists(scan_dir):
        os.makedirs(scan_dir)
    app.run(host='0.0.0.0', port=8000)
