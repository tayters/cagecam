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
output_file = os.path.join(output_dir, f"video_{timestamp}.mp4")

try:
    GPIO.output(GPIO_PIN, GPIO.HIGH)

    # Pipe libcamera-vid output to ffmpeg to create MP4
    cmd = (
        f"libcamera-vid --nopreview -o - -t 180000 --width 1920 --height 1080 --saturation 0 "
        f"| ffmpeg -y -i - -vcodec libx264 -preset veryfast -crf 20 {output_file}"
    )
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

finally:
    GPIO.output(GPIO_PIN, GPIO.LOW)
    GPIO.cleanup()
