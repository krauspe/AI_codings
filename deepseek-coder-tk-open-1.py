import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil
import glob
import time


def open_file_dialog():
    """Open file dialog and return the selected paths."""
    multiple_selections = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    if multiple_selections:
        return [f[0] for f in multiple_selections]
    else:
        return None


def open_directory_dialog():
    """Open directory dialog and return selected paths."""
    directories = filedialog.askdirectory(
        title="Select Directory",
    )

    if directories:
        return [d[0] for d in directories]
    else:
        return None


def download_file(start, end):
    """Download a file from the specified start URL to destination path."""
    try:
        # Simulate downloading (replace with actual download logic)
        print(f"Starting download: {start}")

        # Simulated download progress
        time.sleep(1)  # Real download would take longer

        # Simulated download complete
        print("Download completed!")
        print(f"File saved at: {end}")
    except Exception as e:
        print(f"Error downloading file: {str(e)}")


def handle_directory_selection(directories):
    """Handle directory selection and initiate model downloads."""
    for directory in directories:
        print(f"\nStarting to download models from directory: {directory}")

        # Example pattern to search for model files (adjust as needed)
        model_pattern = "model_*[.]*"
        model_files = glob.glob(os.path.join(directory, model_pattern))

        if not model_files:
            print(f"No model files found in directory: {directory}")
            continue

        print(f"Found {len(model_files)} model files to download:")
        for i, file in enumerate(model_files, 1):
            print(f"{i}. {file}")

            # Simulated download with progress bar (replace with actual logic)
            download_file(file, os.path.join(directory, "downloaded_models"))

    print("Download process completed.")


def main():
    root = tk.Tk()
    root.title("Model Downloader")

    button_frame = ttk.Frame(root)
    button_frame.pack(padx=10, pady=5)

    # Exit Button
    exit_button = ttk.Button(
        button_frame,
        text="Exit",
        command=root.destroy
    )
    exit_button.pack(side=tk.LEFT, padx=5, pady=2)

    # Open File Dialog Button
    open_file_button = ttk.Button(
        button_frame,
        text="Open File(s)",
        command=open_file_dialog
    )
    open_file_button.pack(side=tk.LEFT, padx=5, pady=2)

    # Open Directory Button
    open_directory_button = ttk.Button(
        button_frame,
        text="Open Directory",
        command=lambda: open_directory_dialog()
    )
    open_directory_button.pack(side=tk.LEFT, padx=5, pady=2)

    root.mainloop()


if __name__ == "__main__":
    main()