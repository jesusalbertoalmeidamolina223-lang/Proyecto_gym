import tkinter as tk
import ttkbootstrap as ttk

class FormularioAtleta:
    @staticmethod
    def construir_formulario(contenedor, campos, diccionario_entries):
        """le damos forma al formulario para colocar sus datos."""
        for i, campo in enumerate(campos):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(contenedor, text=f"{campo}:", font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="e", padx=10, pady=8)
            ent = ttk.Entry(contenedor, width=25)
            ent.grid(row=row, column=col+1, sticky="w", padx=10, pady=8)
            diccionario_entries[campo] = ent