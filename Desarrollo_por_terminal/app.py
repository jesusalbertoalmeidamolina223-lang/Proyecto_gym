# J.C. TRAINING GROUP - Gestión Pro (Terminal)
# Interfaz de Consola Interactiva.

import os
from estilos import Estilo
from controlador import ControladorAcciones

class GymApp:
    def __init__(self):
        self.ui_data = Estilo()
        self.controlador = ControladorAcciones()
        self.campos = self.ui_data.campos

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_banner(self, titulo=""):
        print("=" * 65)
        print("       J.C. TRAINING GROUP - Gestión Pro (Terminal)       ")
        if titulo:
            print(f" > {titulo.upper()} <<")
        print("=" * 65)

    def menu_principal(self):
        while True:
            self.limpiar_pantalla()
            self.mostrar_banner("Menú Principal")
            print(" [1] Registrar / Actualizar Atleta")
            print(" [2] Listar y Buscar Atletas")
            print(" [3] Ver Perfil Detallado")
            print(" [4] Ver Historial de Evolución")
            print(" [5] Eliminar Ficha de Atleta")
            print(" [6] Crear Respaldo de Seguridad")
            print(" [7] Salir del Sistema")
            print("-" * 65)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_atleta_ui()
            elif opcion == "2":
                self.listar_atletas_ui()
            elif opcion == "3":
                self.ver_perfil_ui()
            elif opcion == "4":
                self.ver_historial_ui()
            elif opcion == "5":
                self.borrar_atleta_ui()
            elif opcion == "6":
                self.crear_respaldo_ui()
            elif opcion == "7":
                print("\n¡Cerrando J.C. TRAINING GROUP! Hasta pronto")
                break
            else:
                input("\nOpcion invalida. Presione Enter para continuar")

    def registrar_atleta_ui(self):
        self.limpiar_pantalla()
        self.mostrar_banner("Registrar / Actualizar Atleta")
        print("Rellene los campos (Deje en blanco si está editando y desea conservar el valor actual):")
        
        info_valores = {}
        for campo in self.campos:
            info_valores[campo] = input(f" -> {campo}: ").strip()
            
        ruta_foto = input("\n Ruta de la foto de la cedula (Opcional, presione Enter para omitir): ").strip()
        
        resultado = self.controlador.procesar_registro(info_valores, ruta_foto)
        
        if resultado["status"] == "error_num":
            print(f"\n[ERROR] El campo '{resultado['campo']}' requiere valores estrictamente numericos.")
        elif resultado["status"] == "error_obligatorios":
            print("\n[ERROR] Los campos 'Nombre' y 'Apellido' son obligatorios.")
        elif resultado["status"] == "exito":
            print(f"\n[ÉXITO] Atleta procesado con ID unico: '{resultado['id']}'")
            
        input("\nPresione Enter para continuar")

    def listar_atletas_ui(self):
        self.limpiar_pantalla()
        self.mostrar_banner("Listar y Buscar Atletas")
        filtro = input("Escriba el nombre/apellido a buscar (o Enter para listar todos): ").strip()
        
        atletas = self.controlador.obtener_lista_atletas(filtro)
        print("\n" + "-" * 75)
        print(f"{'ID ÚNICO':<30} | {'NOMBRE':<15} | {'APELLIDO':<15} | {'ÚLTIMO PAGO':<12}")
        print("-" * 75)
        
        if not atletas:
            print("   No se encontraron coincidencias en los registros.")
        else:
            for k, v in atletas.items():
                print(f"{k:<30} | {v.get('Nombre', ''):<15} | {v.get('Apellido', ''):<15} | {v.get('Ultimo Pago (DD/MM/AAAA)', '--'):<12}")
        print("-" * 75)
        input("\nPresione Enter para regresar")

    def ver_perfil_ui(self):
        self.limpiar_pantalla()
        self.mostrar_banner("Ficha Detallada del Atleta")
        id_cliente = input("Ingrese el ID UNICO del atleta: ").strip()
        
        perfil = self.controlador.obtener_perfil_atleta(id_cliente)
        if not perfil:
            print("\n[ERROR] El ID ingresado no coincide con ningun registro.")
        else:
            print("\n" + "-" * 50)
            print(f" DATOS ACTUALES DEL ATLETA: {id_cliente.upper()}")
            print("-" * 50)
            for campo in self.campos:
                print(f" • {campo:<25}: {perfil.get(campo, '---')}")
            print(f" • Ubicacion de Cedula    : {perfil.get('foto_cedula', 'Ninguna')}")
            print("-" * 50)
            
        input("\nPresione Enter para regresar...")

    def ver_historial_ui(self):
        self.limpiar_pantalla()
        self.mostrar_banner("Historial de Evolucion Temporal")
        id_cliente = input("Ingrese el ID UNICO del atleta: ").strip()
        
        historial = self.controlador.obtener_historial_atleta(id_cliente)
        if not historial:
            print("\n[AVISO] No se encontraron variaciones o el atleta no existe.")
        else:
            print(f"\nRegistros históricos para: {id_cliente}\n")
            for reg in reversed(historial):
                print(f" -> Registro tomado el: {reg.get('Fecha_Sistema', '---')}")
                print(f"    Medidas -> Peso: {reg.get('Peso (kg)', '-')}kg | Cintura: {reg.get('Cintura (cm)', '-')}cm | Brazo: {reg.get('Brazo (cm)', '-')}cm")
                print(f"               Pecho: {reg.get('Pecho (cm)', '-')}cm | Glúteos: {reg.get('Gluteos (cm)', '-')}cm | Pierna: {reg.get('Pierna (cm)', '-')}cm")
                print(f"    Estado  -> Último Pago registrado: {reg.get('Ultimo Pago (DD/MM/AAAA)', '---')}")
                print("-" * 75)
                
        input("\nPresione Enter para regresar...")

    def borrar_atleta_ui(self):
        self.limpiar_pantalla()
        self.mostrar_banner("Eliminar Ficha de Atleta")
        id_c = input("Ingrese el ID UNICO a eliminar: ").strip()
        
        perfil = self.controlador.obtener_perfil_atleta(id_c)
        if not perfil:
            print("\n[ERROR] El atleta no existe.")
            input("\nPresione Enter para volver")
            return
            
        confirmar = input(f"\n¿Seguro que deseas eliminar permanentemente a {id_c}? (s/n): ").strip().lower()
        if confirmar == 's':
            self.controlador.procesar_borrado(id_c)
            print("\n[EXITO] Atleta e historial fisico borrados por completo.")
        else:
            print("\n[CANCELADO] No se realizaron modificaciones.")
            
        input("\nPresione Enter para continuar")

    def crear_respaldo_ui(self):
        self.limpiar_pantalla()
        self.mostrar_banner("Copia de Seguridad del Sistema")
        destino = input("Ingrese la ruta de la carpeta de destino para el respaldo: ").strip()
        
        if destino and os.path.exists(destino):
            try:
                folder = self.controlador.ejecutar_respaldo(destino)
                print(f"\n[EXITO] Copia de seguridad guardada en:\n -> {folder}")
            except Exception as e:
                print(f"\n[ERROR] No se pudo completar el empaquetado: {e}")
        else:
            print("\n[ERROR] La ruta especificada es inválida o no existe.")
            
        input("\nPresione Enter para continuar")