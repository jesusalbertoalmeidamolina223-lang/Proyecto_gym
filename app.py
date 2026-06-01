import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk

# Importación del núcleo de lógica
from core_logic.motor_atletas import ControladorAcciones
from estilos import EstilosInterfaz

# Importación de componentes visuales desacoplados
from gui_components.formulario import FormularioAtleta
from gui_components.tabla import TablaAtletas
from gui_components.visor_fotos import VisorMultimedia
from gui_components.botones import InterfazBotones

class GymApp:
    def __init__(self, root):
        self.root = root
        self.controlador = ControladorAcciones()
        self.esquema_visual = EstilosInterfaz()
        self.campos = self.esquema_visual.campos
        
        self.entries = {}
        self.ruta_foto_temporal = ""
        self.search_var = tk.StringVar()
        
        self.setup_ui()
        self.actualizar_tabla_datos()

    def setup_ui(self):
        self.root.title("J.C. TRAINING GROUP - GUI/CLI")
        self.root.geometry("1320x900")
        
        hdr = ttk.Frame(self.root, bootstyle="secondary")
        hdr.pack(fill="x", pady=(0, 10))
        ttk.Label(hdr, text="J.C. TRAINING GROUP ", font=("Segoe UI", 16, "bold"), bootstyle="inverse-secondary").pack(pady=12)

        cuerpo = ttk.Frame(self.root, padding=15)
        cuerpo.pack(fill="both", expand=True)

        # en la izquierda: se basa en el uso de componentes y formulario estático
        frame_izq = ttk.LabelFrame(cuerpo, text=" Registro de Medidas Antropométricas ")
        frame_izq.pack(side="left", fill="both", expand=True, padx=(0, 10))
        FormularioAtleta.construir_formulario(frame_izq, self.campos, self.entries)

        # por la derecha: se encarga de los componente de visor y multimedia
        frame_der = ttk.LabelFrame(cuerpo, text=" Foto de Cédula de Identidad ")
        frame_der.pack(side="right", fill="y", padx=(10, 0))
        
        self.lbl_visor = VisorMultimedia.construir_visor(frame_der, self)
        VisorMultimedia.mostrar_placeholder(self.lbl_visor)

        ttk.Button(frame_der, text="Seleccionar Imagen", bootstyle="info", command=self.buscar_foto_local).pack(fill="x", pady=10, padx=15)

        # Panel de Control y el centro de controles 
        panel_b = ttk.Frame(self.root, padding=10)
        panel_b.pack(fill="x")
        InterfazBotones.construir_panel_botones(panel_b, self)

        # Panel de búsqueda y tabla de datos
        panel_baja = ttk.Frame(self.root, padding=15)
        panel_baja.pack(fill="both", expand=True)
        
        frame_busqueda = ttk.Frame(panel_baja)
        frame_busqueda.pack(fill="x", pady=(0,5))
        ttk.Label(frame_busqueda, text="Buscar Atleta: ", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Entry(frame_busqueda, textvariable=self.search_var, width=40).pack(side="left", padx=5)
        self.search_var.trace_add("write", lambda *a: self.actualizar_tabla_datos(self.search_var.get()))

        # Tabla por componente
        self.tree = TablaAtletas.construir_tabla(panel_baja)
        self.tree.bind("<<TreeviewSelect>>", self.cargar_atleta_clicado)

    def buscar_foto_local(self):
        fn = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
        if fn:
            self.ruta_foto_temporal = fn
            VisorMultimedia.renderizar(self.lbl_visor, fn)

    def ejecutar_registro(self, *args):
        datos = {c: self.entries[c].get() for c in self.campos}
        exito, msg = self.controlador.procesar_registro(datos, self.ruta_foto_temporal, self.campos)
        if exito:
            messagebox.showinfo("Operación Exitosa", f"Atleta procesado con éxito.\nID: {msg}")
            self.limpiar_formulario()
            self.actualizar_tabla_datos()
        else:
            messagebox.showerror("Error de Datos", msg)

    def cargar_atleta_clicado(self, _):
        sel = self.tree.selection()
        if not sel: return
        id_c = self.tree.item(sel[0])["values"][0]
        atleta = self.controlador.filtrar_atletas("").get(id_c, {})
        
        for c in self.campos:
            self.entries[c].delete(0, tk.END)
            self.entries[c].insert(0, atleta.get(c, ""))
            
        foto = atleta.get("foto_cedula")
        if foto:
            VisorMultimedia.renderizar(self.lbl_visor, os.path.join(self.controlador.config.img_dir, foto))
        else:
            VisorMultimedia.mostrar_placeholder(self.lbl_visor)

    def ejecutar_borrado(self, *args):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Atención", "Seleccione un atleta de la lista para eliminar.")
        id_c = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar Acción", f"¿Estás seguro de eliminar permanentemente el registro de '{id_c}'?"):
            if self.controlador.ejecutar_borrado(id_c):
                messagebox.showinfo("Éxito", "Atleta borrado de la base de datos.")
                self.limpiar_formulario()
                self.actualizar_tabla_datos()

    def abrir_ventana_historial(self, *args):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Atención", "Seleccione un atleta de la tabla para examinar su historial.")
        id_c = self.tree.item(sel[0])["values"][0]
        
        v = ttk.Toplevel(self.root)
        v.title(f"Línea de Tiempo de Evolución Física - {id_c}")
        v.geometry("900x400")
        
        columnas = ("Fecha", "Peso", "Cintura", "Brazo", "Pecho", "Gluteos", "Pierna", "Pago")
        tree_h = ttk.Treeview(v, columns=columnas, show="headings")
        for col in columnas:
            tree_h.heading(col, text=col)
            tree_h.column(col, anchor="center", width=110)
        tree_h.pack(fill="both", expand=True, padding=10)
        
        for r in reversed(self.controlador.obtener_historial_atleta(id_c)):
            tree_h.insert("", "end", values=(
                r.get("Fecha_Sistema",""), r.get("Peso (kg)",""), r.get("Cintura (cm)",""), 
                r.get("Brazo (cm)",""), r.get("Pecho (cm)",""), r.get("Gluteos (cm)",""),
                r.get("Pierna (cm)",""), r.get("Ultimo Pago (DD/MM/AAAA)","")
            ))

    def ejecutar_respaldo(self, *args):
        dst = filedialog.askdirectory(title="Ubicación para Copia de Seguridad")
        if dst:
            try:
                zip_res = self.controlador.empaquetar_respaldo_sistema(dst)
                messagebox.showinfo("Copia de Seguridad", f"Respaldo ZIP generado en:\n{zip_res}")
            except Exception as e:
                messagebox.showerror("Error de Respaldo", str(e))

    def limpiar_formulario(self, *args):
        for ent in self.entries.values(): ent.delete(0, tk.END)
        VisorMultimedia.mostrar_placeholder(self.lbl_visor)
        self.ruta_foto_temporal = ""

    def actualizar_tabla_datos(self, filtro=""):
        for item in self.tree.get_children(): self.tree.delete(item)
        for k, v in self.controlador.filtrar_atletas(filtro).items():
            self.tree.insert("", "end", values=(k, v.get("Nombre",""), v.get("Apellido",""), v.get("Fecha de Ingreso",""), v.get("Ultimo Pago (DD/MM/AAAA)","")))

    def solicitar_salida(self, *args):
        if messagebox.askyesno("Salir del Sistema", "¿Deseas cerrar la aplicación de J.C. Training Group?"): 
            self.root.destroy()