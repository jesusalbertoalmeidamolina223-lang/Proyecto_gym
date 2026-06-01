import json

class CrudBase:
    def __init__(self, config_entorno):
        self.config = config_entorno

    def cargar_datos(self):
        """lee el archivo fisico de clientes_gym.json."""
        try:
            with open(self.config.db_file, "r", encoding="utf-8") as f: 
                return json.load(f)
        except Exception:
            return {}

    def guardar_datos(self, datos):
        """actualiza la base de datos de cada atleta."""
        with open(self.config.db_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)