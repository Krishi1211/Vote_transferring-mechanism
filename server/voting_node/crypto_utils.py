"""
Cryptography utilities for vote encryption and hashing
Uses Python's cryptography library for production-grade security
"""
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

# Encryption key (should be loaded from environment in production)
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'dev-key-32-bytes-change-prod!!')

def sha256_hash(data: str) -> str:
    """
    Compute SHA-256 hash of data
    Returns hex string of hash
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def sha256_hash_bytes(data: bytes) -> bytes:
    """
    Compute SHA-256 hash of bytes
    Returns raw bytes
    """
    return hashlib.sha256(data).digest()

def derive_key(password: str, salt: bytes = None) -> tuple:
    """
    Derive a cryptographic key from a password using PBKDF2
    Returns (key, salt)
    """
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    return key, salt

def encrypt_vote(plaintext: str, key: bytes = None) -> str:
    """
    Encrypt vote data using AES-256-GCM
    Returns base64-encoded ciphertext with nonce
    """
    if key is None:
        # Use default key (derive from ENCRYPTION_KEY)
        key, _ = derive_key(ENCRYPTION_KEY, b'fixed-salt-12345')  # Fixed salt for consistency
    
    # Generate random nonce
    nonce = os.urandom(12)
    
    # Create AESGCM cipher
    aesgcm = AESGCM(key)
    
    # Encrypt
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    
    # Combine nonce + ciphertext and encode
    combined = nonce + ciphertext
    return base64.b64encode(combined).decode('utf-8')

def decrypt_vote(encrypted: str, key: bytes = None) -> str:
    """
    Decrypt vote data using AES-256-GCM
    Returns plaintext
    """
    if key is None:
        # Use default key
        key, _ = derive_key(ENCRYPTION_KEY, b'fixed-salt-12345')
    
    # Decode from base64
    combined = base64.b64decode(encrypted.encode('utf-8'))
    
    # Split nonce and ciphertext
    nonce = combined[:12]
    ciphertext = combined[12:]
    
    # Create AESGCM cipher
    aesgcm = AESGCM(key)
    
    # Decrypt
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')

def secure_random_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token
    Returns base64-encoded token
    """
    return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')

def hash_voter_id(voter_id: int, salt: str = "vote-system-salt") -> str:
    """
    Hash voter ID for anonymous shard routing
    Returns hex string
    """
    data = f"{voter_id}{salt}"
    return sha256_hash(data)

# Test encryption/decryption on module load (development only)
if __name__ == '__main__':
    test_vote = "Vote for Candidate A"
    encrypted = encrypt_vote(test_vote)
    decrypted = decrypt_vote(encrypted)
    
    print(f"Original: {test_vote}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_vote == decrypted}")
    
    print(f"\nSHA-256 Hash: {sha256_hash(test_vote)}")
