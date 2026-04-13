# Fase 1: Infraestructura y Gestión de Archivos
# Esta parte es el "esqueleto". Define dónde se guardará todo y asegura que, si el programa se pasa a otra computadora o lo convierto en un .exe, no se pierde nada.
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os
import shutil
import sys
from PIL import Image, ImageTk
from datetime import datetime

class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("J.C. TRAINING GROUP - Gestión Pro")
        self.root.geometry("1300x950")

        # GESTIÓN DE RUTAS (SOPORTE .EXE)
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Rutas de carpetas y archivos
        self.db_file = os.path.join(self.base_dir, "clientes_gym.json")
        self.img_dir = os.path.join(self.base_dir, "cedulas")
        self.hist_dir = os.path.join(self.base_dir, "historiales")

        # Creación automática de estructura
        for folder in [self.img_dir, self.hist_dir]:
            if not os.path.exists(folder): os.makedirs(folder)
            
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w", encoding="utf-8") as f: json.dump({}, f)