#!/usr/bin/env python
"""
Script to check Supabase project status and guide through table creation
"""

def check_supabase_status():
    """Check Supabase project status and provide guidance"""
    
    print("🔍 Supabase Project Status Check")
    print("=" * 50)
    
    print("📝 Your Supabase Project Details:")
    print("Project URL: https://ydexeftnucyjnorycrpd.supabase.co")
    print("Project Reference: ydexeftnucyjnorycrpd")
    print("Database Password: Abtrs@2025")
    print()
    
    print("🔍 What to Check in Your Supabase Dashboard:")
    print("1. Go to your Supabase project dashboard")
    print("2. Check if the project status is 'Active' (not paused)")
    print("3. Go to 'Table Editor' - it should be empty initially")
    print("4. Go to 'SQL Editor' - you can run queries here")
    print()
    
    print("📋 Expected Tables (after migrations):")
    print("Django Core Tables:")
    print("  - auth_group")
    print("  - auth_permission") 
    print("  - auth_user")
    print("  - django_admin_log")
    print("  - django_content_type")
    print("  - django_migrations")
    print("  - django_session")
    print()
    print("Your App Tables:")
    print("  - accounts_user")
    print("  - routes_route")
    print("  - buses_bus")
    print("  - buses_seat")
    print("  - bookings_booking")
    print("  - terminals_terminal")
    print("  - gps_tracking_driver")
    print("  - gps_tracking_buslocation")
    print("  - gps_tracking_speedalert")
    print("  - gps_tracking_routeprogress")
    print("  - gps_tracking_geofencearea")
    print("  - gps_tracking_emergencyalert")
    print("  - core_sitesettings")
    print()
    
    print("🚀 How to Create Tables:")
    print("Method 1: Deploy to Vercel first (Recommended)")
    print("  1. Deploy your Django app to Vercel")
    print("  2. Visit: your-vercel-url.vercel.app/api/migrate")
    print("  3. Check Supabase Table Editor for created tables")
    print()
    print("Method 2: Manual SQL (Alternative)")
    print("  1. Go to Supabase SQL Editor")
    print("  2. Run the SQL commands I'll provide")
    print()
    
    print("❓ Current Status:")
    print("- If you see NO tables: This is normal! Tables need to be created")
    print("- If project is paused: Unpause it in project settings")
    print("- If connection fails: Check your database credentials")

if __name__ == '__main__':
    check_supabase_status()
