# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Se encarga de ser el ensamblaje Principal de la Interfaz (UI)
# Este es el archivo en donde todo se une. Aqui organizamos como se distribuyen visualmente el formulario,
# la tabla y el visor de fotos para que el sistema sea comodo de usar en el dia a dia del gimnasio.
# app.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk

# Importacion de dependencias siguiendo la orquestacion del diagrama
from controlador import ControladorAcciones
from estilos import EstilosInterfaz
from botones import InterfazBotones

class GymApp:
    def __init__(self, root):
        self.root = root
        
        # Inicio de Capas Inferiores
        self.controlador = ControladorAcciones()
        self.esquema_visual = EstilosInterfaz()
        self.campos = self.esquema_visual.campos
        
        # Variables de control de la Interfaz (UI State)
        self.entries = {}
        self.ruta_foto_temporal = ""
        self.search_var = tk.StringVar()
        
        self.inicializar_estilos_entorno()
        self.setup_ui()
        self.actualizar_tabla_datos()
        self.mostrar_placeholder_visor()

    def inicializar_estilos_entorno(self):
        self.root.title("J.C. TRAINING GROUP - Gestión de Atletas")
        self.root.geometry("1300x950")
        
        self.style = ttk.Style(theme="darkly")
        # Definicion de estilos personalizados para la aplicacion
        self.style.configure('TFrame', background=self.controlador.color_bg)
        self.style.configure('Header.TFrame', background="black")
        self.style.configure('Card.TFrame', background=self.controlador.color_panel)
        self.style.configure('Title.TLabel', background="black", foreground=self.controlador.color_accent, font=("Segoe UI", 28, "bold"))
        self.style.configure('Search.TLabel', background=self.controlador.color_bg, foreground=self.controlador.color_accent, font=("Segoe UI", 10, "bold"))

    def setup_ui(self):
        # Encabezado (Header)
        h = ttk.Frame(self.root, style='Header.TFrame')
        h.pack(fill="x")
        ttk.Label(h, text="J.C. TRAINING GROUP", style='Title.TLabel').pack(pady=15)

        # Zona Superior (Formulario interactivo + Panel fotografico)
        top_container = ttk.Frame(self.root, padding=20)
        top_container.pack(fill="x")
        # Panel de Formulario con diseño de tarjeta para mejorar la estetica y organización visual
        form_panel = ttk.Frame(top_container, style='Card.TFrame', padding=20)
        form_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Construccion dinamica de Entradas de Texto
        for i, campo in enumerate(self.campos):
            ttk.Label(form_panel, text=f"{campo}:", background=self.controlador.color_panel, font=("Segoe UI", 9, "bold")).grid(
                row=i//2, column=(i%2)*2, padx=10, pady=5, sticky="e"
            )
            self.entries[campo] = ttk.Entry(form_panel, width=30)
            self.entries[campo].grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5, sticky="w")

        ttk.Button(form_panel, text="Seleccionar Foto", command=self.solicitar_foto_interfaz, bootstyle="info").grid(row=8, column=0, columnspan=2, pady=10)
        self.lbl_status_foto = ttk.Label(form_panel, text="Sin archivo seleccionado", background=self.controlador.color_panel)
        self.lbl_status_foto.grid(row=8, column=2, sticky="w")

        # Visor de Fotos Independiente
        visor_panel = ttk.Frame(top_container, style='Card.TFrame', padding=20, width=250)
        visor_panel.pack(side="right", fill="y")
        visor_panel.pack_propagate(False)
        self.lbl_foto_visor = ttk.Label(visor_panel, relief="solid", borderwidth=1)
        self.lbl_foto_visor.pack(fill="both", expand=True)

        # Zona Media (Panel de Botones)
        btn_container = ttk.Frame(self.root, padding=5)
        btn_container.pack(fill="x")
        InterfazBotones.construir_panel_botones(btn_container, self)

        # Zona de Busqueda Interactiva
        search_frame = ttk.Frame(self.root, padding=(20, 10, 20, 0))
        search_frame.pack(fill="x")
        ttk.Label(search_frame, text="BUSCAR ATLETA:", style='Search.TLabel').pack(side="left", padx=10)
        ttk.Entry(search_frame, textvariable=self.search_var, width=50, bootstyle="info").pack(side="left", padx=10)
        self.search_var.trace_add("write", lambda *a: self.actualizar_tabla_datos(self.search_var.get()))

        # Zona Inferior: Tabla de Datos
        table_frame = ttk.Frame(self.root, padding=20)
        table_frame.pack(fill="both", expand=True)
        columnas = ("ID", "Nombre", "Apellido", "Pago")
        self.tree = ttk.Treeview(table_frame, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.cargar_datos_en_campos)

    def solicitar_foto_interfaz(self):
        filename = filedialog.askopenfilename(filetypes=[('Imágenes', '*.jpg *.jpeg *.png')])
        if filename:
            self.ruta_foto_temporal = filename
            self.lbl_status_foto.config(text="Foto vinculada", foreground=self.controlador.color_accent)
            self.renderizar_imagen_visor(filename)

    def renderizar_imagen_visor(self, ruta):
        try:
            img = Image.open(ruta)
            img.thumbnail((220, 280), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_foto_visor.config(image=photo, text="")
            self.lbl_foto_visor.image = photo
        except Exception:
            self.placeholder_visor()

    def mostrar_placeholder_visor(self):
        self.lbl_foto_visor.config(image='', text="SIN FOTO", foreground="grey")

    def actualizar_tabla_datos(self, filtro=""):
        for item in self.tree.get_children(): 
            self.tree.delete(item)
            
        # Invoca capa de negocio para obtener datos filtrados y actualiza la tabla
        datos_filtrados = self.controlador.filtrar_atletas(filtro)
        for k, v in datos_filtrados.items():
            self.tree.insert("", "end", values=(k, v.get("Nombre", ""), v.get("Apellido", ""), v.get("Ultimo Pago (DD/MM/AAAA)", "--")))

    def ejecutar_registro(self):
        valores_formulario = {c: self.entries[c].get().strip() for c in self.campos}
        
        # Capa de control responde de manera preventiva ante errores comunes de entrada de datos
        es_valido, campo_error = self.controlador.verificar_campos_medidas(valores_formulario)
        if not es_valido:
            return messagebox.showerror("Dato no válido", f"El campo '{campo_error}' solo acepta números.")
        
        if not valores_formulario['Nombre'] or not valores_formulario['Apellido']:
            return messagebox.showwarning("Campos vacíos", "El nombre y apellido son obligatorios.")

        # Almacenamiento y actualizacion de la interfaz tras el registro exitoso
        self.controlador.procesar_registro(valores_formulario, self.ruta_foto_temporal)
        self.actualizar_tabla_datos()
        self.limpiar_formulario()
        messagebox.showinfo("Hecho", "¡Atleta guardado exitosamente!")

    def cargar_datos_en_campos(self, _):
        seleccion = self.tree.selection()
        if not seleccion: return
        id_c = self.tree.item(seleccion[0])['values'][0]
        perfil = self.controlador.cargar_datos().get(id_c, {})
        
        self.limpiar_formulario()
        for campo, valor in perfil.items():
            if campo in self.entries:
                self.entries[campo].insert(0, valor)
        
        foto = perfil.get("foto_cedula")
        if foto:
            ruta = os.path.join(self.controlador.img_dir, foto)
            if os.path.exists(ruta):
                self.renderizar_imagen_visor(ruta)
                return
        self.mostrar_placeholder_visor()

    def ejecutar_borrado(self):
        seleccion = self.tree.selection()
        if not seleccion: return
        
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este atleta del sistema?"):
            id_c = self.tree.item(seleccion[0])['values'][0]
            self.controlador.procesar_borrado_completo(id_c)
            self.actualizar_tabla_datos()
            self.limpiar_formulario()
            messagebox.showinfo("Hecho", "El perfil fue removido exitosamente.")

    def limpiar_formulario(self):
        for entry in self.entries.values(): 
            entry.delete(0, tk.END)
        self.ruta_foto_temporal = ""
        self.lbl_status_foto.config(text="Sin archivo seleccionado", foreground="white")
        self.mostrar_placeholder_visor()

    def abrir_ventana_historial(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return messagebox.showwarning("Atención", "Por favor, elija un atleta de la tabla.")
        
        id_cliente = self.tree.item(seleccion[0])['values'][0]
        nombre = self.tree.item(seleccion[0])['values'][1]
        
        # Nueva Subventana de Presentación
        ventana_h = ttk.Toplevel(self.root)
        ventana_h.title(f"Línea de Tiempo - Evolución de: {nombre}")
        ventana_h.geometry("1000x500")
        
        main_frame = ttk.Frame(ventana_h, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        columnas = ("Fecha Registro", "Peso", "Cintura", "Brazo", "Pecho", "Gluteos", "Pierna", "Último Pago")
        tree_h = ttk.Treeview(main_frame, columns=columnas, show="headings")
        for col in columnas:
            tree_h.heading(col, text=col)
            tree_h.column(col, width=110, anchor="center")
        tree_h.pack(fill="both", expand=True)
        
        # Recuperacion y presentación de linea de tiempo historial de los atletas
        datos_h = self.controlador.obtener_historial_atleta(id_cliente)
        for reg in reversed(datos_h): 
            tree_h.insert("", "end", values=(
                reg.get("Fecha_Sistema", "---"), reg.get("Peso (kg)", ""),
                reg.get("Cintura (cm)", ""), reg.get("Brazo (cm)", ""),
                reg.get("Pecho (cm)", ""), reg.get("Gluteos (cm)", ""),
                reg.get("Pierna (cm)", ""), reg.get("Ultimo Pago (DD/MM/AAAA)", "")
            ))

    def ejecutar_respaldo(self):
        destino = filedialog.askdirectory(title="Selecciona la ruta de destino para el respaldo")
        if destino:
            try:
                ruta_final = self.controlador.empaquetar_respaldo_sistema(destino)
                messagebox.showinfo("Respaldo Creado", f"Copia de seguridad guardada con éxito en:\n{ruta_final}")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al empaquetar el sistema: {e}")

    def solicitar_salida(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar el sistema J.C. Training?"):
            self.root.destroy()