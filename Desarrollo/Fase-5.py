# Fase 5: Historial Evolutivo y Respaldo
# Finalizamos con la seguridad y el seguimiento. Creamos archivos de historial separados para no saturar la base de datos principal y la herramienta de Backupdef(o copia de seguridad) abrir_ventana_historial(self):
seleccion = self.tree.selection()
if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista.")
            return
        
id_cliente = self.tree.item(seleccion[0])['values'][0]
        # Aquí se abre una ventana Toplevel que lee historiales/{id_cliente}.json

def crear_respaldo(self):
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
        destino = filedialog.askdirectory(title="Donde guardar el respaldo")
        if destino:
            try:
                folder_respaldo = os.path.join(destino, f"Backup_Gym_{fecha}")
                os.makedirs(folder_respaldo)
                shutil.copy2(self.db_file, folder_respaldo)
                shutil.copytree(self.img_dir, os.path.join(folder_respaldo, "cedulas"))
                shutil.copytree(self.hist_dir, os.path.join(folder_respaldo, "historiales"))
                messagebox.showinfo("Respaldo", "Copia de seguridad completada.")
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al respaldar: {e}")

# INICIO DEL PROGRAMA
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = GymApp(root)
    root.mainloop()