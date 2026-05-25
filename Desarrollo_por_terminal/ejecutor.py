# J.C. TRAINING GROUP - Gestión Pro (Terminal)
# Lanzador Oficial del Sistema en Consola.

from app import GymApp

if __name__ == "__main__":
    # Inicializa la aplicación sin entorno gráfico e inicia el bucle del menú
    sistema = GymApp()
    sistema.menu_principal()