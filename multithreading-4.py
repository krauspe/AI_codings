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


def execute_command_thread(command):
    """Executes a command in a separate thread and updates the output widget."""
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
        
        def update_gui():
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, output + "\n")
            output_text.see(tk.END)
            output_text.config(state=tk.DISABLED)
        
        # Schedule the GUI update on the main thread
        root.after(0, update_gui)
        
    except Exception as e:
        def update_gui_error():
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"Error: {str(e)}\n")
            output_text.see(tk.END)
            output_text.config(state=tk.DISABLED)
            
        # Schedule the GUI update on the main thread
        root.after(0, update_gui_error)

def execute_command():
    """Prompt the user for a command and execute it in a separate thread."""
    command = simpledialog.askstring("Command Input", "Enter a PowerShell command:")
    if command:
        # Run the command in a separate thread to avoid blocking the GUI
        thread = threading.Thread(target=execute_command_thread, args=(command,), daemon=True)
        thread.start()

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

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Courier", 12), state=tk.DISABLED, height=20)
output_text.pack(fill=tk.BOTH, expand=True)

# Start the clock update in a separate thread
clock_thread = threading.Thread(target=update_clock, daemon=True)
clock_thread.start()

# Run the Tkinter event loop
root.mainloop()