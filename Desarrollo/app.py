# J.C. TRAINING GROUP - Ensamblaje Principal de la Interfaz (UI)
# Este es el archivo donde todo se une. Aqui organizamos como se distribuyen
# visualmente el formulario, la tabla y el visor de fotos para que el sistema sea comodo de usar en el dia a dia del gimnasio.

import ttkbootstrap as ttk
from botones import InterfazBotones

class GymApp(InterfazBotones):
    def __init__(self, root):
        super().__init__(root)
        
        #Configuracion de la ventana principal
        self.root.title("J.C. TRAINING GROUP - Gestión de Atletas")
        self.root.geometry("1300x950")
        
        #Arrancamos los motores visuales y de datos
        self.configurar_estilos()
        self.setup_ui()
        self.actualizar_tabla()
        self.mostrar_imagen_placeholder()

    def setup_ui(self):
        """Distribuye los elementos en la pantalla (Header, Cuerpo y Tabla)."""
        
        #Encabezado
        h = ttk.Frame(self.root, style='Header.TFrame')
        h.pack(fill="x")
        ttk.Label(h, text="J.C. TRAINING GROUP", style='Title.TLabel').pack(pady=15)

        #Zona Superior: Formulario y Foto 
        top_container = ttk.Frame(self.root, padding=20)
        top_container.pack(fill="x")
        
        #Panel del Formulario
        form_panel = ttk.Frame(top_container, style='Card.TFrame', padding=20)
        form_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        #Generamos los campos automáticamente desde la lista definida en estilos.py
        for i, campo in enumerate(self.campos):
            ttk.Label(form_panel, text=f"{campo}:", 
                      background=self.color_panel, 
                      font=("Segoe UI", 9, "bold")).grid(row=i//2, column=(i%2)*2, 
                                                       padx=10, pady=5, sticky="e")

            self.entries[campo] = ttk.Entry(form_panel, width=30)
            self.entries[campo].grid(row=i//2, column=(i%2)*2+1, 
                                     padx=10, pady=5, sticky="w")

        #Control de imagen en el formulario
        ttk.Button(form_panel, text="Seleccionar Foto", 
                   command=self.seleccionar_foto_cedula, 
                   bootstyle="info").grid(row=8, column=0, columnspan=2, pady=10)
        
        self.lbl_status_foto = ttk.Label(form_panel, text="Sin archivo seleccionado", 
                                        background=self.color_panel)
        self.lbl_status_foto.grid(row=8, column=2, sticky="w")

        #Visor de Foto (a la derecha del formulario)
        visor_panel = ttk.Frame(top_container, style='Card.TFrame', padding=20, width=250)
        visor_panel.pack(side="right", fill="y")
        visor_panel.pack_propagate(False) # Evita que el panel se encoja
        
        self.lbl_foto_visor = ttk.Label(visor_panel, relief="solid", borderwidth=1)
        self.lbl_foto_visor.pack(fill="both", expand=True)

        #Zona Media: Botones de Accion
        btn_container = ttk.Frame(self.root, padding=5)
        btn_container.pack(fill="x")
        self.crear_botonera(btn_container)

        #Zona de Busqueda
        search_frame = ttk.Frame(self.root, padding=(20, 10, 20, 0))
        search_frame.pack(fill="x")
        
        ttk.Label(search_frame, text="BUSCAR ATLETA:", style='Search.TLabel').pack(side="left", padx=10)
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                width=50, bootstyle="info")
        search_entry.pack(side="left", padx=10)
        
        #Filtro en tiempo real mientras se escribe
        self.search_var.trace_add("write", lambda *a: self.actualizar_tabla(self.search_var.get()))

        #Zona Inferior: Tabla de Datos
        table_frame = ttk.Frame(self.root, padding=20)
        table_frame.pack(fill="both", expand=True)
        
        columnas = ("ID", "Nombre", "Apellido", "Pago")
        self.tree = ttk.Treeview(table_frame, columns=columnas, show="headings", height=8)
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
            
        self.tree.pack(side="left", fill="both", expand=True)
        
        #Evento para cargar datos al hacer clic en la tabla
        self.tree.bind("<<TreeviewSelect>>", self.cargar_desde_tabla)