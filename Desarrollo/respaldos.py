# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Historial de evolucion y copias de seguridad.
# en esta parte se gestionan las graficas y la evolucion de medidas de los atletas.
# Metimos una funcion de respaldo manual para que si el usuario cambia de PC, se pueda llevar toda la base de datos sin problemas.
from busqueda import *

class HistorialRespaldos(BusquedaMedia):
    def abrir_ventana_historial(self):
        """Muestra una ventana nueva con el progreso temporal del atleta seleccionado."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atencion", "Por favor, elige a un cliente de la lista.")
            return
        
        # Sacamos los datos basicos para el titulo de la ventana
        id_cliente = self.tree.item(seleccion[0])['values'][0]
        nombre = self.tree.item(seleccion[0])['values'][1]
        
        ventana_h = ttk.Toplevel(self.root)
        ventana_h.title(f"Linea de Tiempo: {nombre}")
        ventana_h.geometry("1000x500")
        
        main_frame = ttk.Frame(ventana_h, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Definimos las columnas de la tabla de evolucion
        columnas = (
            "Fecha Registro", "Peso", "Cintura", "Brazo", 
            "Pecho", "Gluteos", "Pierna", "Ultimo Pago"
        )
        
        tree_h = ttk.Treeview(main_frame, columns=columnas, show="headings")
        for col in columnas:
            tree_h.heading(col, text=col)
            tree_h.column(col, width=110, anchor="center")
        tree_h.pack(fill="both", expand=True)
        
        # Buscamos el archivo de historial especifico de este cliente
        ruta_h = os.path.join(self.historial_dir, f"{id_cliente}.json")
        if os.path.exists(ruta_h):
            with open(ruta_h, "r", encoding="utf-8") as f:
                datos_h = json.load(f)
                # Mostramos los registros del mas nuevo al más viejo
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

    def crear_respaldo(self):
        """Generamos una copia completa de la base de datos, fotos e historiales."""
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
        destino = filedialog.askdirectory(title="¿Donde quieres guardar el respaldo?")
        
        if destino:
            # Creamos una carpeta unica con la fecha y hora actual
            folder_backup = os.path.join(destino, f"Respaldo_Gym_{fecha}")
            try:
                os.makedirs(folder_backup)
                
                # Copiamos todo: JSON principal, fotos y archivos de progreso
                shutil.copy2(self.db_file, folder_backup) 
                shutil.copytree(self.img_dir, os.path.join(folder_backup, "cedulas")) 
                shutil.copytree(self.historial_dir, os.path.join(folder_backup, "historiales")) 
                
                messagebox.showinfo("Sistema Protegido", f"Copia de seguridad creada en:\n{folder_backup}")
            except Exception as e:
                messagebox.showerror("Error de Respaldo", f"No se pudo completar la copia: {e}")