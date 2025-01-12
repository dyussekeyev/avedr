from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/kvrt', methods=['GET'])
def kvrt():
    response = requests.get('http://127.0.0.1:8000/scan')
    return jsonify({"kvrt": response.json()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
