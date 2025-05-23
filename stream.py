import subprocess
import threading
import os  # Add this import
from gpiozero import DigitalOutputDevice

# Set up GPIO17 as a digital output
ir_output = DigitalOutputDevice(17, active_high=True, initial_value=False)

# Global variable to hold the stream process
stream_process = None

def start_stream():
    global stream_process
    # Start Libcamera stream piped into VLC for HTTP streaming
    stream_command = (
        "libcamera-vid --nopreview -o - -t 0 --width 1920 --height 1080 --saturation 0 --codec h264 "
        "| cvlc -q stream:///dev/stdin "
        "--sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264"
        "> /dev/null 2>&1"
    )
    try:
        # Start the stream in a new process group
        stream_process = subprocess.Popen(
            stream_command,
            shell=True,
            preexec_fn=os.setsid  # This makes the shell the leader of a new process group
        )
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
        try:
            os.killpg(os.getpgid(stream_process.pid), 15)  # 15 is SIGTERM
            print("Streaming process terminated.")
        except Exception as e:
            print(f"Error terminating stream: {e}")
