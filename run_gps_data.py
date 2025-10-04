#!/usr/bin/env python
import subprocess
import sys

try:
    # Run the GPS data creation script
    result = subprocess.run([sys.executable, 'simple_gps_data.py'], 
                          capture_output=True, text=True, cwd='.')
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print("Return code:", result.returncode)
except Exception as e:
    print(f"Error running script: {e}")