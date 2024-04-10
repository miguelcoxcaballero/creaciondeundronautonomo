import os
import qrcode
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_qr_code():
    x = x_input.get()
    y = y_input.get()
    sidelength = sidelength_var.get()
    if x and y and sidelength:
        qr_text = f'{sidelength},{x},{y}'  # Updated format to "a,b,c"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,  # Set border to 0 for borderless QR code
        )
        qr.add_data(qr_text)
        qr.make(fit=True)

        global img
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = "qr_code.png"
        img.save(img_path)  # Save QR code as PNG

        # Display QR code
        display_qr_code(img_path)

def display_qr_code(img_path):
    img = Image.open(img_path)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img

def save_pdf():
    x = x_input.get()
    y = y_input.get()
    sidelength = sidelength_var.get()
    if x and y and sidelength:
        qr_text = f'{sidelength},{x},{y}'  # Updated format to "a,b,c"

        # Set default file name and initial directory
        default_file_name = qr_text + ".pdf"
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        file_path = filedialog.asksaveasfilename(
            initialfile=default_file_name,
            initialdir=downloads_folder,
            defaultextension='.pdf',
            filetypes=[('PDF Files', '*.pdf')]
        )

        if file_path:
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4  # Get A4 dimensions

            # Convert side length from cm to points (1 cm = 28.35 points)
            qr_size_points = float(sidelength) * 28.35

            # Center the QR code on the page
            x = (width - qr_size_points) / 2
            y = (height - qr_size_points) / 2
            img_path = "qr_code.png"
            c.drawImage(img_path, x, y, width=qr_size_points, height=qr_size_points)
            c.save()

# Set up GUI
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("350x550")  # Set window size

font = ('Arial', 10)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

x_label = tk.Label(input_frame, text="Enter X:", font=font)
x_label.grid(row=0, column=0, pady=5)
x_input = tk.Entry(input_frame, font=font)
x_input.grid(row=0, column=1, pady=5)

y_label = tk.Label(input_frame, text="Enter Y:", font=font)
y_label.grid(row=1, column=0, pady=5)
y_input = tk.Entry(input_frame, font=font)
y_input.grid(row=1, column=1, pady=5)

sidelength_label = tk.Label(input_frame, text="Select Side Length:", font=font)
sidelength_label.grid(row=2, column=0, pady=5)
sidelength_var = tk.StringVar(value="8")  # default value

# Radio buttons for side length selection
radiobutton_8 = tk.Radiobutton(input_frame, text="8", variable=sidelength_var, value="8", font=font)
radiobutton_8.grid(row=2, column=1)
radiobutton_18 = tk.Radiobutton(input_frame, text="18", variable=sidelength_var, value="18", font=font)
radiobutton_18.grid(row=3, column=1)

generate_button = tk.Button(input_frame, text="Generate QR Code", font=font, command=generate_qr_code)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# QR Code Display Frame
qr_frame = tk.Frame(root)
qr_frame.pack(pady=10)

qr_label = tk.Label(qr_frame)
qr_label.pack()

# Save Button
save_button = tk.Button(root, text="Save as PDF", font=font, command=save_pdf)
save_button.pack(pady=10)

root.mainloop()
