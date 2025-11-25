import subprocess
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# Global process handler
class VoteSystemProcess:
    def __init__(self):
        self.process = subprocess.Popen(
            ['./SecureVoteSystem.exe', '--interactive'],
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
    return send_from_directory('.', 'index.html')

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
