# J.C. TRAINING GROUP - Lanzador del Sistema
# Este es el archivo principal. Para iniciar la aplicacion, solo hay que ejecutar este script. 
# Se encarga de levantar la ventana, aplicar el tema visual y mantener el programa corriendo.

import ttkbootstrap as ttk
from app import GymApp

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = GymApp(root)
    root.mainloop()