# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Esta parte se encarga de ser el cerebro para la Logica de Negocio.
# Aqui se procesan los datos de los formularios y se valida la informacion antes de guardarla.
# El manejo de archivos que nos asegura de que las fotos se guarden bien y el historial no se dañe.
# Es el puente que Conecta la interfaz con el almacenamiento fisico (JSON/Fotos)
import os
from respaldos import HistorialRespaldos

class ControladorAcciones(HistorialRespaldos):
    def __init__(self):
        super().__init__()

    def procesar_registro(self, valores_formulario, ruta_foto_temporal):
        """crea un ID unico para el atleta, gestiona el almacenamiento de la foto y actualiza la base de datos con los nuevos datos del formulario."""
        id_c = f"{valores_formulario['Nombre'].lower()}_{valores_formulario['Apellido'].lower()}".replace(" ", "")
        db_actual = self.cargar_datos()

        # Almacenamiento multimedia interactivo
        foto_final = self.gestionar_copiado_foto(ruta_foto_temporal, id_c)
        valores_formulario["foto_cedula"] = foto_final or db_actual.get(id_c, {}).get("foto_cedula")
        
        # Doble funcion: Actualiza el historial de medidas y luego guarda el estado actualizado de la base de datos
        self.registrar_en_historial(id_c, valores_formulario)
        db_actual[id_c] = valores_formulario
        self.guardar_datos(db_actual)
        return id_c

    def procesar_borrado_completo(self, id_c):
        """Elimina completamente el registro del atleta, incluyendo su foto de cédula y su historial de medidas, asegurando que no queden rastros en el sistema."""
        db = self.cargar_datos()
        perfil = db.get(id_c, {})
        
        # Remoción de foto de cédula
        foto = perfil.get("foto_cedula")
        if foto:
            path_foto = os.path.join(self.img_dir, foto)
            if os.path.exists(path_foto): os.remove(path_foto)
            
        # Remocion del historial de medidas
        path_historial = os.path.join(self.historial_dir, f"{id_c}.json")
        if os.path.exists(path_historial): os.remove(path_historial)

        # Extracción definitiva del registro del atleta de la base de datos
        db.pop(id_c, None)
        self.guardar_datos(db)

    def verificar_campos_medidas(self, valores_formulario):
        # Valida que los campos numéricos del formulario contengan valores numéricos válidos,
        # permitiendo el uso de comas como separadores decimales,
        # y devuelve un mensaje de error específico si se encuentra un campo con formato incorrecto.
        campos_numericos = [
            "Edad", "Peso (kg)", "Altura (cm)", "Cintura (cm)", 
            "Brazo (cm)", "Pecho (cm)", "Gluteos (cm)", "Pierna (cm)"
        ]
        for campo in campos_numericos:
            valor = valores_formulario.get(campo, "").strip()
            if valor: 
                try: 
                    float(valor.replace(',', '.'))
                except ValueError:
                    return False, campo
        return True, None