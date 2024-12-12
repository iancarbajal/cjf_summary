import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox
import subprocess
import os


def process_file(file_path):
    try:
        # Ejecutar el script summary.py con el archivo seleccionado
        output_file = f"{file_path.split("/")[-1]}_output.txt"
        command = f'python summary.py "{file_path}"'
        subprocess.run(command, shell=True, check=True)

        # Leer el resultado del archivo de salida
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                result_textbox.delete("1.0", "end")
                result_textbox.insert("1.0", f.read())
            messagebox.showinfo("Éxito", "El archivo se procesó correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró el archivo de salida.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar el archivo: {str(e)}")


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if file_path:
        file_entry.delete(0, "end")
        file_entry.insert(0, file_path)


def drop_file(event):
    file_path = event.data.strip()
    if os.path.isfile(file_path) and file_path.endswith(".pdf"):
        file_entry.delete(0, "end")
        file_entry.insert(0, file_path)
    else:
        messagebox.showerror("Error", "Por favor, arrastra un archivo PDF válido.")


def run_script():
    file_path = file_entry.get()
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Error", "Selecciona un archivo PDF válido.")
        return
    result_textbox.delete("1.0", "end")  # Limpiar resultados previos
    process_file(file_path)


# Configuración de la ventana principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana con soporte para DnD
app = TkinterDnD.Tk()
app.title("Procesador de PDFs")
app.geometry("700x600")

# Campo de entrada para el archivo
file_frame = ctk.CTkFrame(app)
file_frame.pack(pady=10, padx=10, fill="x")

file_entry = ctk.CTkEntry(file_frame, placeholder_text="Arrastra un archivo aquí o selecciónalo")
file_entry.pack(side="left", fill="x", expand=True, padx=5)

browse_button = ctk.CTkButton(file_frame, text="Seleccionar archivo", command=open_file)
browse_button.pack(side="right", padx=5)

# Botón para ejecutar el script
run_button = ctk.CTkButton(app, text="Procesar archivo", command=run_script)
run_button.pack(pady=10)

# Caja de texto para mostrar los resultados
result_textbox = ctk.CTkTextbox(app, height=20, width=80)
result_textbox.pack(pady=10, padx=10, fill="both", expand=True)

# Habilitar arrastrar y soltar archivos
app.drop_target_register(DND_FILES)
app.dnd_bind("<<Drop>>", drop_file)

app.mainloop()
