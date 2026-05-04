# Importancia del modulo 
import tkinter as tk
from tkinter import filedialog, messagebox
# Para una interfaz moderna (estilo dark)
import ttkbootstrap as ttk      
from ttkbootstrap.constants import *
# Para guardar y leer la base de datos de clientes
import json   
 # Para gestion de rutas y carpetas del sistema 
import os  
# Para copiar archivos (fotos y respaldos)   
import shutil  
 # Para manejar rutas cuando el programa se convierte en .exe                               
import sys    
# Para procesar y mostrar imagenes (cedulas)
from PIL import Image, ImageTk  
# Para registrar fechas de ingreso y pagos
from datetime import datetime    

class GymApp:
    def __init__(self, root):
#Configuracion inicial de la aplicacion y variables de entorno.
        self.root = root
        self.root.title("J.C. TRAINING GROUP - Gestión Pro")
        self.root.geometry("1300x950")      
# Logica para detectar si el programa corre como script o como ejecutable (.exe)
# Esto asegura que los archivos siempre se guarden en la carpeta correcta.
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

# Definicion de rutas para archivos de datos e imagenes
        self.db_file = os.path.join(self.base_dir, "clientes_gym.json")
        self.img_dir = os.path.join(self.base_dir, "cedulas")
        self.historial_dir = os.path.join(self.base_dir, "historiales") 
        
# Creacion de estructura: Crea las carpetas de fotos e historiales si no existen
        for folder in [self.img_dir, self.historial_dir]:
            if not os.path.exists(folder): os.makedirs(folder)
            
# Inicializa el archivo JSON si es la primera vez que se abre la app
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w", encoding="utf-8") as f: json.dump({}, f)

# Confuguracion visual (Colores Neon/Dark)
        self.color_bg = "#0B0E14"
        self.color_accent = "#00F5FF"
        self.color_panel = "#161B22"
        self.style = ttk.Style(theme="darkly")
        self.configurar_estilos()

# Definicion de todos los campos de datos que pedira el formulario
        self.campos = [
            "Nombre", "Apellido", "Edad", "Fecha de Ingreso", "Peso (kg)", 
            "Altura (cm)", "Cintura (cm)", "Brazo (cm)", "Pecho (cm)", 
            "Gluteos (cm)", "Pierna (cm)", "Enfermedades", 
            "Discapacidad", "Ultimo Pago (DD/MM/AAAA)"
        ]
        # Diccionario para almacenar los widgets de entrada (Entry)
        self.entries = {}   
        # Guarda la ruta de la foto antes de registrar al cliente        
        self.ruta_foto_temporal = "" 
        # Variable vinculada a la barra de busqueda
        self.search_var = tk.StringVar() 

        # Inicializar la interfaz y cargar la tabla de clientes
        self.setup_ui()
        self.actualizar_tabla()

    def configurar_estilos(self):
#Define la apariencia personalizada de los marcos, etiquetas y titulos.
        self.style.configure('TFrame', background=self.color_bg)
        self.style.configure('Header.TFrame', background="black")
        self.style.configure('Card.TFrame', background=self.color_panel)
        self.style.configure('Title.TLabel', background="black", foreground=self.color_accent, font=("Segoe UI", 28, "bold"))
        self.style.configure('Search.TLabel', background=self.color_bg, foreground= self.color_accent, font=("Segoe UI", 10, "bold"))

    def setup_ui(self):
#Dibuja todos los elementos de la interfaz gráfica (Botones, Entradas, Tabla).
        # Seleccion superior: Titulo
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill="x")
        ttk.Label(header, text="J.C. TRAINING GROUP", style='Title.TLabel').pack(pady=15)

        # Contenedor principal para formulario y visor de fotos
        top_frame = ttk.Frame(self.root, padding=20)
        top_frame.pack(fill="x")

        #Seccion izquierda: Formulario de datos
        form_panel = ttk.Frame(top_frame, style='Card.TFrame', padding=20)
        form_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Genera automaticamente los campos de texto en 2 columnas
        for i, campo in enumerate(self.campos):
            row, col = i // 2, (i % 2) * 2
            ttk.Label(form_panel, text=f"{campo}:", background=self.color_panel, font=("Segoe UI", 9, "bold")).grid(row=row, column=col, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(form_panel, width=30)
            entry.grid(row=row, column=col+1, padx=10, pady=5, sticky="w")
            self.entries[campo] = entry

        # Boton para cargar la foto de la cedula
        self.btn_foto = ttk.Button(form_panel, text="Seleccionar Foto Cédula", command=self.seleccionar_foto_cedula, bootstyle="info")
        self.btn_foto.grid(row=(len(self.campos)//2)+1, column=0, columnspan=2, pady=10)
        self.lbl_status_foto = ttk.Label(form_panel, text="Sin archivo seleccionado", background=self.color_panel, font=("Segoe UI", 8, "italic"))
        self.lbl_status_foto.grid(row=(len(self.campos)//2)+1, column=2, columnspan=2, sticky="w")

        # Seccion derecha: Visor de imagen
        self.photo_panel = ttk.Frame(top_frame, style='Card.TFrame', padding=20, width=250)
        self.photo_panel.pack(side="right", fill="y")
        self.photo_panel.pack_propagate(False)
        self.lbl_foto_visor = ttk.Label(self.photo_panel, relief="solid", borderwidth=1)
        self.lbl_foto_visor.pack(fill="both", expand=True)

        # Seccion central: Botones de control 
        btn_frame = ttk.Frame(self.root, padding=5)
        btn_frame.pack(fill="x")
        inner_btn_frame = ttk.Frame(btn_frame)
        inner_btn_frame.pack(anchor="center")
        
        ttk.Button(inner_btn_frame, text="REGISTRAR / ACTUALIZAR", command=self.registrar, bootstyle="success", width=22).pack(side="left", padx=5)
        ttk.Button(inner_btn_frame, text="VER HISTORIAL", command=self.abrir_ventana_historial, bootstyle="info-outline", width=18).pack(side="left", padx=5) 
        ttk.Button(inner_btn_frame, text="BORRAR CLIENTE", command=self.borrar, bootstyle="danger", width=18).pack(side="left", padx=5)
        ttk.Button(inner_btn_frame, text="LIMPIAR", command=self.limpiar_campos, bootstyle="secondary", width=12).pack(side="left", padx=5)
        ttk.Button(inner_btn_frame, text="RESPALDO", command=self.crear_respaldo, bootstyle="warning", width=12).pack(side="left", padx=5)

        # Seccion de busqueda rapida sobre la tabla de clientes
        search_frame = ttk.Frame(self.root, padding=(20, 10, 20, 0))
        search_frame.pack(fill="x")
        ttk.Label(search_frame, text="🔍 BUSCAR (Nombre o Apellido):", style='Search.TLabel').pack(side="left", padx=10)
        self.ent_search = ttk.Entry(search_frame, textvariable=self.search_var, width=50, bootstyle="info")
        self.ent_search.pack(side="left", padx=10)
        # La tabla se actualiza automaticamente mientras escribes
        self.search_var.trace_add("write", lambda *args: self.actualizar_tabla(self.search_var.get()))

        # Seccion inferior: Tabla de datos (Treeview)
        table_frame = ttk.Frame(self.root, padding=20)
        table_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Apellido", "Pago"), show="headings", height=8)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        for col in ("ID", "Nombre", "Apellido", "Pago"):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
# Al hacer clic en un cliente de la tabla, se cargan sus datos en el formulario
        self.tree.bind("<<TreeviewSelect>>", self.cargar_desde_tabla)

    def abrir_ventana_historial(self):
# Crea una ventana emergente para mostrar el progreso historico de un cliente.
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista primero.")
            return
        
        id_cliente = self.tree.item(seleccion[0])['values'][0]
        nombre = self.tree.item(seleccion[0])['values'][1]
        
        # Ventana secundaria (Toplevel)
        ventana_h = ttk.Toplevel(self.root)
        ventana_h.title(f"Evolución Histórica: {nombre}")
        ventana_h.geometry("1000x500")
        
        main_frame = ttk.Frame(ventana_h, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text=f"HISTORIAL DE MEDICIONES Y PAGOS", font=("Segoe UI", 14, "bold"), foreground=self.color_accent).pack(pady=10)

        # Tabla dentro de la ventana de historial
        columnas = ("Fecha Registro", "Peso", "Cintura", "Brazo", "Pecho", "Gluteos", "Pierna", "Ultimo Pago")
        tree_h = ttk.Treeview(main_frame, columns=columnas, show="headings")
        
        for col in columnas:
            tree_h.heading(col, text=col)
            tree_h.column(col, width=110, anchor="center")
        
        tree_h.pack(fill="both", expand=True)
        
# Lee el archivo JSON individual del cliente y llena la tabla
        ruta_h = os.path.join(self.historial_dir, f"{id_cliente}.json")
        if os.path.exists(ruta_h):
            with open(ruta_h, "r", encoding="utf-8") as f:
                datos_h = json.load(f)
                # Muestra los más nuevos primero
                for reg in reversed(datos_h): 
                    tree_h.insert("", "end", values=(
                        reg.get("Fecha_Sistema", "---"),
                        reg.get("Peso (kg)", ""),
                        reg.get("Cintura (cm)", ""),
                        reg.get("Brazo (cm)", ""),
                        reg.get("Pecho (cm)", ""),
                        reg.get("Gluteos (cm)", ""),
                        reg.get("Pierna (cm)", ""),
                        reg.get("Ultimo Pago (DD/MM/AAAA)", "")
                    ))

    def cargar_datos(self):
#Lee la base de datos principal desde el archivo JSON.
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}

    def guardar_datos(self, datos):
#Escribe la base de datos completa en el archivo JSON.
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def crear_respaldo(self):
#Copia todos los datos (JSON y fotos) a una carpeta elegida por el usuario.
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
        destino = filedialog.askdirectory(title="Selecciona dónde guardar el respaldo")
        if destino:
            folder_respaldo = os.path.join(destino, f"Respaldo_Gym_{fecha}")
            try:
                os.makedirs(folder_respaldo)
                # Copia JSON principal
                shutil.copy2(self.db_file, folder_respaldo) 
                # Copia fotos
                shutil.copytree(self.img_dir, os.path.join(folder_respaldo, "cedulas")) 
                # Copia progresos
                shutil.copytree(self.historial_dir, os.path.join(folder_respaldo, "historiales")) 
                messagebox.showinfo("Copia Exitosa", "Respaldo completo creado.")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al respaldar: {e}")

    def validar_campos_numericos(self):
# Verifica que los campos de medidas contengan números válidos antes de guardar.
        campos_a_validar = [
            "Edad", "Peso (kg)", "Altura (cm)", "Cintura (cm)", 
            "Brazo (cm)", "Pecho (cm)", "Gluteos (cm)", "Pierna (cm)"
        ]
        for campo in campos_a_validar:
            valor = self.entries[campo].get().strip()
            if valor: 
                try:
                    float(valor.replace(',', '.')) 
                except ValueError:
                    messagebox.showerror("Error de formato", f"El campo '{campo}' debe ser un número válido.")
                    return False
        return True

    def registrar(self):
#Recopila los datos del formulario y los guarda en el JSON principal y en el historial.
        if not self.validar_campos_numericos():
            return
        
        nombre = self.entries['Nombre'].get().strip()
        apellido = self.entries['Apellido'].get().strip()
        if not nombre or not apellido:
            messagebox.showwarning("Faltan datos", "Nombre y Apellido requeridos.")
            return

# Genera un ID único basado en el nombre (ej: juan_perez)
        id_c = f"{nombre.lower()}_{apellido.lower()}".replace(" ", "")
        d = self.cargar_datos()
        
# Procesa la foto si se selecciono una nueva
        nombre_foto = self.gestionar_copiado_foto(id_c)
        if not nombre_foto and id_c in d: nombre_foto = d[id_c].get("foto_cedula")

# Crea un diccionario con los datos actuales del formulario
        datos = {c: self.entries[c].get() for c in self.campos}
        datos["foto_cedula"] = nombre_foto
        
#Logica de Historial: Guarda una 'foto' de los datos hoy 
        ruta_h = os.path.join(self.historial_dir, f"{id_c}.json")
        historial = []
        if os.path.exists(ruta_h):
            with open(ruta_h, "r", encoding="utf-8") as f: historial = json.load(f)
        
        registro_hoy = datos.copy()
        registro_hoy["Fecha_Sistema"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        historial.append(registro_hoy)
        
        with open(ruta_h, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)
        
# Guarda en la base de datos principal
        d[id_c] = datos
        self.guardar_datos(d)
        self.actualizar_tabla()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Datos y progreso guardados correctamente.")

    def actualizar_tabla(self, filtro=""):
#Refresca la lista de clientes mostrada en la tabla, permitiendo filtrar por busqueda.
        for i in self.tree.get_children(): self.tree.delete(i)
        d = self.cargar_datos()
        filtro = filtro.lower()
        for k, v in d.items():
            if not filtro or filtro in v.get("Nombre", "").lower() or filtro in v.get("Apellido", "").lower():
                self.tree.insert("", "end", values=(k, v.get("Nombre",""), v.get("Apellido",""), v.get("Ultimo Pago (DD/MM/AAAA)","--")))

    def gestionar_copiado_foto(self, id_cliente):
#Mueve la foto desde la carpeta de origen a la carpeta interna del programa.
        if not self.ruta_foto_temporal or not os.path.exists(self.ruta_foto_temporal): return None
        ext = os.path.splitext(self.ruta_foto_temporal)[1]
        nuevo_nombre = f"cedula_{id_cliente}{ext}"
        shutil.copy2(self.ruta_foto_temporal, os.path.join(self.img_dir, nuevo_nombre))
        return nuevo_nombre

    def seleccionar_foto_cedula(self):
#Abre el explorador de archivos para elegir una imagen de cedula.
        filename = filedialog.askopenfilename(filetypes=[('Imágenes', '*.jpg *.jpeg *.png')])
        if filename:
            self.ruta_foto_temporal = filename
            self.lbl_status_foto.config(text="Foto vinculada", foreground=self.color_accent)
            self.visualizar_imagen(filename)

    def visualizar_imagen(self, ruta):
                                          #Ajusta y muestra la imagen en el visor de la derecha.
        try:
            img = Image.open(ruta)
            img.thumbnail((220, 280), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_foto_visor.config(image=photo, text="")
            self.lbl_foto_visor.image = photo
        except: self.mostrar_imagen_placeholder()

    def mostrar_imagen_placeholder(self):
# Muestra un mensaje de 'Sin Foto' cuando no hay imagen disponible.
        self.lbl_foto_visor.config(image='', text="SIN FOTO", foreground="grey")

    def cargar_desde_tabla(self, event):
# Rellena el formulario con los datos del cliente seleccionado en la tabla.
        seleccion = self.tree.selection()
        if not seleccion: return
        id_cliente = self.tree.item(seleccion[0])['values'][0]
        cliente = self.cargar_datos().get(id_cliente, {})
        self.limpiar_campos()
# Rellena cada Entry con el valor correspondiente del JSON
        for campo in self.campos:
            if campo in cliente: self.entries[campo].insert(0, cliente[campo])
        # Carga la foto en el visor
        foto = cliente.get("foto_cedula")
        if foto:
            ruta = os.path.join(self.img_dir, foto)
            if os.path.exists(ruta): self.visualizar_imagen(ruta)
            else: self.mostrar_imagen_placeholder()
        else: self.mostrar_imagen_placeholder()

    def borrar(self):
# Elimina permanentemente a un cliente, su foto y su historial de progresos.
        seleccion = self.tree.selection()
        if not seleccion: return
        id_cliente = self.tree.item(seleccion[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente y todo su historial?"):
            d = self.cargar_datos()
            # Borrar archivo de foto fisica
            foto = d[id_cliente].get("foto_cedula")
            if foto:
                ruta_f = os.path.join(self.img_dir, foto)
                if os.path.exists(ruta_f): os.remove(ruta_f)
            # Borrar archivo JSON de historial
            ruta_h = os.path.join(self.historial_dir, f"{id_cliente}.json")
            if os.path.exists(ruta_h): os.remove(ruta_h)
            
            # Borrar registro del JSON principal y actualizar
            del d[id_cliente]
            self.guardar_datos(d)
            self.actualizar_tabla()
            self.limpiar_campos()

    def limpiar_campos(self):
        """Vacía todas las cajas de texto y el visor de fotos."""
        for e in self.entries.values(): e.delete(0, tk.END)
        self.ruta_foto_temporal = ""
        self.lbl_status_foto.config(text="No seleccionada", foreground="white")
        self.mostrar_imagen_placeholder()

# Arranque de la aplicacion 
if __name__ == "__main__":
    # Crea la ventana con el tema oscuro
    root = ttk.Window(themename="darkly") 
    app = GymApp(root)
    root.update()
    app.mostrar_imagen_placeholder()
    # Inicia el bucle de eventos
    root.mainloop() 