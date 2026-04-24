# J.C. TRAINING GROUP - Modulo de Configuración Base
# NOTA: centralizamos las rutas y el estilo visual.
# Se separo asi para no tener que buscar entre 1000 líneas cuando quiera cambiar un color o mover la base de datos.

import os
import sys
import json
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class Configuracion:
    def __init__(self):
# Gestion de Rutas del Proyecto
        # En esta parte verificamos si corre como script o como .exe (para que no falle al instalarlo)
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Archivos y carpetas principales
        self.db_file = os.path.join(self.base_dir, "clientes_gym.json")
        self.img_dir = os.path.join(self.base_dir, "cedulas")
        self.historial_dir = os.path.join(self.base_dir, "historiales")
        
        # Inicializacion del entorno (verificamos que existan las carpetas necesarias)
        self._preparar_entorno()

# Desarrollo Visual de la Paleta Dark
        # Lista de colores elegidos para un look moderno y profesional
        self.color_bg = "#0B0E14"     # Fondo profundo
        self.color_accent = "#00F5FF" # Cian para resaltar botones/titulos
        self.color_panel = "#161B22"  # Contenedores secundarios
        self.color_text = "#FFFFFF"   # Texto base

    def _preparar_entorno(self):
        """Esta aprte crea las carpetas y el JSON base si es la primera vez que se ejecuta."""
        for folder in [self.img_dir, self.historial_dir]:
            if not os.path.exists(folder): 
                os.makedirs(folder)
            
        if not os.path.exists(self.db_file):
            # Se agrego un diccionario vacio para evitar errores de lectura inicial
            with open(self.db_file, "w", encoding="utf-8") as f: 
                json.dump({}, f)
            print("Base de datos inicializada correctamente.") # Log para control interno