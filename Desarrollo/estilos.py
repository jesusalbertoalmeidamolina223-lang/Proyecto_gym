# J.C. TRAINING GROUP - Diseño de Interfaz y Diccionario de Datos
# Aqui definimos como se ve la app y qur datos vamos a pedir.
# Si mañana quiero agregar un campo nuevo (ej. Correo), solo lo sumariamos a la lista.

from configuracion import *

class EstilosInterfaz(Configuracion):
    def __init__(self, root):
        super().__init__()
        self.root = root
        
# Usamos el tema 'darkly' de ttkbootstrap como base
        self.style = ttk.Style(theme="darkly")

        # Diccionario de Campos (Formulario)
        # Estos son los datos que apareceran en el orden del formulario
        self.campos = [
            "Nombre", "Apellido", "Edad", "Fecha de Ingreso", 
            "Peso (kg)", "Altura (cm)", "Cintura (cm)", 
            "Brazo (cm)", "Pecho (cm)", "Gluteos (cm)", 
            "Pierna (cm)", "Enfermedades", "Discapacidad", 
            "Ultimo Pago (DD/MM/AAAA)"
        ]

        # Variables de control para la UI
        self.entries = {}
        self.ruta_foto_temporal = ""
        self.search_var = tk.StringVar()

    def configurar_estilos(self):
        """Ajustes personalizados sobre el tema oscuro para darle identidad al gym."""
        
        # Fondos generales
        self.style.configure('TFrame', background=self.color_bg)
        self.style.configure('Header.TFrame', background="black")
        self.style.configure('Card.TFrame', background=self.color_panel)

        # Estilos de Texto / Etiquetas
        self.style.configure('Title.TLabel', 
                             background="black", 
                             foreground=self.color_accent, 
                             font=("Segoe UI", 28, "bold"))
        
        self.style.configure('Search.TLabel', 
                             background=self.color_bg, 
                             foreground=self.color_accent, 
                             font=("Segoe UI", 10, "bold"))