# ==============================================================================
# ARCHIVO: app.py (EL MOTOR LOGÍCO Y PROCESADOR DE CONSULTAS)
# ==============================================================================

# Importamos Flask para crear la web, render_template para dibujar el HTML,
# y request para "atrapar" lo que el usuario escribe o selecciona en los filtros.
# Importamos las herramientas principales de Flask:
# - Flask: Para crear y levantar el servidor web.
# - render_template: Para procesar y mostrar los archivos HTML (con Jinja2).
# - request: Para capturar los filtros y datos que envía el usuario desde el navegador.
# - redirect: Para redirigir el flujo navegación hacia otras rutas si es necesario.
from flask import Flask, render_template, request, redirect

# Importamos sqlite3 para interactuar con bases de datos SQL relacionales locales.
# Importamos os para manipular rutas de archivos del sistema operativo de forma segura.
import sqlite3, os

# Inicializamos nuestra aplicación web Flask y le damos un nombre interno basado en el módulo actual.
app = Flask(__name__)

# Obtiene la ruta absoluta de la carpeta exacta donde está guardado este archivo "app.py".
# Esto evita errores si ejecutas el proyecto desde terminales en carpetas externas.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Une la ruta de la carpeta del proyecto con el nombre físico de tu base de datos ('bienes_raiz.db').
# Así, Flask siempre sabrá exactamente en qué dirección del disco duro leer o guardar los lotes, casas y carros.
DB_PATH = os.path.join(BASE_DIR, 'bienes_raiz.db')

# Definimos una función reutilizable para abrir conexión con la base de datos.
def obtener_db():
    # Se conecta físicamente al archivo 'database.db' en tu disco duro.
    conn = sqlite3.connect(DB_PATH)
    
    # Truco de Ingeniería: Transforma los resultados en un diccionario.
    # Así podemos llamarlos en el HTML como propiedad['precio'] en vez de propiedad[3].
    conn.row_factory = sqlite3.Row 
    
    # Devuelve la conexión lista para ser usada.
    return conn

# Registra el decorador de Flask para mapear las peticiones del navegador de la ruta principal ('/')
@app.route('/')
# Define la función de vista 'inicio' que se dispara de forma automática al cargar el home del sitio web
def inicio():
    # Intenta capturar el parámetro 'filtro' de la URL; si el usuario entra directo, le asigna el valor por defecto None
    filtro_actual = request.args.get('filtro', None)
    # Intenta capturar la ubicación seleccionada; si el usuario no ha tocado el filtro, se inicializa como 'Todas'
    sub_ubicacion = request.args.get('ubicacion', 'Todas')
    # Intenta capturar el precio máximo seleccionado; si no viene ningún valor en la petición URL, se define como 'Todos'
    sub_precio = request.args.get('precio_max', 'Todos')
    # Intenta capturar la marca automotriz seleccionada; si el parámetro no existe en la consulta, toma el valor 'Todas'
    sub_marca = request.args.get('marca', 'Todas')

    # Abre un flujo de conexión directo hacia el archivo local de base de datos relacional SQLite 'bienes_raiz.db'
    conn = sqlite3.connect(DB_PATH)
    # Configura la fábrica de filas para transformar las tuplas nativas de la consulta en diccionarios legibles por clave
    conn.row_factory = sqlite3.Row
    # Inicializa el cursor para interactuar con la base de datos y poder redactar comandos SQL dinámicos
    cursor = conn.cursor()

    # Ejecuta un comando DDL para estructurar la tabla propiedades de forma automática si es la primera vez que se monta la app
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propiedades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            precio INTEGER NOT NULL,
            descripcion TEXT,
            imagen_url TEXT,
            marca TEXT
        )
    ''')
    # Confirma la transacción en el motor de la base de datos para guardar la creación de la tabla en el disco duro
    conn.commit()

    # Consulta el inventario total ejecutando una cuenta rápida sobre el número de filas de la tabla propiedades
    cursor.execute("SELECT COUNT(*) FROM propiedades")
    # Condicional lógico que valida si la base de datos se encuentra completamente en blanco (conteo igual a cero)
    if cursor.fetchone()[0] == 0:
        # Crea un contenedor tipo lista con registros estructurados comercialmente para sembrar la base de datos
        datos_prueba = [
            ('Hermoso Lote de Montaña', 'Lote', 'Santa Elena, Medellín', 120000000, 'Espectacular lote con vista limpia, ideal para inversión o descanso.', 'lote1.webp', None),
            ('Finca Turística Premium', 'Casa', 'Guarne, Antioquia', 240000000, 'Casa campestre amoblada, zona de asados y acceso pavimentado.', 'casa1.webp', None),
            ('Toyota Hilux 4x4', 'Carro', 'El Poblado, Medellín', 180000000, 'Camioneta perfecta para terrenos difíciles y subir a la montaña.', 'carro1.webp', 'Toyota'),
            ('Nissan Frontier Diésel', 'Carro', 'Santa Elena, Medellín', 140000000, 'Excelente fuerza y rendimiento para transporte en la zona.', 'carro2.webp', 'Nissan')
        ]
        # Inyecta de forma masiva el inventario inicial simulando múltiples inserciones seguras parametrizadas
        cursor.executemany('''
            INSERT INTO propiedades (titulo, categoria, ubicacion, precio, descripcion, imagen_url, marca)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', datos_prueba)
        # Confirma de forma definitiva la carga masiva de los datos de prueba en el archivo físico .db
        conn.commit()

    # Inicializa una lista vacía de propiedades para que la plantilla HTML no arroje un error si no hay categoría activa
    propiedades = []
    # Inicializa el contador matemático en cero para representar el estado base inicial de la vitrina
    total = 0
    
    # Evalúa si la variable filtro_actual no es None (es decir, el usuario ya seleccionó una sección específica)
    if filtro_actual:
        # Prepara la raíz de la consulta SQL de filtrado dinámico apuntando estrictamente al tipo de categoría elegida
        query = "SELECT * FROM propiedades WHERE categoria = ?"
        # Almacena el valor de la categoría activa como el primer elemento protegido dentro de la lista de parámetros
        params = [filtro_actual]

        # Comprueba si el usuario requiere una zona geográfica específica diferente del filtro por defecto 'Todas'
        if sub_ubicacion != 'Todas':
            # Concatena el operador AND de SQL para anexar la regla de coincidencia exacta sobre la columna ubicacion
            query += " AND ubicacion = ?"
            # Agrega el valor del parámetro geográfico de forma segura al final de la lista de argumentos
            params.append(sub_ubicacion)

        # Comprueba si el usuario fijó un límite de presupuesto máximo en lugar del filtro global 'Todos'
        if sub_precio != 'Todos':
            # Concatena la restricción matemática indicando que el precio en base de datos debe ser menor o igual al filtro
            query += " AND precio <= ?"
            # Fuerza la conversión del string de la URL a un tipo numérico entero puro y lo agrega a los parámetros
            params.append(int(sub_precio))

        # Doble validación: Si la categoría seleccionada es un carro y además se especificó una marca distinta a 'Todas'
        if filtro_actual == 'Carro' and sub_marca != 'Todas':
            # Concatena la condición final a la consulta para restringir el listado por el fabricante automotor
            query += " AND marca = ?"
            # Inyecta la marca vehicular requerida dentro de la colección final de argumentos SQL
            params.append(sub_marca)

        # Ordena al cursor ejecutar la consulta armada en tiempo de ejecución de manera blindada contra inyecciones SQL
        cursor.execute(query, params)
        # Captura la colección completa de filas encontradas y las asigna formalmente a la variable propiedades
        propiedades = cursor.fetchall()
        # Calcula matemáticamente la cantidad de elementos devueltos por el motor de la base de datos
        total = len(propiedades)

    # Cierra de forma limpia la conexión de SQLite para optimizar los recursos del sistema operativo y liberar el archivo
    conn.close()

    # Retorna el renderizado HTML inyectando de forma asíncrona y segura las variables en el motor de Jinja2
    return render_template(
        # Apunta al archivo principal de la interfaz visual ubicado en el directorio de plantillas de la app
        'index.html',
        # Envía la categoría seleccionada para decidir dinámicamente si se despliega el catálogo o el menú inicial
        filtro_actual=filtro_actual,
        # Pasa el estado de la ubicación actual para mantener la opción seleccionada de forma persistente en los formularios
        sub_ubicacion=sub_ubicacion,
        # Pasa el precio máximo elegido para conservar la coherencia de los filtros tras cada actualización
        sub_precio=sub_precio,
        # Pasa el fabricante automotriz activo para conservar el estado de búsqueda en el panel select de carros
        sub_marca=sub_marca,
        # Envía el set de datos final con los inmuebles o vehículos listos para ser iterados en la cuadrícula visual
        propiedades=propiedades,
        # Pasa el número entero del conteo de resultados para alimentar las etiquetas de salida semántica en la cabecera
        total=total
    )
# Registra una nueva ruta URL ('/admin') que aceptará tanto ver el formulario (GET) como enviar los datos (POST)
@app.route('/admin', methods=['GET', 'POST'])
# Declara la función de Python encargada de la lógica del panel de control de inventario
def admin():
    # Condicional que detecta si el usuario le dio clic al botón de enviar el formulario (petición POST)
    if request.method == 'POST':
        # Captura el texto del campo 'titulo' enviado por el formulario web
        titulo = request.form.get('titulo')
        # Captura la categoría seleccionada (Lote, Casa o Carro) del formulario
        categoria = request.form.get('categoria')
        # Captura la zona geográfica o ubicación del activo comercial
        ubicacion = request.form.get('ubicacion')
        # Captura el precio y lo transforma inmediatamente en un número entero para la base de datos
        precio = int(request.form.get('precio'))
        # Captura el texto descriptivo o características adicionales ingresadas
        descripcion = request.form.get('descripcion')
        # Captura el nombre de la imagen (o asigna una por defecto si el usuario lo deja en blanco)
        imagen_url = request.form.get('imagen_url') or 'placeholder.jpg'
        # Captura la marca del vehículo (si la categoría elegida fue un Carro)
        marca = request.form.get('marca', None)

        # Abre una conexión limpia con tu base de datos física 'bienes_raiz.db'
        conn = sqlite3.connect(DB_PATH)
        # Inicializa el cursor para poder redactar y ejecutar la inserción SQL
        cursor = conn.cursor()
        
        # Ejecuta la sentencia SQL para insertar de forma segura el nuevo registro en la tabla de propiedades
        cursor.execute('''
            INSERT INTO propiedades (titulo, categoria, ubicacion, precio, descripcion, imagen_url, marca)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, categoria, ubicacion, precio, descripcion, imagen_url, marca))
        
        # Guarda y consolida permanentce los cambios y el nuevo activo en el archivo del disco duro
        conn.commit()
        # Cierra la conexión de la base de datos para liberar recursos del servidor
        conn.close()
        
        # Redirige automáticamente al usuario a la página de inicio para que vea su nuevo producto listado
        return redirect('/')

    # Si la petición es de tipo GET (el usuario solo entró a mirar la URL /admin), renderiza la plantilla limpia
    return render_template('admin.html')

# Bloque estándar de arranque: si ejecutas este archivo, enciende el servidor en modo depuración.
if __name__ == '__main__':
    app.run(debug=True)
