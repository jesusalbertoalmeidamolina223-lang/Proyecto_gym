# J.C. TRAINING GROUP - Sistema de Gestion de Atletas 
# Modulo de Configuración Base
# Configura las rutas y el estilo visual.
# Se encarga de preparar el entorno para que el sistema funcione sin problemas desde el primer el principio.

import os
import sys
import json
from ttkbootstrap.constants import *

class Configuracion:
    def __init__(self):
# Gestion de Rutas del Proyecto
        # En esta parte se verifica si corre como script o como .exe (para que no falle al instalarlo)
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
        """Esta parte crea las carpetas y el JSON base si es la primera vez que se ejecuta."""
        for folder in [self.img_dir, self.historial_dir]:
            if not os.path.exists(folder): 
                os.makedirs(folder)
            
        if not os.path.exists(self.db_file):
            # Se agrego un diccionario vacio para evitar errores de lectura inicial
            with open(self.db_file, "w", encoding="utf-8") as f: 
                json.dump({}, f)
            print("Base de datos inicializada correctamente.") 