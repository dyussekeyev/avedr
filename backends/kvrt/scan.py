from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/scan', methods=['GET'])
def scan():
    return jsonify({"message": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
