# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# El panel de Control (Interfaz de Botones)
# Aqui centralizamos todos los botones de accion del sistema.
# utilizamos un bucle para crearlos y para ayudar a que todos tengan el mismo espacio y estilo, manteniendo la interfaz limpia y ordenada.

import ttkbootstrap as ttk
from controlador import ControladorAcciones

class InterfazBotones(ControladorAcciones):
    def crear_botonera(self, contenedor):
        """Genera la fila de botones principales en el centro de la pantalla."""
        
        # Panel interno para centrar los botones dentro del contenedor principal
        inner_f = ttk.Frame(contenedor)
        inner_f.pack(anchor="center")

        #Configuracion de Botones
        # Formato: ("Texto", comando, "estilo_visual", ancho)
        # Esto hace que sea muy facil añadir o quitar funciones después.
        btns = [
            ("REGISTRAR", self.registrar, "success", 22),
            ("HISTORIAL", self.abrir_ventana_historial, "info-outline", 18),
            ("BORRAR", self.borrar, "danger", 18),
            ("LIMPIAR", self.limpiar_campos, "secondary", 12),
            ("RESPALDO", self.crear_respaldo, "warning", 12), 
            ("SALIR", self.salir_aplicacion, "danger", 10)
        ]

        # Construccion automatica de la interfaz
        for texto, comando, estilo, ancho in btns:
            ttk.Button(
                inner_f, 
                text=texto, 
                command=comando, 
                bootstyle=estilo, 
                width=ancho
            ).pack(side="left", padx=5)