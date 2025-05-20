import subprocess
import threading
from gpiozero import DigitalOutputDevice

# Set up GPIO17 as a digital output
ir_output = DigitalOutputDevice(17, active_high=True, initial_value=False)

# Global variable to hold the stream process
stream_process = None

def start_stream():
    global stream_process
    # Start Libcamera stream piped into VLC for HTTP streaming
    stream_command = (
        "libcamera-vid -o - -t 0 --width 1920 --height 1080 --codec h264 "
        "| cvlc -q stream:///dev/stdin "
        "--sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264"
    )
    try:
        # Start the stream in a shell so the pipe works
        stream_process = subprocess.Popen(stream_command, shell=True)
    except Exception as e:
        print(f"Failed to start stream: {e}")

# Start the stream in a background thread
stream_thread = threading.Thread(target=start_stream, daemon=True)
stream_thread.start()

print("Streaming started at http://<raspberrypi_ip>:8080")
print("Type 'on' to turn IR ON, 'off' to turn it OFF, or 'exit' to quit.")

try:
    while True:
        command = input("IR control > ").strip().lower()
        if command == "on":
            ir_output.on()
            print("IR LED ON")
        elif command == "off":
            ir_output.off()
            print("IR LED OFF")
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command. Use 'on', 'off', or 'exit'.")
finally:
    ir_output.off()
    print("IR LED turned off.")
    if stream_process:
        stream_process.terminate()
        print("Streaming process terminated.")
