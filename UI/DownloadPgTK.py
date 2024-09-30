import tkinter as tk
from tkinter import messagebox, filedialog
import csv

def download_csv(data):
    """Function to download CSV file."""
    # Open a file dialog to save the CSV file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save CSV File"
    )

    # Check if a file path was selected
    if file_path:
        try:
            # Writing to CSV
            with open(file_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(['Name', 'Age', 'City'])
                # Write data
                for row in data:
                    writer.writerow(row)
            messagebox.showinfo("Success", "CSV file downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {e}")

def generate_data():
    """Generate some sample data to download."""
    return [
        ['Alice', 30, 'New York'],
        ['Bob', 25, 'Los Angeles'],
        ['Charlie', 35, 'Chicago']
    ]

def on_download():
    """Handle download button click."""
    data = generate_data()  # Generate sample data
    download_csv(data)      # Call the download function

# Create the main application window
root = tk.Tk()
root.title("CSV Download Example")

# Create a button to download the CSV file
download_button = tk.Button(root, text="Download CSV", command=on_download)
download_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
