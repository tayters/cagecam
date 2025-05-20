import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO17 as an output
GPIO.setup(17, GPIO.OUT)

print("GPIO17 Control")
print("Type 'on' to turn ON, 'off' to turn OFF, or 'exit' to quit.")

try:
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "on":
            GPIO.output(17, GPIO.HIGH)
            print("GPIO17 is ON")
        elif command == "off":
            GPIO.output(17, GPIO.LOW)
            print("GPIO17 is OFF")
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Please type 'on', 'off', or 'exit'.")
finally:
    GPIO.cleanup()
    print("GPIO cleanup done.")
