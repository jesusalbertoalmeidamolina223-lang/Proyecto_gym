# # J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Diseno de Interfaz y Diccionario de Datos.
# Maneja la Interfaz y Estructura definiendo el estilo de la aplicacion con el esquema de los datos.
# Si llega el momento de agregar algo mas como el correo,Instagram o el whatsapp, se agrega a la lista y el sistema lo toma solo.
class EstilosInterfaz:
    def __init__(self):
        # Esquema del Diccionario de Campos de Datos para los Atletas
        self.campos = [
            "Nombre", "Apellido", "Edad", "Fecha de Ingreso", 
            "Peso (kg)", "Altura (cm)", "Cintura (cm)", 
            "Brazo (cm)", "Pecho (cm)", "Gluteos (cm)", 
            "Pierna (cm)", "Enfermedades", "Discapacidad", 
            "Ultimo Pago (DD/MM/AAAA)"
        ]