# 📊 Insert Sample Data Guide

## 🎯 What We've Fixed

### ✅ Admin User Management Issues Fixed:
1. **Fixed form field names** in `AdminUserCreateFormWithDriver` and `AdminUserEditFormWithDriver`
2. **Fixed emergency_contact field references** 
3. **Fixed placeholder field names**
4. **Added favicon links** to prevent 404 errors
5. **Created Tailwind CSS file** for production use

### ✅ Sample Data Created:
- **SQL script**: `insert_sample_data.sql` - Ready to run in Supabase
- **Python script**: `insert_sample_data.py` - Ready to run locally
- **Comprehensive data** for all tables

## 🚀 How to Insert Sample Data

### Method 1: Using SQL Script (Recommended for Supabase)

#### Step 1: Go to Supabase SQL Editor
1. **Open your Supabase dashboard**
2. **Go to SQL Editor**
3. **Click "New Query"**

#### Step 2: Run the SQL Script
1. **Copy the contents of `insert_sample_data.sql`**
2. **Paste it into the SQL Editor**
3. **Click "Run"**

#### Step 3: Verify Data
1. **Go to Table Editor**
2. **Check each table** - you should see sample data

### Method 2: Using Python Script (For Local Development)

#### Step 1: Run the Python Script
```bash
python insert_sample_data.py
```

#### Step 2: Verify Data
Check your local database for the inserted data.

## 📋 Sample Data Includes:

### 🏢 Core Data:
- **Site Settings**: ABTRS configuration
- **1 Superuser**: admin/admin123

### 🚏 Terminals (6 terminals):
- Freetown Central Terminal
- Bo Terminal  
- Kenema Terminal
- Makeni Terminal
- Koidu Terminal
- Port Loko Terminal

### 🛣️ Routes (7 routes):
- Freetown to Bo (250.5 km, 180 min, $45.00)
- Bo to Kenema (85.2 km, 60 min, $25.00)
- Freetown to Makeni (120.8 km, 90 min, $35.00)
- Makeni to Koidu (95.3 km, 75 min, $30.00)
- Freetown to Port Loko (65.4 km, 45 min, $20.00)
- Bo to Makeni (180.6 km, 120 min, $40.00)
- Kenema to Koidu (110.7 km, 80 min, $32.00)

### 🚌 Buses (8 buses):
- AB001: Mercedes-Benz Sprinter (50 seats)
- AB002: Toyota Coaster (45 seats)
- AB003: Isuzu NPR (55 seats)
- AB004: Nissan Civilian (48 seats)
- AB005: Mitsubishi Rosa (52 seats)
- AB006: Hino Rainbow (46 seats)
- AB007: Mercedes-Benz Sprinter (50 seats)
- AB008: Toyota Coaster (44 seats)

### 💺 Seats (400+ seats):
- **4 seats per row** (A, B, C, D)
- **Available by default**
- **Properly linked to buses**

### 👨‍💼 Drivers (8 drivers):
- **Driver profiles** with license numbers
- **Emergency contacts**
- **Linked to users**

### 👥 Users (4 sample users):
- **admin**: System Administrator
- **john_doe**: Driver
- **jane_smith**: Passenger  
- **mike_wilson**: Passenger

### 🎫 Bookings (3 sample bookings):
- **Confirmed bookings** with different payment methods
- **Seat assignments**
- **Proper status tracking**

### 📍 GPS Tracking Data:
- **Bus locations** with coordinates and speed
- **Geofence areas** around terminals
- **Speed alerts** for overspeeding
- **Emergency alerts** for various scenarios
- **Route progress** tracking

## 🔑 Login Credentials:

### Admin Access:
- **Username**: admin
- **Password**: admin123
- **Access**: Full admin panel

### Driver Access:
- **Username**: john_doe
- **Password**: driver123
- **Access**: Driver dashboard

### Passenger Access:
- **Username**: jane_smith
- **Password**: passenger123
- **Access**: Booking system

## 🎯 Expected Results:

After inserting sample data, you should see:

### ✅ In Supabase Table Editor:
- **6 terminals** with coordinates
- **7 routes** with pricing
- **8 buses** with different capacities
- **400+ seats** properly assigned
- **8 drivers** with profiles
- **4 users** including admin
- **3 bookings** with different statuses
- **GPS tracking data** for all buses
- **Geofence areas** around terminals
- **Speed and emergency alerts**

### ✅ In Your Application:
- **Working admin panel** with user management
- **Functional booking system** with real data
- **GPS tracking** with live data
- **Route management** with sample routes
- **Bus management** with assigned drivers

## 🔧 Troubleshooting:

### If SQL script fails:
1. **Check if tables exist** first
2. **Run table creation script** if needed
3. **Check for foreign key constraints**
4. **Verify data types match**

### If Python script fails:
1. **Check database connection**
2. **Verify all models are imported**
3. **Check for duplicate data**
4. **Run migrations first**

### If data doesn't appear:
1. **Refresh the Table Editor**
2. **Check for error messages**
3. **Verify script execution**
4. **Check database permissions**

## 🎉 Success!

Once sample data is inserted:
- ✅ **Your database is populated** with realistic data
- ✅ **All functionality is testable** with real data
- ✅ **Admin panel works** with user management
- ✅ **Booking system works** with routes and buses
- ✅ **GPS tracking works** with sample locations

**Your ABTRS system is now fully functional with sample data! 🚌✨**
