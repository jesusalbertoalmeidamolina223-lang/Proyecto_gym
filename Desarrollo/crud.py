# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Gestiona los datos JSON y Validaciones.
# Es el motor de los datos se encarga de guardar y cargar todo el historial.
# Es importante ya que Si esta logica tira error, basicamente el atleta se queda sin registros en el sistema.
import json
from configuracion import Configuracion

class CrudBase(Configuracion):
    def __init__(self):
        super().__init__()

    def cargar_datos(self):
        """Intenta leer el archivo físico de clientes_gym.json."""
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: 
                return json.load(f)
        except Exception:
            return {}

    def guardar_datos(self, datos):
        """Escribe el estado actualizado de la base de datos en el archivo fisico clientes_gym.json, asegurando la persistencia de los datos del sistema."""
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)