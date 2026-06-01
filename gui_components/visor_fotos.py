import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

class VisorMultimedia:
    @staticmethod
    def construir_visor(contenedor, app_referencia):
        """esta parte se encarga de construir el área visual para mostrar las imágenes."""
        lbl_visor = ttk.Label(contenedor, anchor="center")
        lbl_visor.pack(fill="both", expand=True, padx=15, pady=15)
        return lbl_visor

    @staticmethod
    def renderizar(lbl_visor, ruta):
        """Muestra la imagen en la pantalla principal de la iterfaz."""
        try:
            img = Image.open(ruta).resize((220, 260), Image.Resampling.LANCZOS)
            ph = ImageTk.PhotoImage(img)
            lbl_visor.config(image=ph, text="")
            lbl_visor.image = ph
        except Exception:
            VisorMultimedia.mostrar_placeholder(lbl_visor)

    @staticmethod
    def mostrar_placeholder(lbl_visor):
        lbl_visor.config(text="[ VISOR VACÍO ]", image="")