#!/usr/bin/env python3
"""
GPS Tracker Simulator
Simulates GPS data transmission from buses for testing purposes.
"""

import requests
import json
import time
import random
import sys
from datetime import datetime

class GPSSimulator:
    def __init__(self, bus_id, server_url):
        self.bus_id = bus_id
        self.server_url = server_url
        self.base_lat = 8.4840  # Freetown, Sierra Leone
        self.base_lon = -13.2299
        self.current_lat = self.base_lat
        self.current_lon = self.base_lon

    def generate_gps_data(self):
        """Generate realistic GPS movement data"""
        # Simulate movement (small random changes)
        lat_change = random.uniform(-0.001, 0.001)
        lon_change = random.uniform(-0.001, 0.001)

        self.current_lat += lat_change
        self.current_lon += lon_change

        # Keep within reasonable bounds
        self.current_lat = max(8.47, min(8.50, self.current_lat))
        self.current_lon = max(-13.25, min(-13.21, self.current_lon))

        # Generate realistic speed (0-80 km/h)
        speed = random.uniform(0, 80)

        # Generate heading (0-360 degrees)
        heading = random.uniform(0, 360)

        # Generate accuracy (3-20 meters)
        accuracy = random.uniform(3, 20)

        return {
            "latitude": round(self.current_lat, 6),
            "longitude": round(self.current_lon, 6),
            "speed": round(speed, 1),
            "heading": round(heading, 1),
            "accuracy": round(accuracy, 1),
            "timestamp": datetime.now().isoformat()
        }

    def send_data(self, gps_data):
        """Send GPS data to server"""
        try:
            url = f"{self.server_url}/gps/api/bus/{self.bus_id}/update-location/"
            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, json=gps_data, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Bus {self.bus_id}: {gps_data['latitude']:.6f}, {gps_data['longitude']:.6f} @ {gps_data['speed']} km/h")
                return True
            else:
                print(f"❌ Server error {response.status_code}: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
        except Exception as e:
            print(f"❌ Send error: {e}")
            return False

    def simulate_route(self, duration_minutes=60, update_interval=10):
        """Simulate a bus route for specified duration"""
        print(f"🚀 Starting GPS simulation for Bus {self.bus_id}")
        print(f"Duration: {duration_minutes} minutes")
        print(f"Update interval: {update_interval} seconds")
        print(f"Server: {self.server_url}")
        print("-" * 50)

        end_time = time.time() + (duration_minutes * 60)
        update_count = 0

        try:
            while time.time() < end_time:
                gps_data = self.generate_gps_data()
                if self.send_data(gps_data):
                    update_count += 1

                time.sleep(update_interval)

        except KeyboardInterrupt:
            print("\n⏹️  Simulation stopped by user")

        print("-" * 50)
        print(f"📊 Simulation complete!")
        print(f"Total updates sent: {update_count}")
        print(f"Duration: {duration_minutes} minutes")

def main():
    if len(sys.argv) < 3:
        print("Usage: python gps_simulator.py <bus_id> <server_url> [duration_minutes] [update_interval]")
        print("Example: python gps_simulator.py 1 http://127.0.0.1:8000 30 10")
        sys.exit(1)

    bus_id = sys.argv[1]
    server_url = sys.argv[2]
    duration_minutes = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    update_interval = int(sys.argv[4]) if len(sys.argv) > 4 else 10

    simulator = GPSSimulator(bus_id, server_url)
    simulator.simulate_route(duration_minutes, update_interval)

if __name__ == "__main__":
    main()</content>
<parameter name="filePath">c:\Users\pateh\Videos\Dissertation\wakafine\wakafine\gps_simulator.py