"""
Utility script to generate secure random keys for production deployment
Run this script and copy the output to your .env file
"""
import secrets

def generate_key(length=64):
    """Generate a secure random key"""
    return secrets.token_urlsafe(length)

if __name__ == '__main__':
    print("=" * 70)
    print("  Secure Vote-Transfer System - Key Generator")
    print("=" * 70)
    print("\nGenerated Security Keys (copy to .env file):\n")
    print(f"JWT_SECRET_KEY={generate_key(64)}")
    print(f"FLASK_SECRET_KEY={generate_key(64)}")
    print(f"ENCRYPTION_KEY={generate_key(32)}")
    print("\n" + "=" * 70)
    print("IMPORTANT: Keep these keys secret and never commit them to Git!")
    print("=" * 70)
