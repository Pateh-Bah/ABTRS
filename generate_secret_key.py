#!/usr/bin/env python
"""
Generate a secure Django secret key for production
"""

import secrets
import string

def generate_secret_key():
    """Generate a secure Django secret key"""
    
    # Django secret key characters
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Generate a 50-character secret key
    secret_key = ''.join(secrets.choice(chars) for _ in range(50))
    
    print("🔐 Generated Django Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    print()
    print("📝 Copy this value and add it to your Vercel environment variables")
    
    return secret_key

if __name__ == '__main__':
    generate_secret_key()
