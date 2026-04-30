# J.C. TRAINING GROUP - Sistema de Gestion de Atletas
# Gestion multimedia y motor de busqueda.
# Usa Pillow para que las fotos se vean bien en el visor y no den problemas de formato.
# Se encarga de guardar las fotos en las carpetas locales usando el ID del cliente como referencia.
# El motor de busqueda: muestra los resultados al momento segun lo que el usuario escriba.
from crud import *

class BusquedaMedia(CrudBase):
    def seleccionar_foto_cedula(self):
        filename = filedialog.askopenfilename(filetypes=[('Imágenes', '*.jpg *.jpeg *.png')])
        if filename:
            self.ruta_foto_temporal = filename
            self.lbl_status_foto.config(text="Foto vinculada", foreground=self.color_accent)
            self.visualizar_imagen(filename)

    def visualizar_imagen(self, ruta):
        try:
            img = Image.open(ruta)
            img.thumbnail((220, 280), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.lbl_foto_visor.config(image=photo, text="")
            self.lbl_foto_visor.image = photo
        except: 
            self.mostrar_imagen_placeholder()

    def mostrar_imagen_placeholder(self):
        self.lbl_foto_visor.config(image='', text="SIN FOTO", foreground="grey")

    def gestionar_copiado_foto(self, id_cliente):
        if not self.ruta_foto_temporal or not os.path.exists(self.ruta_foto_temporal): 
            return None
        ext = os.path.splitext(self.ruta_foto_temporal)[1]
        nuevo_nombre = f"cedula_{id_cliente}{ext}"
        shutil.copy2(self.ruta_foto_temporal, os.path.join(self.img_dir, nuevo_nombre))
        return nuevo_nombre

    def actualizar_tabla(self, filtro=""):
        for i in self.tree.get_children(): self.tree.delete(i)
        d = self.cargar_datos()
        filtro = filtro.lower()
        for k, v in d.items():
            if not filtro or filtro in v.get("Nombre", "").lower() or filtro in v.get("Apellido", "").lower():
                self.tree.insert("", "end", values=(k,v.get("Nombre",""), v.get("Apellido",""), v.get("Ultimo Pago (DD/MM/AAAA)","--")))