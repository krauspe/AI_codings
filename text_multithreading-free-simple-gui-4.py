import FreeSimpleGUI as sg
import time
import threading
import subprocess

# Function to update the clock
def update_clock(window):
    """Update the clock label with the current time."""
    while True:
        current_time = time.strftime("%H:%M:%S")
        window.write_event_value('-UPDATE_CLOCK-', current_time)
        time.sleep(1)

# Function to execute a command
def execute_command(command, window):
    """Execute a PowerShell command and display the output incrementally."""
    try:
        process = subprocess.Popen(
            ["powershell", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            window.write_event_value('-COMMAND_OUTPUT-', line)
        for line in process.stderr:
            window.write_event_value('-COMMAND_OUTPUT-', line)
    except Exception as e:
        window.write_event_value('-COMMAND_OUTPUT-', f"Error: {str(e)}")

def execute_command_thread(command, window):
    """Run the execute_command function in a separate thread.""" 
    threading.Thread(target=execute_command, args=(command, window), daemon=True).start()

# Define the layout
layout = [
    [sg.Text('', size=(20, 1), font=("Helvetica", 48), key='-CLOCK-')],
    [sg.InputText('', size=(60, 1), font=("Courier", 12), key='-COMMAND_INPUT-'), sg.Button('Run', font=("Helvetica", 16))],
    [sg.Multiline('', size=(80, 20), font=("Courier", 12), key='-OUTPUT-', disabled=True, autoscroll=True, expand_x=True, expand_y=True)],
    [sg.Button('Exit', font=("Helvetica", 16))]
]

# Create the window
window = sg.Window("Clock and Command Executor", layout, resizable=True, finalize=True)

# Start the clock update in a separate thread
threading.Thread(target=update_clock, args=(window,), daemon=True).start()

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Run':
        command = values['-COMMAND_INPUT-']
        if command:
            execute_command_thread(command, window)  # Run command in a separate thread
    elif event == '-UPDATE_CLOCK-':
        window['-CLOCK-'].update(values['-UPDATE_CLOCK-'])
    elif event == '-COMMAND_OUTPUT-':
        window['-OUTPUT-'].update(values['-COMMAND_OUTPUT-'], append=True)

# Close the window
window.close()