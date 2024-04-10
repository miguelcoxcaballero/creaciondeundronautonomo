import os
import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('QR Gen 2 Generator by AlexBe')
        self.root.geometry('800x600')
        
        # Constantes
        self.DEFAULT_QR_SIZE = 10
        self.DEFAULT_QRS_PER_ROW = 3
        
        # Atributos
        self.qr_size = self.DEFAULT_QR_SIZE
        self.text_var = tk.StringVar(value="default")
        self.text_var.trace_add("write", self.generate_qr)
        self.qr_entries = {}
        self.num_additional_qrs = 0
        self.text_entry_visible = False
        self.current_qr_index = None
        self.text_entry = None
        self.qr_labels = {}
        self.qrs_per_row = self.DEFAULT_QRS_PER_ROW
        self.width_entry_value = tk.StringVar(value="10")

        self.setup_ui()

    def setup_ui(self):
        self.create_menu()
        self.create_button_frame()
        self.create_qr_frame()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export as PDF file", command=self.save_as_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def create_button_frame(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.TOP, pady=10)

        ttk.Button(button_frame, text='Zoom in (+)', command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Zoom out (-)', command=self.zoom_out).pack(side=tk.LEFT, padx=5)

        qr_config_frame = ttk.Frame(button_frame)
        qr_config_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(qr_config_frame, text="QR por row:").pack(side=tk.LEFT)
        self.qr_per_row_entry = ttk.Entry(qr_config_frame)
        self.qr_per_row_entry.insert(0, str(self.qrs_per_row))
        self.qr_per_row_entry.pack(side=tk.LEFT)
        ttk.Button(qr_config_frame, text="Update", command=self.update_qr_per_row).pack(side=tk.LEFT)

        ttk.Button(button_frame, text="New QR", command=self.generate_additional_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete every QR", command=self.delete_all_qrs).pack(side=tk.LEFT, padx=5)

        width_entry_frame = ttk.Frame(button_frame)
        width_entry_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(width_entry_frame, text="Width (cm)").pack(side=tk.LEFT)
        self.width_entry = ttk.Entry(width_entry_frame, textvariable=self.width_entry_value)
        self.width_entry.pack(side=tk.LEFT)

    def create_qr_frame(self):
        self.qr_frame = ttk.Frame(self.root)
        self.qr_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.generate_qr()

    def update_qr_per_row(self):
        try:
            new_qr_per_row = int(self.qr_per_row_entry.get())
            if new_qr_per_row > 0:
                self.qrs_per_row = new_qr_per_row
                self.generate_qr()
            else:
                messagebox.showerror("Error", "La cantidad de QR por fila debe ser mayor a 0.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido para la cantidad de QR por fila.")

    def generate_qr(self, *args):
        for index, text_var in self.qr_entries.items():
            data = text_var.get()

            if data:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=self.qr_size,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                img = ImageTk.PhotoImage(img)
                if index not in self.qr_labels:
                    qr_label = ttk.Label(self.qr_frame, image=img, relief="solid")
                    qr_label.image = img
                    qr_label.bind("<Button-1>", lambda event, qr_index=index: self.toggle_text_entry(qr_index, event.x_root, event.y_root))
                    qr_label.grid(row=(index - 1) // self.qrs_per_row, column=(index - 1) % self.qrs_per_row, padx=10, pady=10, sticky="nsew")
                    self.qr_labels[index] = qr_label
                else:
                    row = (index - 1) // self.qrs_per_row
                    column = (index - 1) % self.qrs_per_row
                    self.qr_labels[index].config(image=img)
                    self.qr_labels[index].image = img
                    self.qr_labels[index].grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

                    # Actualizar posición del cuadro de texto si está visible
                    if self.text_entry_visible and index == self.current_qr_index:
                        self.update_text_entry_position(index)

    def zoom_in(self):
        self.qr_size += 1
        self.generate_qr()

    def zoom_out(self):
        if self.qr_size > 1:
            self.qr_size -= 1
            self.generate_qr()

    def toggle_text_entry(self, qr_index, x, y):
        if self.current_qr_index is None or qr_index != self.current_qr_index:
            if self.text_entry_visible:
                self.qr_entries[self.current_qr_index].set(self.text_var.get())
                self.text_entry.destroy()
                self.text_entry_visible = False
                self.current_qr_index = None

            self.text_var.set(self.qr_entries[qr_index].get())
            self.text_entry = ttk.Entry(self.qr_frame, textvariable=self.text_var, justify='center')
            self.update_text_entry_position(qr_index)
            self.text_entry.focus_set()
            self.text_entry_visible = True
            self.current_qr_index = qr_index
        else:
            self.qr_entries[self.current_qr_index].set(self.text_var.get())
            self.text_entry.destroy()
            self.text_entry_visible = False
            self.current_qr_index = None

    def update_text_entry_position(self, qr_index):
        qr_label = self.qr_labels[qr_index]
        qr_width, qr_height = qr_label.winfo_width(), qr_label.winfo_height()
        qr_center_x = qr_label.winfo_rootx() + qr_width / 2 - self.qr_frame.winfo_rootx()
        qr_center_y = qr_label.winfo_rooty() + qr_height / 2 - self.qr_frame.winfo_rooty()
        entry_width, entry_height = 150, 25
        entry_x = qr_center_x - entry_width / 2
        entry_y = qr_center_y - entry_height / 2
        self.text_entry.place(x=entry_x, y=entry_y, width=entry_width, height=entry_height)

    def delete_all_qrs(self):
        for qr_label in self.qr_labels.values():
            qr_label.destroy()
        self.qr_labels = {}
        self.qr_entries = {}
        self.num_additional_qrs = 0
        self.generate_qr()

    def generate_additional_qr(self):
        self.num_additional_qrs += 1
        index = len(self.qr_entries) + 1
        text_var = tk.StringVar(value="vacio")
        text_var.trace_add("write", self.generate_qr)
        self.qr_entries[index] = text_var
        self.generate_qr()

    def save_as_pdf(self):
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_filename:
            c = canvas.Canvas(pdf_filename, pagesize=A4)

            for index, text_var in self.qr_entries.items():
                data = text_var.get()

                if data:
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=self.qr_size,
                        border=4,
                    )
                    qr.add_data(data)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")

                    img_filename = f"temp_qr_{index}.png"
                    img.save(img_filename)

                    # Centrar QR en la hoja y ajustar el tamaño en puntos
                    qr_width, qr_height = img.size
                    pdf_width, pdf_height = A4

                    # Convertir dimensiones de centímetros a puntos
                    width_in_cm = float(self.width_entry_value.get())
                    width_in_points = width_in_cm * 28.35  # 1 cm = 28.35 puntos
                    height_in_points = width_in_points * (qr_height / qr_width)

                    x_offset = (pdf_width - width_in_points) / 2
                    y_offset = (pdf_height - height_in_points) / 2

                    c.drawInlineImage(img_filename, x_offset, y_offset, width=width_in_points, height=height_in_points)
                    os.remove(img_filename)

                    c.showPage()

            c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
