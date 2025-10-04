#!/usr/bin/env python
"""
Simple script to test Supabase database connection
"""

import os
import psycopg2

def test_connection():
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
    
    # You'll need to provide your password
    print("📝 To test the connection, you need to:")
    print("1. Go to your Supabase dashboard")
    print("2. Go to Settings → Database")
    print("3. Copy your database password")
    print("4. Run this command with your password:")
    print(f"   python -c \"import psycopg2; conn = psycopg2.connect(host='{host}', database='{database}', port='{port}', user='{user}', password='YOUR_PASSWORD', sslmode='require'); print('✅ Connection successful!')\"")
    print()
    
    print("🔧 Your Vercel environment variables should be:")
    print(f"DB_HOST={host}")
    print(f"DB_NAME={database}")
    print(f"DB_USER={user}")
    print("DB_PASSWORD=[Your Supabase password]")
    print(f"DB_PORT={port}")
    print()
    print("SECRET_KEY=)G2(AjgvT6Rc7@oY(laWNKW&!JuRnl+SMz9J17aiUjf#kcZOBz")
    print("DEBUG=False")
    print("GOOGLE_MAPS_API_KEY=AIzaSyAvP5QtAlj_WcbZ84Yoo2K_I_MGW8guO30")
    print("SUPABASE_URL=https://ydexeftnucyjnorycrpd.supabase.co")
    print("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkZXhlZnRudWN5am5vcnljcnBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTM0NDUsImV4cCI6MjA3NTA2OTQ0NX0.QpzB4MN-7WIhjSSLyR8x9Mguj904HpI40AgokU-RhLE")

if __name__ == '__main__':
    test_connection()
