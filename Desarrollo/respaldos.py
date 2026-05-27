# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Se encarga de ver el historial de evolucion y copias de seguridad.
# en esta parte se gestionan las graficas y la evolucion de medidas de los atletas.
# Metimos una funcion de respaldo manual para que si el usuario cambia de PC, se pueda llevar toda la base de datos sin problemas.
import os
import json
import shutil
from datetime import datetime
from busqueda import BusquedaMedia

class HistorialRespaldos(BusquedaMedia):
    def __init__(self):
        super().__init__()

    def obtener_historial_atleta(self, id_cliente):
        """Busca el archivo de progreso del atleta en la carpeta fisica /historiales/."""
        ruta = os.path.join(self.historial_dir, f"{id_cliente}.json")
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def registrar_en_historial(self, id_c, nuevos_datos):
        """Agrega un bloque secuencial de medidas físicas a la linea de tiempo del atleta."""
        ruta = os.path.join(self.historial_dir, f"{id_c}.json")
        historial = self.obtener_historial_atleta(id_c)
        
        # Inyeccion de estampa de tiempo
        registro = {**nuevos_datos, "Fecha_Sistema": datetime.now().strftime("%d/%m/%Y %H:%M")}
        historial.append(registro)
        
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)

    def empaquetar_respaldo_sistema(self, directorio_destino):
        """ crea un duplicado íntegro de la BD, historiales y multimedia en un destino externo."""
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
        folder_backup = os.path.join(directorio_destino, f"Respaldo_Gym_{fecha}")
        
        os.makedirs(folder_backup)
        shutil.copy2(self.db_file, folder_backup) 
        shutil.copytree(self.img_dir, os.path.join(folder_backup, "cedulas")) 
        shutil.copytree(self.historial_dir, os.path.join(folder_backup, "historiales")) 
        return folder_backup