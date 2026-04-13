# Fase 4: Gestión de Multimedia y Búsqueda
# Se añadio la capacidad de procesar imágenes y la búsqueda inteligente, lo que hace que la experiencia de usuario sea mucho más fluida.
def visualizar_imagen(self, ruta):
        try:
            img = Image.open(ruta)
            img.thumbnail((220, 280), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_foto_visor.config(image=photo, text="")
            self.lbl_foto_visor.image = photo
        except:
            self.lbl_foto_visor.config(image='', text="SIN FOTO")

    # Búsqueda dinámica vinculada a la variable search_var
def filtrar_busqueda(self, *args):
        filtro = self.search_var.get().lower()
        self.actualizar_tabla(filtro)