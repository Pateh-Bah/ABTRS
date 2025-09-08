#!/usr/bin/env python3
"""
Simple GPS Tracker for Raspberry Pi
This script reads GPS data from a serial GPS module and sends it to your Wakafine server.
"""

import time
import requests
import serial
import sys
from datetime import datetime

class SimpleGPSTracker:
    def __init__(self, bus_id, server_url, gps_port='/dev/ttyS0', baud_rate=9600):
        self.bus_id = bus_id
        self.server_url = server_url
        self.gps_port = gps_port
        self.baud_rate = baud_rate
        self.serial_conn = None

    def connect_gps(self):
        """Connect to GPS module"""
        try:
            self.serial_conn = serial.Serial(
                self.gps_port,
                self.baud_rate,
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            print(f"✅ Connected to GPS on {self.gps_port}")
            return True
        except Exception as e:
            print(f"❌ GPS connection failed: {e}")
            return False

    def parse_nmea(self, nmea_sentence):
        """Parse NMEA GPS sentence"""
        try:
            parts = nmea_sentence.split(',')
            if parts[0] == '$GPGGA' and len(parts) >= 10:
                # $GPGGA sentence contains position data
                latitude = parts[2]
                lat_dir = parts[3]
                longitude = parts[4]
                lon_dir = parts[5]
                fix_quality = parts[6]

                if fix_quality == '0':
                    return None  # No GPS fix

                # Convert to decimal degrees
                if latitude and longitude:
                    lat_deg = float(latitude[:2])
                    lat_min = float(latitude[2:])
                    lat_decimal = lat_deg + (lat_min / 60)
                    if lat_dir == 'S':
                        lat_decimal = -lat_decimal

                    lon_deg = float(longitude[:3])
                    lon_min = float(longitude[3:])
                    lon_decimal = lon_deg + (lon_min / 60)
                    if lon_dir == 'W':
                        lon_decimal = -lon_decimal

                    return {
                        'latitude': lat_decimal,
                        'longitude': lon_decimal,
                        'fix_quality': int(fix_quality)
                    }
        except Exception as e:
            print(f"NMEA parsing error: {e}")

        return None

    def send_location(self, gps_data):
        """Send GPS data to server"""
        try:
            url = f"{self.server_url}/gps/api/bus/{self.bus_id}/update-location/"
            data = {
                "latitude": gps_data['latitude'],
                "longitude": gps_data['longitude'],
                "speed": 0,  # Will be calculated by server if needed
                "heading": 0,
                "accuracy": 10  # Default accuracy
            }

            response = requests.post(
                url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                print(f"✅ Location sent: {gps_data['latitude']:.6f}, {gps_data['longitude']:.6f}")
                return True
            else:
                print(f"❌ Server error: {response.status_code} - {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
        except Exception as e:
            print(f"❌ Send error: {e}")
            return False

    def run(self):
        """Main tracking loop"""
        print(f"🚀 Starting GPS tracker for Bus {self.bus_id}")
        print(f"Server: {self.server_url}")
        print(f"GPS Port: {self.gps_port}")

        if not self.connect_gps():
            print("❌ Cannot connect to GPS module. Exiting.")
            return

        print("📡 Listening for GPS data... (Press Ctrl+C to stop)")

        try:
            while True:
                try:
                    if self.serial_conn.in_waiting > 0:
                        line = self.serial_conn.readline().decode('ascii', errors='replace').strip()

                        if line.startswith('$GPGGA'):
                            gps_data = self.parse_nmea(line)
                            if gps_data:
                                self.send_location(gps_data)
                                time.sleep(10)  # Send every 10 seconds
                            else:
                                print("📍 No GPS fix available")

                except UnicodeDecodeError:
                    continue  # Skip invalid data
                except Exception as e:
                    print(f"❌ Read error: {e}")
                    time.sleep(1)

        except KeyboardInterrupt:
            print("\n⏹️  GPS tracker stopped by user")
        finally:
            if self.serial_conn:
                self.serial_conn.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python gps_tracker.py <bus_id> <server_url>")
        print("Example: python gps_tracker.py 1 http://127.0.0.1:8000")
        sys.exit(1)

    bus_id = sys.argv[1]
    server_url = sys.argv[2]

    tracker = SimpleGPSTracker(
        bus_id=bus_id,
        server_url=server_url,
        gps_port='/dev/ttyS0'  # Change this based on your GPS module
    )

    tracker.run()

if __name__ == "__main__":
    main()</content>
<parameter name="filePath">c:\Users\pateh\Videos\Dissertation\wakafine\wakafine\raspberry_pi_gps_tracker.py