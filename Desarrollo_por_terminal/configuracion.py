# J.C. TRAINING GROUP - Gestion Pro (Terminal)
# Modulo de Configuracion Base y Rutas.

import os
import sys

class Configuracion:
    def __init__(self):
        # Organiza Rutas del Proyecto de forma dinamica 
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Archivos y carpetas principales
        self.db_file = os.path.join(self.base_dir, "clientes_gym.json")
        self.img_dir = os.path.join(self.base_dir, "cedulas")
        self.historial_dir = os.path.join(self.base_dir, "historiales")
        
        self._preparar_entorno()

    def _preparar_entorno(self):
        """Crea automaticamente las carpetas de imagenes, historiales y archivos base."""
        for folder in [self.img_dir, self.historial_dir]:
            if not os.path.exists(folder): 
                os.makedirs(folder)