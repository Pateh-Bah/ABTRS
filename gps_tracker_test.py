# Bus GPS Data Transmission - Complete Setup Guide

## Overview
Your Wakafine system supports multiple methods for buses to transmit GPS location data. The system is already equipped with APIs to receive and process GPS data from various sources.

---

## 🚗 Method 1: Mobile App (Driver's Phone) - RECOMMENDED

### **Already Implemented!** ✅

Your system already includes a complete mobile tracking app for drivers.

### **How It Works:**
1. **Driver logs in** to their account
2. **Opens the tracking app** at `/gps/driver/tracking/`
3. **Grants location permission** in their browser
4. **Starts tracking** - app automatically sends GPS data every 10-30 seconds
5. **Data flows to your server** via the existing API

### **Setup Instructions:**

#### **For Drivers:**
1. **Access the app**: Go to `http://yourdomain.com/gps/driver/tracking/`
2. **Login** with driver credentials
3. **Grant location permission** when prompted
4. **Configure settings**:
   - Update interval (5-30 seconds)
   - High accuracy GPS mode
   - Vibration feedback
5. **Tap "Start Tracking"** to begin transmission

#### **Technical Details:**
- **API Endpoint**: `POST /gps/api/bus/{bus_id}/update-location/`
- **Data Format**:
```json
{
  "latitude": 8.4840,
  "longitude": -13.2299,
  "speed": 45.5,
  "heading": 90,
  "accuracy": 5.2,
  "timestamp": "2025-08-27T10:30:00Z"
}
```

---

## 📡 Method 2: Dedicated GPS Tracker Hardware

### **Compatible Devices:**
- **Teltonika** GPS trackers
- **Quectel** modules
- **u-blox** GPS receivers
- **Generic OBD-II** devices with GPS
- **Ruptela** trackers

### **Setup Instructions:**

#### **Hardware Requirements:**
- GPS tracker with cellular connectivity
- SIM card with data plan
- Power source (vehicle battery)

#### **Configuration Steps:**

1. **Configure Device IP/URL**:
   ```
   Server URL: http://yourdomain.com
   Port: 80 (or your Django port)
   Path: /gps/api/bus/{bus_id}/update-location/
   ```

2. **Set Data Format** (JSON):
   ```json
   {
     "latitude": "{latitude}",
     "longitude": "{longitude}",
     "speed": "{speed}",
     "heading": "{heading}",
     "accuracy": "{accuracy}"
   }
   ```

3. **Authentication**:
   - Use device IMEI as identifier
   - Or implement API key authentication

#### **Sample Python Script for Testing:**
```python
import requests
import json
import time
import random

# Simulate GPS tracker
def send_gps_data(bus_id, server_url):
    while True:
        # Simulate GPS coordinates (Freetown area)
        latitude = 8.4840 + random.uniform(-0.01, 0.01)
        longitude = -13.2299 + random.uniform(-0.01, 0.01)
        speed = random.uniform(0, 60)  # 0-60 km/h

        data = {
            "latitude": latitude,
            "longitude": longitude,
            "speed": speed,
            "heading": random.uniform(0, 360),
            "accuracy": random.uniform(3, 15)
        }

        try:
            response = requests.post(
                f"{server_url}/gps/api/bus/{bus_id}/update-location/",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"✅ Data sent: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(10)  # Send every 10 seconds

# Usage
send_gps_data(bus_id=1, server_url="http://127.0.0.1:8000")
```

---

## 🥧 Method 3: Raspberry Pi with GPS Module

### **Hardware Requirements:**
- **Raspberry Pi** (Zero W, 3B+, or 4)
- **GPS Module** (Neo-6M, Neo-8N, or similar)
- **GSM/GPRS Module** (optional, for cellular backup)
- **Power supply** and **antenna**

### **Software Setup:**

#### **1. Install Required Packages:**
```bash
sudo apt update
sudo apt install python3-pip gpsd gpsd-clients
sudo pip3 install requests pyserial pynmea2
```

#### **2. GPS Tracking Script:**
```python
#!/usr/bin/env python3
import time
import requests
import serial
import pynmea2
from datetime import datetime

class GPStracker:
    def __init__(self, bus_id, server_url, gps_port='/dev/ttyS0'):
        self.bus_id = bus_id
        self.server_url = server_url
        self.gps_port = gps_port
        self.serial_conn = None

    def connect_gps(self):
        try:
            self.serial_conn = serial.Serial(self.gps_port, 9600, timeout=1)
            print("✅ GPS module connected")
            return True
        except Exception as e:
            print(f"❌ GPS connection failed: {e}")
            return False

    def get_gps_data(self):
        if not self.serial_conn:
            return None

        try:
            line = self.serial_conn.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                msg = pynmea2.parse(line)
                if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                    return {
                        'latitude': msg.latitude,
                        'longitude': msg.longitude,
                        'speed': getattr(msg, 'spd_over_grnd', 0),
                        'heading': getattr(msg, 'true_course', 0),
                        'timestamp': datetime.now().isoformat()
                    }
        except Exception as e:
            print(f"GPS parsing error: {e}")

        return None

    def send_to_server(self, gps_data):
        try:
            url = f"{self.server_url}/gps/api/bus/{self.bus_id}/update-location/"
            response = requests.post(url, json=gps_data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Server error: {e}")
            return False

    def run(self):
        print(f"🚀 Starting GPS tracker for Bus {self.bus_id}")

        if not self.connect_gps():
            return

        while True:
            gps_data = self.get_gps_data()
            if gps_data:
                print(f"📍 GPS: {gps_data['latitude']:.6f}, {gps_data['longitude']:.6f}")
                if self.send_to_server(gps_data):
                    print("✅ Data sent to server")
                else:
                    print("❌ Failed to send data")

            time.sleep(10)  # Update every 10 seconds

# Usage
if __name__ == "__main__":
    tracker = GPStracker(
        bus_id=1,
        server_url="http://yourdomain.com",
        gps_port="/dev/ttyS0"  # Adjust based on your setup
    )
    tracker.run()
```

#### **3. Auto-start Setup:**
```bash
# Create service file
sudo nano /etc/systemd/system/gps-tracker.service

[Unit]
Description=GPS Tracker Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/gps_tracker.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable gps-tracker
sudo systemctl start gps-tracker
```

---

## 🚙 Method 4: Vehicle Telematics Integration

### **Compatible Systems:**
- **OBD-II** adapters with GPS
- **Fleet management systems**
- **Vehicle CAN bus** data
- **Telematics control units (TCU)**

### **Integration Approaches:**

#### **OBD-II Adapter:**
```python
import obd
import requests
import time

def obd_gps_tracker(bus_id, server_url):
    connection = obd.OBD()

    while True:
        # Get GPS data from OBD
        speed = connection.query(obd.commands.SPEED)
        gps_data = connection.query(obd.commands.GPS)

        if gps_data.value and speed.value:
            data = {
                "latitude": gps_data.value.latitude,
                "longitude": gps_data.value.longitude,
                "speed": speed.value.magnitude,
                "heading": 0,  # OBD might not provide heading
                "accuracy": 10  # Default accuracy
            }

            try:
                response = requests.post(
                    f"{server_url}/gps/api/bus/{bus_id}/update-location/",
                    json=data
                )
                print(f"✅ OBD data sent: {response.status_code}")
            except Exception as e:
                print(f"❌ OBD error: {e}")

        time.sleep(15)  # Update every 15 seconds

# Usage
obd_gps_tracker(bus_id=1, server_url="http://127.0.0.1:8000")
```

---

## 🔧 API Authentication & Security

### **Current API Security:**
- **CSRF Exempt**: Location updates don't require CSRF tokens
- **No Authentication**: Public API for easy integration
- **Bus ID Validation**: Ensures data goes to correct bus

### **Enhanced Security Options:**

#### **API Key Authentication:**
```python
# Add to settings.py
GPS_API_KEYS = {
    'device_001': 'your_secret_key_1',
    'device_002': 'your_secret_key_2',
}

# Modify UpdateBusLocationAPIView
def post(self, request, pk):
    api_key = request.headers.get('X-API-Key')
    if api_key not in settings.GPS_API_KEYS.values():
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    # ... rest of the code
```

#### **Device Registration:**
```python
# Create GPSDevice model
class GPSDevice(models.Model):
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
```

---

## 📊 Data Flow & Processing

### **Data Pipeline:**
1. **GPS Device** collects location data
2. **Device transmits** data to your server
3. **Django API** receives and validates data
4. **Data stored** in BusLocation model
5. **Bus model updated** with current location
6. **Speed alerts** generated if needed
7. **Public map** displays real-time locations

### **Data Validation:**
- **Coordinate validation**: -90 to 90 latitude, -180 to 180 longitude
- **Speed validation**: 0-200 km/h range
- **Accuracy filtering**: Discard inaccurate readings (>100m)
- **Timestamp validation**: Prevent old data submission

---

## 🛠️ Testing & Debugging

### **Test the API:**
```bash
# Test location update
curl -X POST http://127.0.0.1:8000/gps/api/bus/1/update-location/ \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 8.4840,
    "longitude": -13.2299,
    "speed": 45.5,
    "heading": 90,
    "accuracy": 5.2
  }'

# Test location retrieval
curl http://127.0.0.1:8000/gps/api/buses/locations/
```

### **Monitor Data:**
```python
# Check recent locations in Django shell
python manage.py shell
>>> from gps_tracking.models import BusLocation
>>> BusLocation.objects.order_by('-timestamp')[:5]
```

---

## 📋 Implementation Checklist

### **For Mobile App (Driver Phone):**
- [x] Driver tracking interface ready
- [x] API endpoint configured
- [ ] Assign buses to drivers
- [ ] Test location transmission
- [ ] Configure update intervals

### **For Hardware GPS Trackers:**
- [ ] Choose GPS device model
- [ ] Configure device server settings
- [ ] Set data transmission format
- [ ] Test device-to-server communication
- [ ] Install and power devices

### **For Raspberry Pi Setup:**
- [ ] Assemble hardware components
- [ ] Install GPS software
- [ ] Configure network connectivity
- [ ] Test GPS data collection
- [ ] Deploy tracking script

### **General Setup:**
- [x] Google Maps API key configured
- [x] Public tracking map accessible
- [ ] Create test bus data
- [ ] Test complete data flow
- [ ] Set up monitoring alerts

---

## 🚀 Quick Start (Mobile App Method)

The fastest way to get started:

1. **Create a driver account** in your Django admin
2. **Assign a bus** to the driver
3. **Have the driver**:
   - Go to `/gps/driver/tracking/` on their phone
   - Login with their credentials
   - Grant location permission
   - Start tracking

4. **Monitor in real-time** at `/gps/` (public map)

**That's it!** Your bus tracking system is now live! 🎉

---

## 📞 Support & Troubleshooting

### **Common Issues:**

#### **"Location permission denied"**
- Ensure browser has location access
- Try refreshing the page
- Check mobile browser settings

#### **"No data received on server"**
- Verify API endpoint URL
- Check network connectivity
- Review server logs for errors

#### **"Inaccurate GPS data"**
- Use high accuracy mode
- Ensure clear sky view
- Consider GPS antenna placement

#### **"Data transmission failures"**
- Check cellular/data signal
- Verify SIM card data plan
- Monitor device battery level

### **Debug Commands:**
```bash
# Check recent GPS data
python manage.py shell -c "
from gps_tracking.models import BusLocation
locations = BusLocation.objects.order_by('-timestamp')[:3]
for loc in locations:
    print(f'Bus {loc.bus.bus_number}: {loc.latitude}, {loc.longitude} @ {loc.speed} km/h')
"

# Clear old location data
python manage.py shell -c "
from gps_tracking.models import BusLocation
from django.utils import timezone
from datetime import timedelta
old_date = timezone.now() - timedelta(days=7)
BusLocation.objects.filter(timestamp__lt=old_date).delete()
print('Old location data cleared')
"
```

---

## 🎯 Next Steps

1. **Choose your transmission method** (mobile app is easiest)
2. **Test with one bus** first
3. **Monitor data quality** and adjust settings
4. **Scale to all buses** once working
5. **Set up alerts** for speed violations and emergencies

Your GPS tracking system is ready to receive data from any of these methods!</content>
<parameter name="filePath">c:\Users\pateh\Videos\Dissertation\wakafine\wakafine\BUS_GPS_TRANSMISSION_GUIDE.md