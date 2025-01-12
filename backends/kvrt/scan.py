from flask import Flask, request, jsonify
import os

app = Flask(__name__)
scan_dir = '/tmp/share'

def run_kvrt(dirname):
    # Запускаем программу kvrt.run с указанными параметрами
    result = subprocess.run(["./kvrt.run", "--", "-accepteula", "-silent", "-customonly", "-custom", dirname], capture_output=True, text=True)
    return result.stdout

def parse_output(output, filename):
    # Ищем угрозу для указанного файла
    match = re.search(r'Threat <(.*?)> is detected on object </.*{}>'.format(re.escape(filename)), output)
    if match:
        return match.group(1)
    return "Threat not found for specified file."

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filepath = os.path.join(scan_dir, file.filename)
    file.save(filepath)

    output = run_kvrt(scan_dir)
    threat = parse_output(output, file.filename)
    
    return jsonify({"message": "File saved successfully", "path": filepath}), 200

if __name__ == '__main__':
    if not os.path.exists(scan_dir):
        os.makedirs(scan_dir)
    app.run(host='0.0.0.0', port=8000)
