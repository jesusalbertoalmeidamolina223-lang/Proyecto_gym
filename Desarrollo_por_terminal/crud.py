# J.C. TRAINING GROUP - Gestion Pro (Terminal)
# Gestion de Datos (Lectura, Escritura y Filtro de Seguridad).

import json
from configuracion import Configuracion

class CrudBase(Configuracion):
    def __init__(self):
        super().__init__()

    def cargar_datos(self):
        """Intenta leer el JSON. Si no existe o está roto, devuelve un diccionario vacío."""
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: 
                return json.load(f) 
        except Exception:
            return {}

    def guardar_datos(self, datos):
        """Sobrescribe el JSON con la información actualizada."""
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def validar_campos_numericos(self, valores_campos):
        """Filtro de seguridad: Valida que los datos ingresados sean estrictamente numéricos."""
        a_validar = [
            "Edad", "Peso (kg)", "Altura (cm)", "Cintura (cm)", 
            "Brazo (cm)", "Pecho (cm)", "Gluteos (cm)", "Pierna (cm)"
        ]
        for campo in a_validar:
            valor = valores_campos.get(campo, "").strip()
            if valor: 
                try: 
                    float(valor.replace(',', '.'))
                except ValueError:
                    return False, campo
        return True, None