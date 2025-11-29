import requests
import os
from flask import Flask, jsonify, send_from_directory

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, 'web', 'dashboard')

app = Flask(__name__)

# Configuration
VOTING_NODE_URL = "http://localhost:5000"

@app.route('/')
def index():
    # Serve the Dashboard UI
    return send_from_directory(DASHBOARD_DIR, 'dashboard.html')

@app.route('/status_proxy', methods=['GET'])
def status_proxy():
    try:
        # Fetch data from the Voting Node (simulating network request)
        response = requests.get(f"{VOTING_NODE_URL}/status")
        return jsonify(response.json())
    except requests.exceptions.ConnectionError:
        return jsonify({"shards": []}), 503

@app.route('/tally_proxy', methods=['GET'])
def tally_proxy():
    try:
        response = requests.get(f"{VOTING_NODE_URL}/tally")
        return jsonify(response.json())
    except requests.exceptions.ConnectionError:
        return jsonify({"tally": []}), 503

if __name__ == '__main__':
    print("Starting Display Server on Port 5001...")
    app.run(port=5001)
