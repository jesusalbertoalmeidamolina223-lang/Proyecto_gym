# J.C. TRAINING GROUP - Gestión Pro (Terminal)
# Cerebro Operativo y Puente de Datos Intermedio.

import os
from respaldos import HistorialRespaldos

class ControladorAcciones:
    def __init__(self):
        self.motor = HistorialRespaldos()
        
    def procesar_registro(self, info_valores, ruta_foto_temporal):
        """Valida campos numéricos y obligatorios antes de efectuar el guardado."""
        es_valido, campo_error = self.motor.validar_campos_numericos(info_valores)
        if not es_valido:
            return {"status": "error_num", "campo": campo_error}
            
        if not info_valores.get('Nombre') or not info_valores.get('Apellido'):
            return {"status": "error_obligatorios"}
            
        # Generar ID Único
        id_c = f"{info_valores['Nombre'].lower()}_{info_valores['Apellido'].lower()}".replace(" ", "")
        db_actual = self.motor.cargar_datos()
        
        # Procesar foto de cédula
        foto_gestionada = self.motor.gestionar_copiado_foto(ruta_foto_temporal, id_c)
        info_valores["foto_cedula"] = foto_gestionada or db_actual.get(id_c, {}).get("foto_cedula")
        
        # Guardar en historial y base de datos
        self.motor.actualizar_archivo_historial(id_c, info_valores)
        db_actual[id_c] = info_valores
        self.motor.guardar_datos(db_actual)
        
        return {"status": "exito", "id": id_c}

    def obtener_lista_atletas(self, filtro=""):
        return self.motor.obtener_atletas_filtrados(filtro)

    def obtener_perfil_atleta(self, id_cliente):
        db = self.motor.cargar_datos()
        return db.get(id_cliente, None)

    def obtener_historial_atleta(self, id_cliente):
        return self.motor.obtener_registros_historial(id_cliente)

    def procesar_borrado(self, id_c):
        """Elimina físicamente los archivos multimedia, historiales y registro lógico."""
        db = self.motor.cargar_datos()
        if id_c not in db:
            return False
            
        foto_archivo = db.get(id_c, {}).get("foto_cedula")
        if foto_archivo:
            path_foto = os.path.join(self.motor.img_dir, foto_archivo)
            if os.path.exists(path_foto): 
                os.remove(path_foto)
                
        path_historial = os.path.join(self.motor.historial_dir, f"{id_c}.json")
        if os.path.exists(path_historial): 
            os.remove(path_historial)

        db.pop(id_c, None)
        self.motor.guardar_datos(db)
        return True

    def ejecutar_respaldo(self, destino):
        return self.motor.ejecutar_copia_respaldo(destino)