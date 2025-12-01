"""
Authentication module for JWT-based voter authentication
"""
import jwt
import bcrypt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Load from environment or use default for development
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def create_token(voter_id: int, email: str) -> str:
    """Create a JWT token for authenticated user"""
    payload = {
        'voter_id': voter_id,
        'email': email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token: str) -> dict:
    """Decode and verify a JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            payload = decode_token(token)
            
            # Add user info to request context
            request.voter_id = payload['voter_id']
            request.voter_email = payload['email']
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            payload = decode_token(token)
            
            # Check if user is admin
            if not payload.get('is_admin', False):
                return jsonify({'error': 'Admin access required'}), 403
            
            request.voter_id = payload['voter_id']
            request.voter_email = payload['email']
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except Exception:
            return jsonify({'error': 'Authentication failed'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
