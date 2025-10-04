#!/usr/bin/env python
"""
Script to test Supabase database connection
"""

import os
import psycopg2
from psycopg2 import sql

def test_supabase_connection():
    """Test connection to Supabase database"""
    
    # Supabase connection details
    host = "db.ydexeftnucyjnorycrpd.supabase.co"
    database = "postgres"
    port = "5432"
    user = "postgres"
    
    print("🔗 Testing Supabase database connection...")
    print(f"Host: {host}")
    print(f"Database: {database}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print()
    
    # You'll need to enter your password
    password = input("Enter your Supabase database password: ")
    
    try:
        # Test connection
        conn = psycopg2.connect(
            host=host,
            database=database,
            port=port,
            user=user,
            password=password,
            sslmode='require'
        )
        
        print("✅ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 Database version: {version[0]}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n📝 Your Vercel environment variables should be:")
        print(f"DB_HOST={host}")
        print(f"DB_NAME={database}")
        print(f"DB_USER={user}")
        print(f"DB_PASSWORD={password}")
        print(f"DB_PORT={port}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Check if your password is correct")
        print("2. Make sure your Supabase project is active")
        print("3. Verify the project reference in the URL")
        return False

if __name__ == '__main__':
    test_supabase_connection()
