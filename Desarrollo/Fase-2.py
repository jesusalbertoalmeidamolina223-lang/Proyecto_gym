# Fase 2: Interfaz Visual (UI) y Estilo Dark
# En esta fase se configura la estética "Neon/Dark" y posicion de los elementos (widgets). Uso de ttkbootstrap nos permite que la aplicacion se vea mejor.
# --- CONFIGURACIÓN VISUAL ---
self.color_bg = "#0B0E14"
self.color_accent = "#00F5FF"
self.color_panel = "#161B22"
self.style = ttk.Style(theme="darkly")
self.configurar_estilos()

# Definición de campos
self.campos = [
            "Nombre", "Apellido", "Edad", "Fecha de Ingreso", "Peso (kg)", 
            "Altura (cm)", "Cintura (cm)", "Brazo (cm)", "Pecho (cm)", 
            "Gluteos (cm)", "Pierna (cm)", "Enfermedades", 
            "Discapacidad", "Ultimo Pago (DD/MM/AAAA)"
        ]
self.entries = {}
self.ruta_foto_temporal = ""
self.search_var = tk.StringVar()

self.setup_ui() # Llama a la construcción de la interfaz
self.actualizar_tabla()

def configurar_estilos(self):
        self.style.configure('TFrame', background=self.color_bg)
        self.style.configure('Header.TFrame', background="black")
        self.style.configure('Card.TFrame', background=self.color_panel)
        self.style.configure('Title.TLabel', foreground=self.color_accent, font=("Segoe UI", 28, "bold"))