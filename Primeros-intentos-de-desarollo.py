import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
from datetime import datetime
import os
import shutil
import sys

class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("J.C. TRAINING GROUP - Gestión Pro")
        self.root.geometry("1100x900")
        
        # --- PALETA DE COLORES ---
        self.color_bg = "#0B0E14"      # Negro de fondo
        self.color_accent = "#00F5FF"  # Turquesa
        self.color_panel = "#161B22"   # Gris oscuro paneles

        # Configuración del estilo
        self.style = ttk.Style(theme="darkly")
        
        # Corrección de estilos para evitar el TclError
        self.style.configure('TFrame', background=self.color_bg)
        self.style.configure('Header.TFrame', background="black") # Para el encabezado
        self.style.configure('Card.TFrame', background=self.color_panel) # Para los paneles internos
        
        self.style.configure('Title.TLabel', 
                             background="black", 
                             foreground=self.color_accent, 
                             font=("Segoe UI", 26, "bold"))
        
        self.style.configure('Accent.TButton', 
                             background=self.color_accent, 
                             foreground="black", 
                             font=("Segoe UI", 10, "bold"))

        # Rutas
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(self.base_path, "clientes_gym.json")
        self.img_dir = os.path.join(self.base_path, "cedulas")
        if not os.path.exists(self.img_dir): os.makedirs(self.img_dir)

        self.campos = [
            "Nombre", "Apellido", "Edad", "Fecha de Ingreso", "Peso (kg)", 
            "Altura (cm)", "Cintura (cm)", "Brazo (cm)", "Pecho (cm)", 
            "Gluteos (cm)", "Pierna (cm)", "Enfermedades", 
            "Discapacidad", "Ultimo Pago (DD/MM/AAAA)"
        ]
        self.entries = {}
        self.foto_path_temp = "" 
        
        self.setup_ui()
        self.actualizar_tabla()

    def setup_ui(self):
        # 1. Header (Usando el estilo configurado)
        header = ttk.Frame(self.root, style='Header.TFrame', height=100)
        header.pack(fill="x")
        ttk.Label(header, text="J.C. TRAINING GROUP", style='Title.TLabel').pack(pady=25)

        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # 2. Panel de Datos (Usando estilo Card)
        form_panel = ttk.Frame(main_frame, style='Card.TFrame', padding=20)
        form_panel.pack(fill="x", pady=10)

        for i, campo in enumerate(self.campos):
            row, col = i // 2, (i % 2) * 2
            ttk.Label(form_panel, text=f"{campo}:", background=self.color_panel).grid(row=row, column=col, padx=10, pady=8, sticky="e")
            entry = ttk.Entry(form_panel, width=35)
            entry.grid(row=row, column=col+1, padx=10, pady=8)
            self.entries[campo] = entry

        # 3. Botones de Acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        acciones = [("REGISTRAR", self.registrar), ("ACTUALIZAR", self.actualizar), 
                    ("BORRAR", self.borrar), ("LIMPIAR", self.limpiar_campos)]
        
        for texto, cmd in acciones:
            ttk.Button(btn_frame, text=texto, command=cmd, style='Accent.TButton', width=15).pack(side="left", padx=10)

        # 4. Tabla
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Apellido", "Estado"), show="headings", height=10)
        for col in ("ID", "Nombre", "Apellido", "Estado"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.column("ID", width=0, stretch=tk.NO)
        self.tree.pack(fill="both", expand=True, pady=10)

    # --- Lógica básica para que no de errores ---
    def cargar_datos(self):
        if not os.path.exists(self.db_file): return {}
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}

    def registrar(self):
        id_c = f"{self.entries['Nombre'].get()}_{self.entries['Apellido'].get()}".lower().replace(" ", "")
        if not id_c or id_c == "_":
            messagebox.showwarning("Atención", "Nombre y Apellido son necesarios")
            return
        d = self.cargar_datos()
        d[id_c] = {c: self.entries[c].get() for c in self.campos}
        with open(self.db_file, "w", encoding="utf-8") as f: json.dump(d, f, indent=4)
        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Cliente guardado")

    def actualizar_tabla(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        d = self.cargar_datos()
        for k, v in d.items():
            self.tree.insert("", "end", values=(k, v.get("Nombre",""), v.get("Apellido",""), "ACTIVO"))

    def seleccionar_foto(self): pass
    def cargar_desde_tabla(self, event): pass
    def actualizar(self): self.registrar()
    def borrar(self): pass
    def limpiar_campos(self):
        for e in self.entries.values(): e.delete(0, tk.END)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = GymApp(root)
    root.mainloop()