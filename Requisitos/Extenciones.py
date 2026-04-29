# SISTEMA DE GESTION: J.C. TRAINING GROUP
# REQUISITOS TECNICOS PARA EL FUNCIONAMIENTO:

# 1. QUE NECESITA PARA EJECUCION:
#    - Python 3.7 o superior instalado.
#    - Acceso de escritura en la carpeta del proyecto (para crear la DB y carpetas).

# 2. REQUISITOS EXTERNOS (Instalar vía terminal/CMD):
#    - pip install ttkbootstrap (Interfaz grAfica moderna y temas oscuros).
#    - pip install Pillow       (Procesamiento y visualización de fotos).

# 3. ESTRUCTURA DE ARCHIVOS (Deben ubicarse en la misma carpeta):
#    - ejecutor.py      -> ARCHIVO PRINCIPAL.
#    - app.py           -> Ensamblaje de la interfaz (UI).
#    - botones.py       -> Definición del panel de control.
#    - busqueda.py      -> Logica de multimedia y filtros de tabla.
#    - configuracion.py -> Rutas del sistema y paleta de colores.
#    - controlador.py   -> Logica de negocio (registro, borrado, carga).
#    - crud.py          -> Motor de lectura/escritura JSON y validaciones.
#    - estilos.py       -> Definicion de campos y personalizacion visual.
#    - respaldos.py     -> Gestion de historial de progreso y copias de seguridad.

# 4. INICIO AUTOMATICO DE LA APLICACION:
#    Al ejecutar 'ejecutor.py', el sistema creara automaticamente:
#    - cedulas     (Carpeta para fotos de atletas).
#    - historiales (Carpeta para archivos JSON individuales de progreso).
#    - clientes_gym.json (Base de datos principal).
