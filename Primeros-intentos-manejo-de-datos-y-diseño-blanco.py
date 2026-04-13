import tkinter as tk  # Importa la librería base para interfaces gráficas

from tkinter import ttk, messagebox, filedialog  # Importa widgets avanzados, cuadros de mensajes y selector de archivos

import json  # Importa la librería para manejar archivos de datos tipo JSON

from datetime import datetime  # Importa funciones para manejar fechas y tiempos

import os  # Importa funciones para interactuar con el sistema operativo (carpetas/rutas)

import shutil  # Importa funciones para copiar archivos (usado para las fotos)

class GymApp:  # Define la clase principal de la aplicación

    def __init__(self, root):  # Método constructor que inicializa la aplicación

#FASE 1: CONFIGURACIÓN DE VENTANA Y RUTAS

        self.root = root  # Guarda la ventana principal en una variable

        self.root.title("J.C. TRAINING GROUP - Gestión Profesional")  # Define el título de la ventana

        self.root.geometry("1100x950")  # Establece el tamaño inicial de la ventana

        self.root.configure(bg="#F0F8FF")  # Define el color de fondo (Alice Blue)

        self.base_path = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta de la carpeta donde está el script
        self.db_file = os.path.join(self.base_path, "clientes_gym.json")  # Define la ruta del archivo de base de datos
        self.img_dir = os.path.join(self.base_path, "cedulas")  # Define la ruta de la carpeta para guardar fotos
        
        if not os.path.exists(self.img_dir):  # Verifica si la carpeta de fotos NO existe

            os.makedirs(self.img_dir)  # Crea la carpeta de fotos si no existía

        # Lista con los nombres de todos los campos que tendrá el formulario
        self.campos = [
            "Nombre", "Apellido", "Edad", "Fecha de Ingreso", "Peso (kg)", 
            "Altura (cm)", "Cintura (cm)", "Brazo (cm)", "Pecho (cm)", 
            "Gluteos (cm)", "Muslos (cm)", "Pierna (cm)", "Enfermedades", 
            "Discapacidad", "Ultimo Pago (DD/MM/AAAA)"
        ]
        self.entries = {}  # Diccionario vacío para almacenar los cuadros de texto (Entry)
        self.foto_path_temp = ""  # Variable para guardar la ruta de la foto seleccionada temporalmente

        # Variables de colores para mantener la estética azul y negro
        self.color_borde_form = "#2196F3"  # Azul brillante
        self.color_borde_boton = "#1976D2"  # Azul oscuro
        self.color_header_busqueda = "#64B5F6"  # Azul claro
        
        self.setup_ui()  # Llama a la función que dibuja la interfaz
        self.actualizar_tabla()  # Carga los datos existentes en la tabla al abrir

    def setup_ui(self):  # Método para crear los elementos visuales

#FASE 2: DISEÑO DE LA INTERFAZ (UI)

        # Crea el encabezado negro superior
        header = tk.Frame(self.root, bg="black", height=80, highlightbackground=self.color_borde_boton, highlightthickness=1)
        header.pack(fill="x")  # Lo expande horizontalmente

        tk.Label(header, text="J.C. TRAINING GROUP", font=("Helvetica", 24, "bold"), 
                 fg="white", bg="black").pack(pady=20)  # Agrega el título dentro del encabezado

        # Crea el contenedor principal de la aplicación
        main_frame = tk.Frame(self.root, bg="#F0F8FF")
        main_frame.pack(pady=10, padx=25, fill="both", expand=True)  # Se ajusta a la ventana

        # Crea un recuadro con título para agrupar los datos del cliente
        form_frame = tk.LabelFrame(main_frame, text=" Datos del Cliente ", bg="#F0F8FF", 
                                   font=("Helvetica", 11, "bold"), bd=2, 
                                   highlightbackground=self.color_borde_form, highlightthickness=1)
        form_frame.pack(fill="x", pady=10)

        # Bucle para crear automáticamente etiquetas y cuadros de texto según la lista de campos
        for i, campo in enumerate(self.campos):
            row, col = i // 2, (i % 2) * 2  # Calcula la posición en una cuadrícula de 2 columnas
            tk.Label(form_frame, text=f"{campo}:", bg="#F0F8FF").grid(row=row, column=col, padx=12, pady=5, sticky="e")
            entry = tk.Entry(form_frame, width=32, highlightthickness=1, highlightbackground="#D3D3D3")
            entry.grid(row=row, column=col+1, padx=12, pady=5)
            self.entries[campo] = entry  # Guarda el widget en el diccionario para usarlo luego

        # Contenedor para la sección de carga de cédula
        cedula_frame = tk.Frame(form_frame, bg="#F0F8FF")
        cedula_frame.grid(row=8, column=0, columnspan=4, pady=15)
        tk.Button(cedula_frame, text="Subir Cédula", command=self.seleccionar_foto, bg="black", fg="white").pack(side="left", padx=8)
        self.lbl_foto = tk.Label(cedula_frame, text="Sin archivo", bg="#F0F8FF", fg="#616161")
        self.lbl_foto.pack(side="left", padx=12)  # Texto que indica si se cargó la foto

        # Contenedor para los botones principales (Registrar, Borrar, Limpiar)
        btn_frame = tk.Frame(main_frame, bg="#F0F8FF")
        btn_frame.pack(pady=15)
        for texto, comando in [("Registrar", self.registrar), ("Borrar", self.borrar), ("Limpiar", self.limpiar_campos)]:
            tk.Button(btn_frame, text=texto, command=comando, bg="black", fg="white", width=14, 
                      font=("Helvetica", 10, "bold"), bd=1, highlightthickness=2).pack(side="left", padx=8)

# Sección de búsqueda
        search_frame = tk.Frame(main_frame, bg="#F0F8FF")
        search_frame.pack(fill="x")
        self.var_busqueda = tk.StringVar()  # Variable especial para detectar cambios en el texto
        self.var_busqueda.trace("w", lambda *args: self.actualizar_tabla())  # Al escribir, actualiza la tabla automáticamente
        tk.Label(search_frame, text="Buscar:", bg="#F0F8FF").pack(side="left", padx=10)
        tk.Entry(search_frame, textvariable=self.var_busqueda, width=40).pack(side="left", padx=10, pady=10)

        # Creación de la tabla de visualización (Treeview)
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Apellido", "Estado"), show="headings", height=10)
        for col in ("ID", "Nombre", "Apellido", "Estado"):
            self.tree.heading(col, text=col)  # Define los encabezados de la tabla
            self.tree.column(col, anchor="center")  # Centra el contenido de las columnas
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.cargar_desde_tabla)  # Al hacer clic en un cliente, carga sus datos

#FASE 3: LÓGICA DE DATOS Y ARCHIVOS

    def obtener_id(self):  # Genera una clave única para cada cliente

        n = self.entries["Nombre"].get().strip().lower()  # Obtiene el nombre en minúsculas

        a = self.entries["Apellido"].get().strip().lower()  # Obtiene el apellido en minúsculas
        return f"{n}_{a}".replace(" ", "")  # Junta nombre y apellido eliminando espacios
    

    def cargar_datos(self):  # Lee el archivo JSON
        if not os.path.exists(self.db_file): return {}  # Si no existe el archivo, devuelve un diccionario vacío
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: return json.load(f)  # Carga y devuelve los datos
        except: return {}  # En caso de error, devuelve vacío

    def seleccionar_foto(self):  # Abre el explorador de archivos para elegir una imagen
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
        if ruta:
            self.foto_path_temp = ruta  # Guarda la ruta seleccionada
            self.lbl_foto.config(text="Foto lista", fg="green")  # Avisa visualmente
# Guarda o actualiza un cliente
    def registrar(self):  
        id_c = self.obtener_id()  # Genera el ID
        if len(id_c) < 2:  # Valida que no esté vacío
            messagebox.showwarning("Error", "Nombre y Apellido son obligatorios.")
            return
# Carga la base de datos actual
        d = self.cargar_datos()  
        foto_final = ""
        if self.foto_path_temp:  # Si el usuario seleccionó una foto nueva
            ext = os.path.splitext(self.foto_path_temp)[1]  # Obtiene la extensión (.jpg, .png)
            foto_final = os.path.join(self.img_dir, f"{id_c}{ext}").replace("\\", "/")  # Define nueva ruta
            shutil.copy(self.foto_path_temp, foto_final)  # Copia el archivo a la carpeta del programa

        # Crea un diccionario con la información escrita en los campos
        info = {c: self.entries[c].get().strip() for c in self.campos}
        # Si no subió foto nueva, intenta mantener la que ya tenía guardada
        info["foto_cedula"] = foto_final if foto_final else d.get(id_c, {}).get("foto_cedula", "")
        
        d[id_c] = info  # Agrega o sobreescribe el cliente en el diccionario
        with open(self.db_file, "w", encoding="utf-8") as f: 
            json.dump(d, f, indent=4, ensure_ascii=False)  # Guarda el JSON actualizado
        
        self.actualizar_tabla()  # Refresca la tabla
        self.limpiar_campos()  # Limpia el formulario
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")

    def actualizar_tabla(self):  # Muestra los clientes en la lista visual
        for i in self.tree.get_children(): self.tree.delete(i)  # Borra todo lo que hay en la tabla actualmente
        d = self.cargar_datos()  # Carga los datos del JSON
        busqueda = self.var_busqueda.get().lower()  # Obtiene lo que el usuario escribió en el buscador
        
        for k, v in d.items():  # Recorre cada cliente
            # Filtra por nombre o apellido
            if busqueda in v["Nombre"].lower() or busqueda in v["Apellido"].lower():
                try:
                    fp = datetime.strptime(v["Ultimo Pago (DD/MM/AAAA)"], "%d/%m/%Y")  # Convierte texto a fecha
                    # Si pasaron 30 días o menos, está al día, si no, pendiente
                    est = "AL DÍA" if (datetime.now() - fp).days <= 30 else "PENDIENTE"
                except: est = "S/D"  # Si la fecha está mal escrita pone Sin Datos
                self.tree.insert("", "end", values=(k, v["Nombre"], v["Apellido"], est))  # Agrega la fila a la tabla

    def cargar_desde_tabla(self, event):  # Pone los datos de un cliente seleccionado en el formulario

        if not self.tree.selection(): return  # Si no hay nada seleccionado, no hace nada

        item = self.tree.selection()[0]  # Obtiene el elemento seleccionado

        id_c = self.tree.item(item)['values'][0]  # Obtiene el ID (que está en la primera columna oculta)
        d = self.cargar_datos()
        if id_c in d:
            c = d[id_c]
            for campo in self.campos:  # Llena cada cuadro de texto con la info del JSON
                self.entries[campo].delete(0, tk.END)
                self.entries[campo].insert(0, c[campo])
            foto = c.get("foto_cedula", "")
            if foto and os.path.exists(foto): os.startfile(foto)  # Abre la foto automáticamente si existe
# Elimina un cliente
    def borrar(self):  
        id_c = self.obtener_id()  # Obtiene el ID del formulario
        d = self.cargar_datos()
        if id_c in d and messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            f = d[id_c].get("foto_cedula", "")
            if f and os.path.exists(f): 
                try: os.remove(f)  # Intenta borrar el archivo de la foto
                except: pass
# Borra los datos del diccionario
            del d[id_c]  

            with open(self.db_file, "w", encoding="utf-8") as f: json.dump(d, f, indent=4)  # Guarda el JSON

            self.actualizar_tabla()  # Refresca la lista

            self.limpiar_campos()  # Limpia el formulario

    def limpiar_campos(self):  # Borra todo el texto del formulario

        for e in self.entries.values(): e.delete(0, tk.END)  # Limpia cada cuadro de texto

        self.foto_path_temp = ""  # Resetea la ruta de la foto

        self.lbl_foto.config(text="Sin archivo", fg="grey")  # Resetea la etiqueta de foto

if __name__ == "__main__":  # Punto de inicio del programa
    root = tk.Tk()  # Crea la ventana principal
    app = GymApp(root)  # Crea la instancia de la aplicación
    root.mainloop()  # Mantiene la ventana abierta y escuchando eventos