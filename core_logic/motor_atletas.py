import os
import json
import shutil
from datetime import datetime
from configuracion import Configuracion
from core_logic.base_datos import CrudBase
from core_logic.validador import ValidadorDatos

class ControladorAcciones:
    def __init__(self):
        self.config = Configuracion()
        self.crud = CrudBase(self.config)

    def filtrar_atletas(self, filtro_texto):
        """esta fuencion nos ayuda a encontrar atletas sin importar que su nombre o apellidoesten en mayúsculas."""
        todos_datos = self.crud.cargar_datos()
        filtro = filtro_texto.lower().strip()
        
        if not filtro:
            return todos_datos
            
        resultado = {}
        for k, v in todos_datos.items():
            if filtro in v.get("Nombre", "").lower() or filtro in v.get("Apellido", "").lower():
                resultado[k] = v
        return resultado

    def procesar_registro(self, valores_formulario, ruta_foto_temporal, lista_campos):
        """en este paso generamos una ID para cada cliente con sus datos."""
        # Lamamos al validadaor desaclopado para verificar los datos 
        es_valido, msg_error = ValidadorDatos.validar_registro(valores_formulario)
        if not es_valido:
            return False, msg_error

        # Generar ID para cada atleta
        id_c = f"{valores_formulario['Nombre'].lower()}_{valores_formulario['Apellido'].lower()}".replace(" ", "")
        db_actual = self.crud.cargar_datos()

        # Limpieza y deja en balco los espacios 
        perfil_limpio = {c: valores_formulario.get(c, "").strip() for c in lista_campos}

        # esta parte la colocamos para que se encargue de gaurdar las fotos y asignarles un nombre 
        if ruta_foto_temporal and os.path.exists(ruta_foto_temporal):
            ext = os.path.splitext(ruta_foto_temporal)[1]
            nombre_foto = f"cedula_{id_c}{ext}"
            ruta_destino = os.path.join(self.config.img_dir, nombre_foto)
            shutil.copy2(ruta_foto_temporal, ruta_destino)
            perfil_limpio["foto_cedula"] = nombre_foto
        else:
            perfil_limpio["foto_cedula"] = db_actual.get(id_c, {}).get("foto_cedula", "")

        # registra el historial y agrega los cambios para cada atleta
        ruta_h = os.path.join(self.config.historial_dir, f"{id_c}.json")
        historial = []
        if os.path.exists(ruta_h):
            try:
                with open(ruta_h, "r", encoding="utf-8") as f:
                    historial = json.load(f)
            except Exception:
                pass

        registro_tiempo = {**perfil_limpio, "Fecha_Sistema": datetime.now().strftime("%d/%m/%Y %H:%M")}
        historial.append(registro_tiempo)
        
        with open(ruta_h, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)

        # Actualiza la base de datos principal
        db_actual[id_c] = perfil_limpio
        self.crud.guardar_datos(db_actual)
        return True, id_c

    def obtener_historial_atleta(self, id_cliente):
        ruta = os.path.join(self.config.historial_dir, f"{id_cliente}.json")
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def ejecutar_borrado(self, id_c):
        db = self.crud.cargar_datos()
        if id_c in db:
            perfil = db[id_c]
            foto = perfil.get("foto_cedula")
            if foto:
                path_f = os.path.join(self.config.img_dir, foto)
                if os.path.exists(path_f): os.remove(path_f)
                
            path_h = os.path.join(self.config.historial_dir, f"{id_c}.json")
            if os.path.exists(path_h): os.remove(path_h)

            db.pop(id_c)
            self.crud.guardar_datos(db)
            return True
        return False

    def empaquetar_respaldo_sistema(self, directorio_destino):
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
        folder_backup = os.path.join(directorio_destino, f"Respaldo_Gym_{fecha}")
        
        shutil.copytree(self.config.base_dir, folder_backup, ignore=shutil.ignore_patterns('__pycache__', '*.py', '*.json', 'core_logic', 'gui_components'))
        
        if os.path.exists(self.config.db_file):
            shutil.copy2(self.config.db_file, os.path.join(folder_backup, "clientes_gym.json"))
            
        ruta_zip = shutil.make_archive(folder_backup, 'zip', folder_backup)
        shutil.rmtree(folder_backup)
        return ruta_zip