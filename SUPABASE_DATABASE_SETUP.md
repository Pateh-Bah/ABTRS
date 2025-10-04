# 🗄️ Supabase Database Setup Guide

## ✅ What We've Prepared

Your Django project has **18 models** across **6 apps** that need to be created in Supabase:

### 📱 Django Apps and Models:

#### Core Django Apps:
- **django.contrib.admin**: LogEntry
- **django.contrib.auth**: Permission, Group  
- **django.contrib.contenttypes**: ContentType
- **django.contrib.sessions**: Session
- **django.contrib.messages**: (no models)
- **django.contrib.staticfiles**: (no models)

#### Your Custom Apps:
- **accounts**: User (custom user model)
- **routes**: Route
- **buses**: Bus, Seat
- **bookings**: Booking
- **terminals**: Terminal
- **gps_tracking**: Driver, BusLocation, SpeedAlert, RouteProgress, GeofenceArea, EmergencyAlert
- **core**: SiteSettings

## 🚀 Method 1: Deploy to Vercel First (Recommended)

### Step 1: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your ABTRS repository
3. Add these environment variables:

```
DB_HOST=db.ydexeftnucyjnorycrpd.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Abtrs@2025
DB_PORT=5432
SECRET_KEY=)G2(AjgvT6Rc7@oY(laWNKW&!JuRnl+SMz9J17aiUjf#kcZOBz
DEBUG=False
GOOGLE_MAPS_API_KEY=AIzaSyAvP5QtAlj_WcbZ84Yoo2K_I_MGW8guO30
SUPABASE_URL=https://ydexeftnucyjnorycrpd.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlkZXhlZnRudWN5am5vcnljcnBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0OTM0NDUsImV4cCI6MjA3NTA2OTQ0NX0.QpzB4MN-7WIhjSSLyR8x9Mguj904HpI40AgokU-RhLE
```

4. Click "Deploy"

### Step 2: Run Migrations
1. After deployment, visit: `https://your-vercel-url.vercel.app/api/migrate`
2. You should see: `{"status": "success", "message": "Migrations completed successfully"}`

### Step 3: Verify Tables in Supabase
1. Go to your [Supabase dashboard](https://supabase.com/dashboard)
2. Open your project
3. Go to **Table Editor**
4. You should see all these tables created:

**Django Core Tables:**
- auth_group
- auth_permission
- auth_user (your custom user model)
- django_admin_log
- django_content_type
- django_migrations
- django_session

**Your App Tables:**
- accounts_user
- routes_route
- buses_bus
- buses_seat
- bookings_booking
- terminals_terminal
- gps_tracking_driver
- gps_tracking_buslocation
- gps_tracking_speedalert
- gps_tracking_routeprogress
- gps_tracking_geofencearea
- gps_tracking_emergencyalert
- core_sitesettings

## 🚀 Method 2: Manual SQL Setup (Alternative)

If you prefer to set up tables manually:

### Step 1: Get SQL Schema
1. Run: `python manage.py sqlmigrate accounts 0001`
2. Run: `python manage.py sqlmigrate routes 0001`
3. Run: `python manage.py sqlmigrate buses 0001`
4. Run: `python manage.py sqlmigrate bookings 0001`
5. Run: `python manage.py sqlmigrate terminals 0001`
6. Run: `python manage.py sqlmigrate gps_tracking 0001`
7. Run: `python manage.py sqlmigrate core 0001`

### Step 2: Execute in Supabase
1. Go to your Supabase dashboard
2. Go to **SQL Editor**
3. Paste and execute each SQL script

## 🎯 Expected Results

After successful setup, you should have:

### ✅ All Tables Created
- **18+ tables** in your Supabase database
- All Django migrations applied
- Database ready for your application

### ✅ Admin Access
- Django admin panel accessible at `/admin`
- Superuser account for management

### ✅ Full Functionality
- User registration/login
- Route management
- Bus and seat management
- Booking system
- GPS tracking
- QR code generation

## 🔧 Troubleshooting

### If migrations fail:
1. Check environment variables are correct
2. Verify Supabase project is active
3. Check Vercel build logs for errors

### If tables are missing:
1. Run migrations again: `/api/migrate`
2. Check Supabase Table Editor
3. Verify all apps have migrations

### If connection fails:
1. Verify database credentials
2. Check Supabase project status
3. Ensure SSL is enabled

## 🎉 Success!

Once all tables are created:
- Your Django app is fully connected to Supabase
- All functionality will work
- Data will persist in PostgreSQL
- You can manage everything through Django admin

**Your bus booking system is now ready for production! 🚌✨**
