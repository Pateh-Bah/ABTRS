#!/usr/bin/env python
"""
Simplified script to set up Supabase database
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def setup_database():
    """Set up the Supabase database"""
    print("🚀 Setting up Supabase database...")
    print()
    
    print("📝 To complete the database setup:")
    print("1. Go to your Supabase dashboard")
    print("2. Go to Settings → Database")
    print("3. Copy your database password")
    print("4. Set up your environment variables in Vercel")
    print()
    
    print("🔧 Environment Variables for Vercel:")
    print("DB_HOST=db.ydexeftnucyjnorycrpd.supabase.co")
    print("DB_NAME=postgres")
    print("DB_USER=postgres")
    print("DB_PASSWORD=[Your Supabase password]")
    print("DB_PORT=5432")
    print("SECRET_KEY=)G2(AjgvT6Rc7@oY(laWNKW&!JuRnl+SMz9J17aiUjf#kcZOBz")
    print("DEBUG=False")
    print("GOOGLE_MAPS_API_KEY=AIzaSyAvP5QtAlj_WcbZ84Yoo2K_I_MGW8guO30")
    print("SUPABASE_URL=https://ydexeftnucyjnorycrpd.supabase.co")
    print("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkZXhlZnRudWN5am5vcnljcnBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTM0NDUsImV4cCI6MjA3NTA2OTQ0NX0.QpzB4MN-7WIhjSSLyR8x9Mguj904HpI40AgokU-RhLE")
    print()
    
    print("🚀 Next Steps:")
    print("1. Add environment variables to Vercel")
    print("2. Push changes to GitHub")
    print("3. Deploy on Vercel")
    print("4. Run migrations via: https://your-vercel-url.vercel.app/api/migrate")
    print()
    
    print("✅ Database setup instructions completed!")

if __name__ == '__main__':
    setup_database()
