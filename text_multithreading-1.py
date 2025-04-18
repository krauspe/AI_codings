import tkinter as tk
from tkinter import simpledialog, scrolledtext
import time
import threading
import subprocess

# Add an exit button to the main window
def exit_application():
    """Exit the application."""
    root.destroy()


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
            output_text.config(state=tk.NORMAL)  # Enable editing to insert text
            output_text.insert(tk.END, output + "\n")  # Append the output
            output_text.see(tk.END)  # Scroll to the end
            output_text.config(state=tk.DISABLED)  # Disable editing
        except Exception as e:
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"Error: {str(e)}\n")
            output_text.see(tk.END)
            output_text.config(state=tk.DISABLED)

# Create the main application window
root = tk.Tk()
root.title("Clock and Command Executor")
root.geometry("600x400")  # Set an initial size
root.rowconfigure(0, weight=1)  # Allow resizing
root.columnconfigure(0, weight=1)

# Create and pack the clock label
clock_label = tk.Label(root, font=("Helvetica", 48))
clock_label.pack(pady=20)

# Create and pack the command button
command_button = tk.Button(root, text="Command", font=("Helvetica", 16), command=execute_command)
command_button.pack(pady=20)

# Create and pack the exit button
exit_button = tk.Button(root, text="Exit", font=("Helvetica", 16), command=exit_application)
exit_button.pack(pady=20)

# Create and pack the output frame with a scrolling text widget
output_frame = tk.Frame(root)
output_frame.pack(pady=20, fill=tk.BOTH, expand=True)
output_frame.rowconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Courier", 12), state=tk.DISABLED, height=10)
output_text.pack(fill=tk.BOTH, expand=True)

# Start the clock update in a separate thread
clock_thread = threading.Thread(target=update_clock, daemon=True)
clock_thread.start()

# Run the Tkinter event loop
root.mainloop()