class ValidadorDatos:
    @staticmethod
    def validar_registro(valores_formulario):
        """con esta funcion verificamos los campos obligatorios y tipos numéricos."""
        if not valores_formulario.get("Nombre") or not valores_formulario.get("Apellido"):
            return False, "El Nombre y el Apellido son obligatorios."

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
                    return False, f"El campo '{campo}' debe ser un número válido."
        return True, ""