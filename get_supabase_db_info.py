#!/usr/bin/env python
"""
Script to get correct Supabase database information
"""

import requests
import json

def get_supabase_info():
    """Get Supabase project information"""
    
    print("🔍 Getting Supabase project information...")
    print("=" * 50)
    
    # Your Supabase project details
    project_ref = "ydexeftnucyjnorycrpd"
    supabase_url = f"https://ydexeftnucyjnorycrpd.supabase.co"
    
    print(f"📝 Project Reference: {project_ref}")
    print(f"📝 Project URL: {supabase_url}")
    print()
    
    # Try to get project info from Supabase API
    try:
        # This is a public endpoint that should work
        api_url = f"https://api.supabase.com/v1/projects/{project_ref}"
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkZXhlZnRudWN5am5vcnljcnBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTM0NDUsImV4cCI6MjA3NTA2OTQ0NX0.QpzB4MN-7WIhjSSLyR8x9Mguj904HpI40AgokU-RhLE'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Project information retrieved:")
            print(f"  - Name: {data.get('name', 'N/A')}")
            print(f"  - Status: {data.get('status', 'N/A')}")
            print(f"  - Region: {data.get('region', 'N/A')}")
        else:
            print(f"⚠️  Could not get project info (Status: {response.status_code})")
            
    except Exception as e:
        print(f"⚠️  Could not connect to Supabase API: {e}")
    
    print()
    print("🔧 Database Connection Details:")
    print("Host: db.ydexeftnucyjnorycrpd.supabase.co")
    print("Database: postgres")
    print("Port: 5432")
    print("User: postgres")
    print("Password: Abtrs@2025")
    print()
    
    print("💡 Connection Issues:")
    print("1. The hostname might be different - check your Supabase dashboard")
    print("2. Go to Settings → Database in your Supabase project")
    print("3. Copy the exact connection string from there")
    print("4. The connection will work on Vercel's servers")
    print()
    
    print("🚀 Alternative: Deploy to Vercel first, then run migrations there")
    print("1. Deploy to Vercel with the environment variables")
    print("2. Visit your-vercel-url.vercel.app/api/migrate")
    print("3. This will create all tables in Supabase")

if __name__ == '__main__':
    get_supabase_info()
