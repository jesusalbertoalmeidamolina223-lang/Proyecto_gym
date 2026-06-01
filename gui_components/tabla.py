import ttkbootstrap as ttk

class TablaAtletas:
    @staticmethod
    def construir_tabla(contenedor):
        """Construye y configura el control Treeview de la parte inferior."""
        columnas = ("ID", "Nombre", "Apellido", "Ingreso", "Pago")
        tree = ttk.Treeview(contenedor, columns=columnas, show="headings", height=7)
        
        titulos = [("ID", "ID Atleta"), ("Nombre", "Nombre"), ("Apellido", "Apellido"), ("Ingreso", "Fecha Ingreso"), ("Pago", "Último Pago")]
        for col, txt in titulos:
            tree.heading(col, text=txt)
            tree.column(col, anchor="center")
            
        tree.pack(fill="both", expand=True)
        return tree