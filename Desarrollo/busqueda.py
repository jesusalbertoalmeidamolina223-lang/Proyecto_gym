# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Gestion multimedia y motor de busqueda.
# Se usa Pillow para que las fotos se vean bien en el visor y no den problemas de formato.
# Se encarga de guardar las fotos en las carpetas locales usando el ID del cliente como referencia.
# El motor de busqueda: muestra los resultados al momento segun lo que el usuario escriba.
import os
import shutil
from crud import CrudBase

class BusquedaMedia(CrudBase):
    def __init__(self):
        super().__init__()

    def gestionar_copiado_foto(self, ruta_foto_temporal, id_cliente):
        """Gestiona el proceso de almacenamiento de la foto de cédula, asegurando que se guarde con un nombre único basado en el ID del cliente."""
        if not ruta_foto_temporal or not os.path.exists(ruta_foto_temporal): 
            return None
        ext = os.path.splitext(ruta_foto_temporal)[1]
        nuevo_nombre = f"cedula_{id_cliente}{ext}"
        ruta_destino = os.path.join(self.img_dir, nuevo_nombre)
        shutil.copy2(ruta_foto_temporal, ruta_destino)
        return nuevo_nombre

    def filtrar_atletas(self, filtro_texto):
        """Realiza una búsqueda en la base de datos de atletas, filtrando por nombre o apellido según el texto ingresado por el usuario."""
        todos_datos = self.cargar_datos()
        filtro = filtro_texto.lower().strip()
        
        if not filtro:
            return todos_datos
            
        resultado = {}
        for k, v in todos_datos.items():
            if filtro in v.get("Nombre", "").lower() or filtro in v.get("Apellido", "").lower():
                resultado[k] = v
        return resultado