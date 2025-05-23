#!/usr/bin/env python3

import subprocess
from datetime import datetime
import os
import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_PIN = 17
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Ensure the output directory exists
output_dir = "/home/pi/videos"
os.makedirs(output_dir, exist_ok=True)

# Generate timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(output_dir, f"video_{timestamp}.h264")

try:
    # Pull GPIO17 high
    GPIO.output(GPIO_PIN, GPIO.HIGH)

    # Run libcamera-vid for 3 minutes (180000 ms)
    subprocess.run([
        "libcamera-vid",
        "--nopreview",
        "-o", output_file,
        "-t", "180000",
        "--width", "1920",
        "--height", "1080",
        "--saturation", "0",
        "--log-level", "error"
    ])

finally:
    # Pull GPIO17 low and cleanup
    GPIO.output(GPIO_PIN, GPIO.LOW)
    GPIO.cleanup()
