"""
Secure Voting Node Server with Production-Level Security
Features:
- JWT Authentication
- Rate Limiting
- CORS Protection
- Encrypted Vote Storage
- Audit Logging
"""
import subprocess
import threading
import time
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Import our security modules
from auth import require_auth, require_admin, create_token, hash_password, verify_password
from database import (
    create_voter, get_voter_by_email, get_voter_by_id,
    has_voted, mark_as_voted, log_action,
    get_voter_count, get_votes_count
)
from crypto_utils import encrypt_vote, decrypt_vote, sha256_hash

# Load environment variables
load_dotenv()

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BIN_DIR = os.path.join(PROJECT_ROOT, 'bin')
WEB_DIR = os.path.join(PROJECT_ROOT, 'web', 'voting_booth')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-in-production')

# CORS Configuration - Allow specific origins
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5000,http://localhost:5001').split(',')
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# Rate Limiting Configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://"  # Use Redis in production: redis://localhost:6379
)

# Global process handler
class VoteSystemProcess:
    def __init__(self):
        exe_path = os.path.join(BIN_DIR, 'SecureVoteSystem.exe')
        try:
            self.process = subprocess.Popen(
                [exe_path, '--interactive'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        except FileNotFoundError:
            print(f"Warning: C++ executable not found at {exe_path}")
            print("Running in mock mode for development")
            self.process = None

    def send_command(self, command):
        if self.process is None:
            return "ERROR: C++ backend not available"
        
        if self.process.poll() is not None:
            return "ERROR: Process ended"
        
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        
        # Read response
        output = self.process.stdout.readline().strip()
        return output

system = VoteSystemProcess()

# ============================================================================
# PUBLIC ROUTES (No Authentication Required)
# ============================================================================

@app.route('/')
def index():
    """Serve the voting booth interface"""
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'registered_voters': get_voter_count(),
        'votes_cast': get_votes_count()
    })

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")  # Prevent registration spam
def register():
    """Register a new voter"""
    data = request.json
    
    # Validate input
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Check if email already exists
    existing = get_voter_by_email(email)
    if existing:
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password and create voter
    password_hash = hash_password(password)
    voter_id = create_voter(email, password_hash, full_name)
    
    # Log registration
    log_action(voter_id, 'REGISTER', f'New voter registered: {email}', request.remote_addr)
    
    # Create token
    token = create_token(voter_id, email)
    
    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'voter_id': voter_id
    }), 201

@app.route('/login', methods=['POST'])
@limiter.limit("10 per hour")  # Prevent brute force
def login():
    """Authenticate a voter and return JWT token"""
    data = request.json
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    # Get voter from database
    voter = get_voter_by_email(email)
    if not voter:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    if not verify_password(password, voter['password_hash']):
        log_action(voter['id'], 'LOGIN_FAILED', 'Invalid password attempt', request.remote_addr)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create token
    token = create_token(voter['id'], voter['email'])
    
    # Log successful login
    log_action(voter['id'], 'LOGIN', 'Successful login', request.remote_addr)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'voter_id': voter['id'],
        'has_voted': voter['has_voted']
    })

# ============================================================================
# PROTECTED ROUTES (Authentication Required)
# ============================================================================

@app.route('/vote', methods=['POST'])
@require_auth
@limiter.limit("1 per day")  # One vote per day per user
def vote():
    """Submit a vote (requires authentication)"""
    data = request.json
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': 'Vote content required'}), 400
    
    voter_id = request.voter_id
    
    # Check if already voted
    if has_voted(voter_id):
        log_action(voter_id, 'VOTE_DUPLICATE', 'Attempted to vote twice', request.remote_addr)
        return jsonify({'error': 'You have already voted'}), 403
    
    # Encrypt the vote
    encrypted_content = encrypt_vote(content)
    
    # Send to C++ backend with encrypted content
    response = system.send_command(f"VOTE {voter_id} {encrypted_content}")
    
    # Mark as voted
    if "SUCCESS" in response or "ERROR" not in response:
        mark_as_voted(voter_id)
        log_action(voter_id, 'VOTE_CAST', f'Vote cast successfully', request.remote_addr)
        
        return jsonify({
            'status': 'success',
            'message': 'Vote recorded successfully',
            'encrypted': True
        })
    else:
        log_action(voter_id, 'VOTE_FAILED', f'Vote failed: {response}', request.remote_addr)
        return jsonify({'error': 'Failed to record vote'}), 500

@app.route('/profile', methods=['GET'])
@require_auth
def profile():
    """Get voter profile information"""
    voter = get_voter_by_id(request.voter_id)
    
    if not voter:
        return jsonify({'error': 'Voter not found'}), 404
    
    return jsonify({
        'voter_id': voter['id'],
        'email': voter['email'],
        'full_name': voter['full_name'],
        'has_voted': voter['has_voted'],
        'voted_at': voter['voted_at'],
        'created_at': voter['created_at']
    })

# ============================================================================
# ADMIN ROUTES (Admin Authentication Required)
# ============================================================================

@app.route('/status', methods=['GET'])
@require_admin
def status():
    """Get system status (admin only)"""
    response = system.send_command("STATUS")
    return response  # Already JSON string from C++

@app.route('/tally', methods=['GET'])
@require_admin
def tally():
    """Get vote tallies (admin only)"""
    response = system.send_command("TALLY")
    return response

@app.route('/admin/stats', methods=['GET'])
@require_admin
def admin_stats():
    """Get detailed system statistics (admin only)"""
    return jsonify({
        'total_registered': get_voter_count(),
        'total_voted': get_votes_count(),
        'turnout_percentage': (get_votes_count() / max(get_voter_count(), 1)) * 100
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("  Secure Vote-Transfer System - Voting Node")
    print("  Production Security Features Enabled")
    print("=" * 60)
    print(f"  Registered Voters: {get_voter_count()}")
    print(f"  Votes Cast: {get_votes_count()}")
    print("=" * 60)
    
    # Run with SSL in production
    ssl_cert = os.getenv('SSL_CERT_PATH')
    ssl_key = os.getenv('SSL_KEY_PATH')
    
    if ssl_cert and ssl_key and os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        print("  Running with HTTPS (SSL enabled)")
        app.run(host='0.0.0.0', port=5000, ssl_context=(ssl_cert, ssl_key))
    else:
        print("  Running with HTTP (development mode)")
        print("  WARNING: Use HTTPS in production!")
        app.run(host='0.0.0.0', port=5000, debug=False)
