import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def open_file():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("Image Files", "*.png"), ("PDF Files", "*.pdf"), ("Word Documents", "*.docx"))
    )
    
    if file_path:
        if file_path.endswith('.png'):
            open_image(file_path)
        elif file_path.endswith('.pdf'):
            open_pdf(file_path)
        elif file_path.endswith('.docx'):
            open_docx(file_path)
        else:
            messagebox.showerror("Error", "Unsupported file format!")

def open_image(file_path):
    img = Image.open(file_path)
    img.show()  # Opens the image in the default image viewer

def open_pdf(file_path):
    os.startfile(file_path)  # This will open the PDF in the default viewer

def open_docx(file_path):
    os.startfile(file_path)  # This will open the Word document in the default viewer

# Create the main application window
root = tk.Tk()
root.title("File Opener")

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=20)

root.mainloop()