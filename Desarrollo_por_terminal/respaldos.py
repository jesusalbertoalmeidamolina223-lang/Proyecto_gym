# J.C. TRAINING GROUP - Gestion Pro (Terminal)
# Historial de Evolucion y Copias de Seguridad.

import os
import json
import shutil
from datetime import datetime
from busqueda import BusquedaMedia

class HistorialRespaldos(BusquedaMedia):
    def __init__(self):
        super().__init__()

    def obtener_registros_historial(self, id_cliente):
        """Lee el archivo JSON histórico de un cliente y retorna su contenido."""
        ruta_h = os.path.join(self.historial_dir, f"{id_cliente}.json")
        if os.path.exists(ruta_h):
            with open(ruta_h, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def actualizar_archivo_historial(self, id_c, nuevos_datos):
        """Guarda una copia del estado de medidas actual en su archivo de progreso."""
        ruta = os.path.join(self.historial_dir, f"{id_c}.json")
        historial = []
        
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f: 
                historial = json.load(f)
        
        registro = {**nuevos_datos, "Fecha_Sistema": datetime.now().strftime("%d/%m/%Y %H:%M")}
        historial.append(registro)
        
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)

    def ejecutar_copia_respaldo(self, destino):
        """Empaqueta la base de datos, fotos e historiales en un directorio seguro."""
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
        folder_backup = os.path.join(destino, f"Respaldo_Gym_{fecha}")
        
        os.makedirs(folder_backup)
        # Copiar base de datos si existe
        if os.path.exists(self.db_file):
            shutil.copy2(self.db_file, folder_backup) 
        # Copiar directorios completos
        shutil.copytree(self.img_dir, os.path.join(folder_backup, "cedulas"), dirs_exist_ok=True) 
        shutil.copytree(self.historial_dir, os.path.join(folder_backup, "historiales"), dirs_exist_ok=True) 
        return folder_backup