import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class GymApp:
    def __init__(self, root):
# Configuración inicial de la ventana y carga de datos.
        self.root = root
        self.root.title("Gestión de Usuarios - Gym")
        self.root.geometry("600x750")
        
# Definición de la base de datos local (archivo JSON)
        self.archivo_datos = "datos_gym.json"
        self.datos_usuarios = self.cargar_datos()

# Inicializar la interfaz visual
        self.crear_widgets()

    def crear_widgets(self):
#Crea todos los elementos visuales (Etiquetas, Entradas, Botones).
        tk.Label(self.root, text="Registro de Clientes", font=("Arial", 16, "bold")).pack(pady=10)

# Contenedor para el formulario
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=5, fill="both")

# Diccionario para almacenar las referencias a los cuadros de texto (Entry)
        self.campos = {}
        labels = [
            "Nombre", "Apellido", "Peso (kg)", "Altura (cm)", 
            "Cadera", "Muslo", "Cintura", "Brazo", "Pecho",
            "Enfermedades", "Discapacidad"
        ]

# Bucle para crear automáticamente las etiquetas y las cajas de texto
        for i, texto in enumerate(labels):
            tk.Label(frame, text=f"{texto}:").grid(row=i, column=0, sticky="w", pady=2)
            ent = tk.Entry(frame, width=30)
            ent.grid(row=i, column=1, pady=2)
            self.campos[texto] = ent # Guardamos el objeto 'ent' para leerlo luego

# Checkbutton para el estado del pago
        tk.Label(frame, text="¿Mensualidad Pagada?").grid(row=len(labels), column=0, sticky="w", pady=5)
        self.pago_var = tk.BooleanVar() # Variable lógica (True/False)
        tk.Checkbutton(frame, variable=self.pago_var).grid(row=len(labels), column=1, sticky="w")

# Panel para los botones de acción
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

# Botones con sus respectivas funciones y colores
        tk.Button(btn_frame, text="Guardar/Actualizar", command=self.guardar_usuario, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Buscar por Nombre", command=self.buscar_usuario, bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Limpiar lista", command=self.limpiar_campos, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Eliminar Atleta", command=self.eliminar_usuario, bg="#F44336", fg="white", width=15).grid(row=1, column=1, padx=5, pady=5)

    def cargar_datos(self):
#Lee el archivo JSON. Si no existe, devuelve un diccionario vacío.
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, "r") as f:
                return json.load(f)
        return {}

    def guardar_datos(self):
#Escribe la información actual en el archivo JSON.
        with open(self.archivo_datos, "w") as f:
            json.dump(self.datos_usuarios, f, indent=4)

    def guardar_usuario(self):
#Extrae los datos de la interfaz y los guarda en el diccionario.
        nombre = self.campos["Nombre"].get().strip().lower() # Usamos el nombre como ID
        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio.")
            return

# Comprensión de diccionario para obtener el texto de cada Entry
        usuario = {k: v.get() for k, v in self.campos.items()}
        usuario["Pagado"] = self.pago_var.get()

# Guardar en memoria y luego en el archivo
        self.datos_usuarios[nombre] = usuario
        self.guardar_datos()
        messagebox.showinfo("Éxito", f"Datos de {nombre.capitalize()} guardados.")

    def buscar_usuario(self):
#Busca un usuario por nombre y rellena el formulario con su información.
        nombre = self.campos["Nombre"].get().strip().lower()
        if nombre in self.datos_usuarios:
            user = self.datos_usuarios[nombre]
# Rellenar cada cuadro de texto con el valor guardado
            for k, v in self.campos.items():
# Borrar lo que haya escrito del usuario antes de mostrar los datos guardados
                v.delete(0, tk.END) 
# Insertar el dato de la "base de datos"
                v.insert(0, user[k]) 
            self.pago_var.set(user["Pagado"])
        else:
            messagebox.showinfo("No encontrado", "No existe un registro con ese nombre.")

    def eliminar_usuario(self):
#Borra al usuario seleccionado tras una confirmacion.
        nombre = self.campos["Nombre"].get().strip().lower()
        if not nombre:
            messagebox.showwarning("Error", "Escribe el nombre del atleta que quieres eliminar.")
            return
        
        if nombre in self.datos_usuarios:
# Ventana de confirmacion para evitar borrados accidentales
            confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar a {nombre.capitalize()}?")
            if confirmar:
                del self.datos_usuarios[nombre]
                self.guardar_datos()
                self.limpiar_campos()
                messagebox.showinfo("Eliminado", f"{nombre.capitalize()} ha sido borrado.")
        else:
            messagebox.showerror("Error", "El atleta no existe.")

    def limpiar_campos(self):
#Vacia todos los campos de texto del formulario.
        for v in self.campos.values():
            v.delete(0, tk.END)
        self.pago_var.set(False)

# Punto de entrada del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()