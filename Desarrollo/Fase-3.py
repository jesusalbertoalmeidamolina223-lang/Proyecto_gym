# Fase 3: Logica de registro de Clientes(CRUD)
# En esta fase el programa cobra vida. Implementamos las funciones para Crear, Leer y Actualizar datos en el archivo JSON.
def cargar_datos(self):
        try:
            with open(self.db_file, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}

def guardar_datos(self, datos):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

def registrar(self):
        nombre = self.entries['Nombre'].get().strip()
        apellido = self.entries['Apellido'].get().strip()
        if not nombre or not apellido:
            messagebox.showwarning("Faltan datos", "Nombre y Apellido son obligatorios.")
            return

        id_c = f"{nombre.lower()}_{apellido.lower()}".replace(" ", "")
        d = self.cargar_datos()
        
        # Procesar foto y guardar
        nombre_foto = self.gestionar_copiado_foto(id_c)
        datos = {c: self.entries[c].get() for c in self.campos}
        datos["foto_cedula"] = nombre_foto if nombre_foto else (d.get(id_c, {}).get("foto_cedula"))
        
        # Guardado en base de datos y refresco de tabla
        d[id_c] = datos
        self.guardar_datos(d)
        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")