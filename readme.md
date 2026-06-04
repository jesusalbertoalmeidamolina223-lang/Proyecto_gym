# SISTEMA DE GESTIÓN: J.C. TRAINING GROUP

## REQUISITOS TÉCNICOS PARA EL FUNCIONAMIENTO

### 1. QUÉ NECESITA PARA SU EJECUCIÓN
* Python 3.7 o superior instalado.
* Acceso de escritura en la carpeta del proyecto (para crear la DB y carpetas).

### 2. REQUISITOS ADICIONALES (Instalar vía terminal/CMD)
* `pip install ttkbootstrap` (Interfaz gráfica moderna y temas oscuros).
* `pip install Pillow` (Procesamiento y visualización de fotos).

---

### 3. ESTRUCTURA INTERNA DEL SISTEMA

**A. LÓGICA DE NEGOCIO (Ubicados en la carpeta `core_logic`):**

* `__init__.py` -> Archivo de inicialización del paquete y exportación limpia de clases.

* `base_datos.py` -> Motor de lectura/escritura JSON de `clientes_gym.json`.

* `motor_atletas.py` -> Lógica de negocio (registro, borrado, filtrado, historial y respaldos).

* `validador.py` -> Validación estricta de campos obligatorios y tipos numéricos.


**B. COMPONENTES DE LA INTERFAZ (Ubicados en la carpeta `gui_components`):**

* `__init__.py` -> Archivo de inicialización del paquete para la importación modular de la UI.

* `botones.py` -> Construcción y asignación de funciones del panel de control de botones.

* `formulario.py` -> Maquetación visual y distribución geométrica del formulario de datos.

* `tabla.py` -> Estructura y configuración del control visual para el listado de atletas.

* `visor_fotos.py` -> Área de renderizado e integración visual para las fotografías de los atletas.


**C. DOCUMENTACIÓN DE INTELIGENCIA ARTIFICIAL (Ubicados en la carpeta `IA`):**

* `razonamiento.txt` -> Registro técnico explicativo del diagnóstico, desacoplamiento modular del sistema (GUI/CLI/LOGIC) y resúmenes del uso de la IA en la reestructuración del software.

---

### 4. ARCHIVOS RAÍZ (Ubicados por fuera de las carpetas en el directorio principal)

* `ejecutor-gui.py` -> **ARCHIVO PRINCIPAL GUI.** Inicializa la ventana con el tema visual oscuro y lanza la aplicación de escritorio.

* `ejecutor_cli.py` -> Interfaz alternativa por terminal de comandos (CLI) para gestionar atletas, registros y respaldos sin entorno gráfico.

* `app.py` -> Ensamblaje maestro de la interfaz gráfica (UI), conectando los componentes visuales con el motor de lógica.

* `configuracion.py` -> Rutas dinámicas del sistema, detección del entorno de ejecución y creación automática de carpetas indispensables.

* `estilos.py` -> Definición de la paleta de campos maestros y métricas antropométricas del atleta.

* `readme.md` -> Manual técnico de requisitos, dependencias de ejecución e instrucciones iniciales de despliegue.

---

### 5. INICIO AUTOMÁTICO DE LA APLICACIÓN

Al ejecutar `ejecutor-gui.py` o `ejecutor_cli.py`, el sistema preparará el entorno de manera autónoma y creará automáticamente:

* `cedulas` -> Carpeta destinada al almacenamiento local de las fotos de los atletas.

* `historiales` -> Carpeta interna para los archivos JSON individuales que guardan la evolución física.

* `clientes_gym.json` -> Archivo central estructurado como la base de datos principal de la aplicación.