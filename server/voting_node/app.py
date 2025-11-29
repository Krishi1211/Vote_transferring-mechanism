import subprocess
import threading
import time
import os
from flask import Flask, request, jsonify, send_from_directory

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BIN_DIR = os.path.join(PROJECT_ROOT, 'bin')
WEB_DIR = os.path.join(PROJECT_ROOT, 'web', 'voting_booth')

app = Flask(__name__)

# Global process handler
class VoteSystemProcess:
    def __init__(self):
        exe_path = os.path.join(BIN_DIR, 'SecureVoteSystem.exe')
        self.process = subprocess.Popen(
            [exe_path, '--interactive'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send_command(self, command):
        if self.process.poll() is not None:
            return "ERROR: Process ended"
        
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        
        # Read response
        output = self.process.stdout.readline().strip()
        return output

system = VoteSystemProcess()

@app.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    voter_id = data.get('id')
    content = data.get('content')
    
    response = system.send_command(f"VOTE {voter_id} {content}")
    return jsonify({"status": response})

@app.route('/status', methods=['GET'])
def status():
    response = system.send_command("STATUS")
    return response # Already JSON string from C++

@app.route('/tally', methods=['GET'])
def tally():
    response = system.send_command("TALLY")
    return response

if __name__ == '__main__':
    app.run(port=5000)
