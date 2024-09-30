import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def download_pdf(data):
    """Function to download PDF file."""
    # Open a file dialog to save the PDF file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        title="Save PDF File"
    )

    # Check if a file path was selected
    if file_path:
        try:
            # Create a PDF
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            
            # Write data to PDF
            c.drawString(100, height - 100, "Name, Age, City")
            y = height - 120
            for row in data:
                c.drawString(100, y, f"{row[0]}, {row[1]}, {row[2]}")
                y -= 20  # Move down for the next row
            
            # Save the PDF
            c.save()
            messagebox.showinfo("Success", "PDF file downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF file: {e}")

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
    download_pdf(data)      # Call the download function

# Create the main application window
root = tk.Tk()
root.title("PDF Download Example")

# Create a button to download the PDF file
download_button = tk.Button(root, text="Download PDF", command=on_download)
download_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
