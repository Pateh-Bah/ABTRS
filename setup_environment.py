#!/usr/bin/env python
"""
Script to help set up environment variables for Supabase connection
"""

def setup_environment():
    """Display environment variables needed for Supabase connection"""
    
    print("🔧 Environment Variables Setup")
    print("=" * 50)
    print()
    
    print("📝 Add these environment variables to your Vercel project:")
    print()
    
    print("Database Configuration:")
    print("DB_HOST=db.ydexeftnucyjnorycrpd.supabase.co")
    print("DB_NAME=postgres")
    print("DB_USER=postgres")
    print("DB_PASSWORD=[Your Supabase database password]")
    print("DB_PORT=5432")
    print()
    
    print("Django Configuration:")
    print("SECRET_KEY=[Generate using generate_secret_key.py]")
    print("DEBUG=False")
    print("GOOGLE_MAPS_API_KEY=AIzaSyAvP5QtAlj_WcbZ84Yoo2K_I_MGW8guO30")
    print()
    
    print("Supabase Configuration:")
    print("SUPABASE_URL=https://ydexeftnucyjnorycrpd.supabase.co")
    print("SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkZXhlZnRudWN5am5vcnljcnBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTM0NDUsImV4cCI6MjA3NTA2OTQ0NX0.QpzB4MN-7WIhjSSLyR8x9Mguj904HpI40AgokU-RhLE")
    print()
    
    print("🚀 Next Steps:")
    print("1. Run: python generate_secret_key.py")
    print("2. Copy the generated SECRET_KEY")
    print("3. Add all environment variables to Vercel")
    print("4. Run: python setup_supabase_database.py")
    print("5. Deploy to Vercel")

if __name__ == '__main__':
    setup_environment()
