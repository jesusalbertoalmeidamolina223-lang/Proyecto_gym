# J.C. TRAINING GROUP - Gestion de Datos (JSON y Validaciones)
# NOTA: Este es el motor que lee y escribe en el disco. 
# Si algo falla aqui, no se guarda el progreso del atleta.

from estilos import *

class CrudBase(EstilosInterfaz):
    def cargar_datos(self):
        """Esta parte intenta leer el JSON. Si no existe o esto roto, devuelve un dict vacio."""
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: 
                return json.load(f)
        except Exception as e:
            # Si el archivo no existe, no pasa nada,se empieza de cero
            return {}

    def guardar_datos(self, datos):
        """En esta parte se sobreescribe el JSON con la informacion actualizada."""
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def validar_campos_numericos(self):
        """
        El filtro de seguridad: Evitos que el programa falle si alguien escribe letras en campos que deben ser medidas fisicas.
        """
        # La lista de campos que solo aceptan numeros
        a_validar = [
            "Edad", "Peso (kg)", "Altura (cm)", "Cintura (cm)", 
            "Brazo (cm)", "Pecho (cm)", "Gluteos (cm)", "Pierna (cm)"
        ]
        
        for campo in a_validar:
            valor = self.entries[campo].get().strip()
            
            if valor: # Solo se valida si el usuario escribio algo
                try: 
                    # Se converte las comas a puntos para que Python lo acepte como float
                    float(valor.replace(',', '.'))
                except ValueError:
                    messagebox.showerror("Dato no válido", f"El campo '{campo}' solo acepta números.")
                    return False
        
        return True 