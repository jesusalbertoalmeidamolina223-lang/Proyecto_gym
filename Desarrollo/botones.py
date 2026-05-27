# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# El panel de Control (Interfaz de Botones)
# Ubicamos todos los botones de accion del sistema.
import ttkbootstrap as ttk

class InterfazBotones:
    @staticmethod
    def construir_panel_botones(contenedor_visual, referencia_app):
        """Construye el panel de botones en el contenedor visual."""
        inner_frame = ttk.Frame(contenedor_visual)
        inner_frame.pack(anchor="center")

        # Configuracion de botones con su texto, metodo asociado, estilo visual y ancho especificos
        esquema_botones = [
            ("REGISTRAR", referencia_app.ejecutar_registro, "success", 22),
            ("HISTORIAL", referencia_app.abrir_ventana_historial, "info-outline", 18),
            ("BORRAR", referencia_app.ejecutar_borrado, "danger", 18),
            ("LIMPIAR", referencia_app.limpiar_formulario, "secondary", 12),
            ("RESPALDO", referencia_app.ejecutar_respaldo, "warning", 12), 
            ("SALIR", referencia_app.solicitar_salida, "danger", 10)
        ]

        for texto, metodo, estilo, ancho in esquema_botones:
            ttk.Button(
                inner_frame, 
                text=texto, 
                command=metodo, 
                bootstyle=estilo, 
                width=ancho
            ).pack(side="left", padx=5)