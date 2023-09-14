import tkinter as tk
import subprocess

# Function to start the Python script
def start_script():
    global script_process
    script_process = subprocess.Popen(["python", "main.py"])

# Function to stop the Python script
def stop_script():
    global script_process
    if script_process:
        script_process.terminate()
        script_process = None

# Create the main window
window = tk.Tk()
window.title("Python Script Controller")

# Create "Start" button
start_button = tk.Button(window, text="Start Script", command=start_script)
start_button.pack()

# Create "Stop" button
stop_button = tk.Button(window, text="Stop Script", command=stop_script)
stop_button.pack()

# Initialize script_process as None
script_process = None

# Run the GUI
window.mainloop()
