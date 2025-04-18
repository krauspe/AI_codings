import tkinter as tk
from tkinter import simpledialog
import time
import threading
import subprocess

def update_clock():
    """Update the clock label with the current time."""
    while True:
        current_time = time.strftime("%H:%M:%S")
        clock_label.config(text=current_time)
        time.sleep(1)


def execute_command():
    """Prompt the user for a command and execute it in PowerShell."""
    command = simpledialog.askstring("Command Input", "Enter a PowerShell command:")
    if command:
        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
            output = result.stdout if result.returncode == 0 else result.stderr
            tk.messagebox.showinfo("Command Output", output)
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))


# Create the main application window
root = tk.Tk()
root.title("Clock and Command Executor")

# Create and pack the clock label
clock_label = tk.Label(root, font=("Helvetica", 48))
clock_label.pack(pady=20)

# Create and pack the command button
command_button = tk.Button(root, text="Command", font=("Helvetica", 16), command=execute_command)
command_button.pack(pady=20)

# Start the clock update in a separate thread
clock_thread = threading.Thread(target=update_clock, daemon=True)
clock_thread.start()

# Run the Tkinter event loop
root.mainloop()