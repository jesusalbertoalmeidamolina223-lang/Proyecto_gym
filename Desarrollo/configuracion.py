# J.C. TRAINING GROUP - Sistema de Gestion de Atletas 
# Modulo de Configuración Base
# Configura las rutas y el estilo visual.
# Se encarga de preparar el entorno para que el sistema funcione sin problemas desde el primer el principio.
import os
import sys
import json

class Configuracion:
    def __init__(self):
        # manejo de rutas físicas para compatibilidad con PyInstaller y ejecucion
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Definición de rutas físicas en el Almacenamiento Fisico (Disco)
        self.db_file = os.path.join(self.base_dir, "clientes_gym.json")
        self.img_dir = os.path.join(self.base_dir, "cedulas")
        self.historial_dir = os.path.join(self.base_dir, "historiales")
        
        # inicia el entorno asegurando que las carpetas y archivos necesarios existan para evitar errores de ejecucion
        self._preparar_entorno()

        # Paleta de colores globales de la identidad visual
        self.color_bg = "#0B0E14"     
        self.color_accent = "#00F5FF" 
        self.color_panel = "#161B22"  
        self.color_text = "#FFFFFF"   

    def _preparar_entorno(self):
        """Prepara el entorno asegurando que las carpetas y archivos necesarios existan."""
        for folder in [self.img_dir, self.historial_dir]:
            if not os.path.exists(folder): 
                os.makedirs(folder)
            
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w", encoding="utf-8") as f: 
                json.dump({}, f)