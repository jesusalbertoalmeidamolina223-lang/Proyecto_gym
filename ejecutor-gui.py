import ttkbootstrap as ttk
from app import GymApp

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = GymApp(root)
    root.mainloop()