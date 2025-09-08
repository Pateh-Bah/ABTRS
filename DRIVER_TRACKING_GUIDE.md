# Driver Tracking System - Complete Guide

## Overview
The Wakafine GPS tracking system provides real-time location monitoring for bus drivers and fleet management. This guide explains how drivers can use the system and how administrators can track vehicles.

---

## 🚗 For Drivers: How to Share Your Location

### Step 1: Access the Driver Tracking App
1. **Log in** to your driver account on the Wakafine system
2. **Navigate** to the Driver Tracking page: `http://yourdomain.com/gps/driver/tracking/`
3. **Bookmark** this page on your mobile device for quick access

### Step 2: Start Location Tracking
1. **Grant Permission**: When prompted, allow location access in your browser
2. **Check Settings**:
   - Update Interval: Choose how often to send location (5-30 seconds)
   - High Accuracy GPS: Enable for better precision (uses more battery)
   - Vibrate on Update: Get feedback when location is sent
3. **Tap "Start Tracking"** to begin sharing your location

### Step 3: Monitor Your Tracking Session
- **Green indicator**: Location tracking is active
- **Real-time stats**: See updates sent and session time
- **Current location**: View your exact coordinates and speed
- **Activity log**: Track all system events and errors

### Step 4: Emergency Features
- **Red Emergency Button**: Tap for immediate alert to control center
- **Automatic alerts**: System detects speeding and sends alerts
- **Connection status**: Monitor if your location data is reaching the server

### Best Practices for Drivers:
✅ **Start tracking at the beginning of your shift**
✅ **Keep the app open in your browser**
✅ **Ensure strong mobile data connection**
✅ **Charge your device - GPS tracking uses battery**
✅ **Test the emergency button during training**

❌ **Don't close the browser tab while tracking**
❌ **Don't disable location services**
❌ **Don't use airplane mode while on duty**

---

## 🖥️ For Administrators: How to Track Drivers

### Step 1: Access the GPS Management Dashboard
1. **Log in** as an administrator
2. **Navigate** to GPS Tracking: `http://yourdomain.com/gps/`
3. **View options**:
   - Public Map: Real-time map of all buses
   - Admin Dashboard: Detailed management interface

### Step 2: Real-Time Bus Monitoring
#### Public Map Features:
- **Live bus locations** with colored indicators:
  - 🟢 Green: Bus is moving (online)
  - 🟠 Orange: Bus is stopped (online)  
  - 🔴 Gray: Bus is offline (no recent updates)
- **Click any bus** to see detailed information
- **Auto-refresh** every 15 seconds
- **Bus status sidebar** with quick stats

#### Admin Dashboard Features:
- **Detailed bus list** with comprehensive status
- **Speed alerts** for buses exceeding limits
- **Emergency alerts** from drivers
- **Historical tracking data**
- **Route progress monitoring**

### Step 3: Understanding Bus Status
```
🟢 Online & Moving: Driver is actively sharing location, bus is in motion
🟠 Online & Stopped: Driver is sharing location but bus is stationary
🔴 Offline: No location updates received in the last 5 minutes
```

### Step 4: Responding to Alerts
#### Speed Alerts:
1. View alert details in admin dashboard
2. Contact driver if necessary
3. Mark alert as acknowledged
4. Monitor for repeated violations

#### Emergency Alerts:
1. **Immediate response required**
2. View exact location of emergency
3. Contact driver immediately
4. Dispatch assistance if needed
5. Mark alert as resolved when handled

---

## 📱 Technical Requirements

### For Drivers (Mobile Devices):
- **Modern smartphone** with GPS capability
- **Mobile browser** (Chrome, Safari, Firefox)
- **Mobile data** or WiFi connection
- **Location services** enabled
- **Battery management** (GPS is power-intensive)

### Browser Compatibility:
✅ Chrome (recommended)
✅ Safari (iOS)
✅ Firefox
✅ Edge
❌ Internet Explorer (not supported)

### Network Requirements:
- **Minimum**: 2G/EDGE data connection
- **Recommended**: 3G/4G/5G or WiFi
- **Data usage**: ~50KB per minute of tracking

---

## 🔧 Troubleshooting Common Issues

### Driver Issues:

#### "Location permission denied"
**Solution**: 
1. Go to browser settings
2. Find location permissions
3. Allow location for the tracking site

#### "Can't connect to server"  
**Solution**:
1. Check mobile data/WiFi connection
2. Try refreshing the page
3. Contact system administrator

#### "GPS accuracy is poor"
**Solution**:
1. Move to an area with clear sky view
2. Enable "High Accuracy GPS" in settings
3. Wait a few minutes for GPS to stabilize

### Administrator Issues:

#### "No buses showing on map"
**Solution**:
1. Check Google Maps API key configuration
2. Verify buses have assigned drivers
3. Confirm drivers are actively tracking

#### "Google Maps not loading"
**Solution**:
1. Verify API key in settings.py: `GOOGLE_MAPS_API_KEY`
2. Check API key has Maps JavaScript API enabled
3. Verify billing is set up for Google Cloud

---

## ⚙️ System Configuration

### Required Settings in `settings.py`:
```python
# Google Maps API Key (required)
GOOGLE_MAPS_API_KEY = 'your-google-maps-api-key-here'

# GPS Tracking Settings
GPS_UPDATE_INTERVAL = 10  # seconds
GPS_OFFLINE_THRESHOLD = 300  # 5 minutes
SPEED_LIMIT_THRESHOLD = 80  # km/h
```

### Database Models:
- **BusLocation**: Stores GPS coordinates and timestamps
- **SpeedAlert**: Records when buses exceed speed limits  
- **EmergencyAlert**: Handles driver emergency signals
- **RouteProgress**: Tracks progress along defined routes

---

## 📊 Monitoring and Analytics

### Real-Time Metrics:
- **Active buses**: Currently sharing location
- **Total distance**: Covered by all buses today
- **Average speed**: Across all active buses
- **Alert counts**: Speed violations and emergencies

### Historical Data:
- **Route history**: Complete path taken by each bus
- **Speed analysis**: Average speeds by route and time
- **Downtime tracking**: When buses were offline
- **Driver performance**: Based on alerts and compliance

---

## 🚀 Advanced Features

### Auto-Tracking Mode:
- Automatically starts tracking when driver logs in
- Uses device sensors to detect when vehicle is moving
- Saves battery by reducing update frequency when stopped

### Geofencing:
- Define virtual boundaries around terminals/stops
- Get alerts when buses enter/exit specific areas
- Track on-time performance for scheduled stops

### Route Optimization:
- Compare actual routes vs planned routes
- Identify traffic delay patterns
- Suggest alternative routes during peak hours

---

## 📞 Support and Contact

### For Technical Issues:
- **System Administrator**: Contact your IT department
- **Driver Training**: Schedule training sessions for new drivers
- **24/7 Support**: Emergency technical support hotline

### For Feature Requests:
- Submit enhancement requests through admin panel
- Regular system updates include new tracking features
- Custom reporting available for specific business needs

---

## 📋 Quick Reference

### Driver Checklist:
- [ ] Location permission granted
- [ ] Tracking started at shift beginning  
- [ ] Emergency button tested
- [ ] Good mobile signal confirmed
- [ ] Device charged and connected to power

### Admin Checklist:
- [ ] Google Maps API key configured
- [ ] All buses assigned to drivers
- [ ] Speed limit thresholds set appropriately
- [ ] Emergency response procedures in place
- [ ] Regular system monitoring scheduled

---

*This system provides comprehensive real-time tracking to improve fleet efficiency, driver safety, and passenger service quality.*