# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Cerebro Operativo (Logica de Negocio)
# Aqui se procesan los datos de los formularios y se valida la informacion antes de guardarla.
# El manejo de archivos que nos asegura de que las fotos se guarden bien y el historial no se dañe.
# Es el puente que Conecta la interfaz con el almacenamiento físico (JSON/Fotos)

from respaldos import *

class ControladorAcciones(HistorialRespaldos):
    def registrar(self):
        """Proceso para actualizar los datosde los atletas."""
        # 1. Validacion rapida de numeros
        if not self.validar_campos_numericos(): return
        
        # 2. Recoleccion de datos del formulario
        info_valores = {c: self.entries[c].get().strip() for c in self.campos}

        if not info_valores['Nombre'] or not info_valores['Apellido']:
            return messagebox.showwarning("Faltan datos", "El nombre y apellido son obligatorios.")
            
        # Generamos un ID unico basado en el nombre (sin espacios) 
        id_c = f"{info_valores['Nombre'].lower()}_{info_valores['Apellido'].lower()}".replace(" ", "")
        
        db_actual = self.cargar_datos()

        # 3. Manejo de la foto (si hay una nueva la copiamos, si no, mantenemos la anterior)
        info_valores["foto_cedula"] = self.gestionar_copiado_foto(id_c) or db_actual.get(id_c, {}).get("foto_cedula")
        
        # 4. Guardado doble: en la base general y en su historial personal
        self._actualizar_archivo_historial(id_c, info_valores)
        db_actual[id_c] = info_valores
        self.guardar_datos(db_actual)

        self._finalizar_accion("¡Atleta registrado correctamente!")

    def cargar_desde_tabla(self, _):
        """Rellena el formulario automaticamente al hacer clic en un cliente de la lista."""
        seleccion = self.tree.selection()
        if not seleccion: return
        
        id_c = self.tree.item(seleccion[0])['values'][0]
        perfil = self.cargar_datos().get(id_c, {})
        
        # Limpiamos antes de cargar los nuevos datos
        self.limpiar_campos()
        for campo, valor in perfil.items():
            if campo in self.entries:
                self.entries[campo].insert(0, valor)
        
        # Buscamos la foto si existe
        foto = perfil.get("foto_cedula")
        ruta = os.path.join(self.img_dir, foto) if foto else None
        
        if ruta and os.path.exists(ruta):
            self.visualizar_imagen(ruta)
        else:
            self.mostrar_imagen_placeholder()

    def borrar(self):
        """Elimina a un cliente y limpia sus archivos para no dejar basura en el disco."""
        item = self.tree.selection()
        if not item or not messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar este perfil?\nEsta accion no se puede deshacer."): 
            return
        
        id_c = self.tree.item(item[0])['values'][0]
        db = self.cargar_datos()
        
        # Borramos archivos fisicos (fotos e historiales) para ahorrar espacio
        for folder, ext in [(self.img_dir, db.get(id_c, {}).get("foto_cedula")), (self.historial_dir, f"{id_c}.json")]:
            if ext:
                path = os.path.join(folder, ext)
                if os.path.exists(path): os.remove(path)

        # Lo quitamos del diccionario y guardamos
        db.pop(id_c, None)
        self.guardar_datos(db)
        self._finalizar_accion("El cliente ha sido borrado del sistema.")

    def limpiar_campos(self):
        """Resetea todo el formulario a blanco."""
        [e.delete(0, tk.END) for e in self.entries.values()]
        self.ruta_foto_temporal = ""
        self.lbl_status_foto.config(text="No seleccionada", foreground="white")
        self.mostrar_imagen_placeholder()

    def _actualizar_archivo_historial(self, id_c, nuevos_datos):
        """Guarda una 'foto' del estado actual del cliente en su archivo de progreso."""
        ruta = os.path.join(self.historial_dir, f"{id_c}.json")
        historial = []
        
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f: 
                historial = json.load(f)
        
        # Añadimos la marca de tiempo del sistema
        registro = {**nuevos_datos, "Fecha_Sistema": datetime.now().strftime("%d/%m/%Y %H:%M")}
        historial.append(registro)
        
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=4, ensure_ascii=False)

    def _finalizar_accion(self, mensaje):
        """Refresca la tabla y limpia todo al terminar una tarea."""
        self.actualizar_tabla()
        self.limpiar_campos()
        messagebox.showinfo("Hecho", mensaje)

    def salir_aplicacion(self):
        """Cierre seguro del programa."""
        if messagebox.askyesno("Cerrar", "¿Deseas salir del sistema J.C. Training?"):
            self.root.destroy()