import os
from core_logic.motor_atletas import ControladorAcciones
from estilos import EstilosInterfaz

def lanzar_consola():
    motor = ControladorAcciones()
    campos_maestros = EstilosInterfaz().campos
    while True:
        print("\n" + "= ="*15)
        print("    J.C. TRAINING GROUP - INTERFAZ DE CONSOLA")
        print("= ="*15)
        print("|1|. Lista / Mostrar Atletas del Gimnasio")
        print("|2|. Registrar Nuevo Atleta")
        print("|3|. Eliminar Atleta de la Base de Datos")
        print("|4|. Crear Respaldo Completo de Seguridad (.ZIP)")
        print("|5|. Cerrar Terminal de Administración")
        print("= ="*15)
        opcion = input("Seleccione una opción del 1 al 5: ").strip()
        
        if opcion == "1":
            filtro = input("\nIngrese texto para buscar (o pulse Enter para listar todos): ")
            atletas = motor.filtrar_atletas(filtro)
            print(f"\nRegistros encontrados ({len(atletas)}):")
            print("-"*60)
            
            for idx, (id_c, datos) in enumerate(atletas.items(), start=1):
                print(f" [{idx}] ID: {id_c}")
                print(f"     Nombre Completo: {datos.get('Nombre', '')} {datos.get('Apellido', '')}")
                print(f"     Fecha de Ingreso: {datos.get('Fecha de Ingreso', '--'):<15} | Último Pago: {datos.get('Ultimo Pago (DD/MM/AAAA)', '--')}")
                print("-" * 60)
                print("     MEDIDAS Y DATOS:")
                
                # Listamos las medidas de forma vertical y ordenada
                for campo in campos_maestros:
                    # Evitamos repetir Nombre, Apellido, Ingreso y Pago que ya pusimos arriba
                    if campo not in ["Nombre", "Apellido", "Fecha de Ingreso", "Ultimo Pago (DD/MM/AAAA)"]:
                        valor = datos.get(campo, '--')
                        print(f"      • {campo:<25}: {valor}")
                
                if datos.get("foto_cedula"):
                    print(f"      • Foto Cédula Archivo     : {datos.get('foto_cedula')}")
                print("= ="*15)

        elif opcion == "2":
            print("\nFormulario de Entrada de Datos")
            valores = {}
            for campo in campos_maestros:
                valores[campo] = input(f" -> {campo}: ").strip()
                
            foto_path = input(" -> Ruta de foto de cédula en disco (Opcional, Enter para omitir): ").strip()
            
            exito, resultado = motor.procesar_registro(valores, foto_path, campos_maestros)
            if exito:
                print(f"\n[EXITO] Atleta guardado de forma limpia. ID asignado: {resultado}")
            else:
                print(f"\n[ALERTA DE LÓGICA] No se pudo procesar: {resultado}")
                
        elif opcion == "3":
            id_borrar = input("\nIngrese el ID exacto del atleta que desea eliminar: ").strip()
            confirmar = input(f"¿Seguro que desea eliminar permanentemente a {id_borrar}? (s/n): ").lower().strip()
            if confirmar == 's':
                if motor.ejecutar_borrado(id_borrar):
                    print("[OK] El registro y sus archivos locales se eliminaron con éxito.")
                else:
                    print("[ERROR] El ID especificado no existe en la base de datos.")
                    
        elif opcion == "4":
            print("\n--- Sistema de Copias de Seguridad ---")
            ruta_destino = input("Ingrese la ruta absoluta de la carpeta para guardar el respaldo (ej. C:/Users/Public): ").strip()
            if os.path.exists(ruta_destino):
                try:
                    archivo_zip = motor.empaquetar_respaldo_sistema(ruta_destino)
                    print(f"[OK] Respaldo empaquetado correctamente en:\n{archivo_zip}")
                except Exception as e:
                    print(f"[ERROR] No se pudo crear el archivo: {str(e)}")
            else:
                print("[ERROR] El directorio especificado no es válido o no existe.")
                
        elif opcion == "5":
            print("\nCerrando terminal de administración de J.C. Training Group. ¡Feliz día!")
            break
        else:
            print("\n[ALERTA] Opción incorrecta. Intente de nuevo.")

if __name__ == "__main__":
    lanzar_consola()