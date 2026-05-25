# J.C. TRAINING GROUP - Gestión Pro (Terminal)
# Gestión Multimedia en Disco y Motor de Búsqueda.

import os
import shutil
from crud import CrudBase

class BusquedaMedia(CrudBase):
    def __init__(self):
        super().__init__()

    def gestionar_copiado_foto(self, ruta_foto_temporal, id_cliente):
        """Maneja el guardado físico de la foto de la cédula en la carpeta local."""
        if not ruta_foto_temporal or not os.path.exists(ruta_foto_temporal): 
            return None
        ext = os.path.splitext(ruta_foto_temporal)[1]
        nuevo_nombre = f"cedula_{id_cliente}{ext}"
        try:
            shutil.copy2(ruta_foto_temporal, os.path.join(self.img_dir, nuevo_nombre))
            return nuevo_nombre
        except Exception:
            return None

    def obtener_atletas_filtrados(self, filtro=""):
        """Filtra la base de datos y encuentra coincidencias por nombre o apellido."""
        d = self.cargar_datos()
        filtro = filtro.lower().strip()
        if not filtro:
            return d
            
        resultados = {}
        for k, v in d.items():
            if filtro in v.get("Nombre", "").lower() or filtro in v.get("Apellido", "").lower():
                resultados[k] = v
        return resultados