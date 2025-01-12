from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/kvrt', methods=['GET'])
def kvrt():
    response = requests.get('http://kvrt:8000/scan')
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
