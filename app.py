# ==============================================================================
# ARCHIVO: app.py (EL MOTOR LÓGICO Y PROCESADOR DE CONSULTAS)
# ==============================================================================

# Importamos las herramientas principales de Flask:
# - Flask: Para crear y levantar el servidor web.
# - render_template: Para procesar y mostrar los archivos HTML (con Jinja2).
# - request: Para capturar los filtros y datos que envía el usuario desde el navegador.
# - redirect: Para redirigir el flujo de navegación hacia otras rutas si es necesario.
from flask import Flask, render_template, request, redirect

# Importamos sqlite3 para interactuar con bases de datos SQL relacionales locales.
# Importamos os para manipular rutas de archivos del sistema operativo de forma segura.
import sqlite3, os, json

# load_dotenv lee el archivo .env y carga las variables de entorno (CLOUDINARY_URL, etc.)
# Esto permite que las credenciales no estén escritas directamente en el código.
from dotenv import load_dotenv
load_dotenv()

# Importamos la librería de Cloudinary para subir imágenes a la nube.
# cloudinary.uploader es el módulo que ejecuta la subida física del archivo.
import cloudinary
import cloudinary.uploader
# Cloudinary lee automáticamente CLOUDINARY_URL del entorno — no hay que configurar nada más.

# Inicializamos nuestra aplicación web Flask.
app = Flask(__name__)

# Obtiene la ruta absoluta de la carpeta donde está guardado este archivo "app.py".
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Une la ruta del proyecto con el nombre físico de la base de datos.
DB_PATH = os.path.join(BASE_DIR, 'bienes_raiz.db')


# ==============================================================================
# FUNCIÓN: inicializar_tabla()
# Crea la tabla si no existe y agrega columnas nuevas si hacen falta.
# Esto permite evolucionar la base de datos sin borrar los datos existentes.
# ==============================================================================
def inicializar_tabla():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crea la tabla con todos los campos desde el inicio si no existe.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propiedades (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo       TEXT NOT NULL,
            categoria    TEXT NOT NULL,
            departamento TEXT DEFAULT 'Antioquia',
            municipio    TEXT DEFAULT '',
            ubicacion    TEXT NOT NULL,
            precio       INTEGER NOT NULL,
            descripcion  TEXT,
            imagen_url   TEXT,
            marca        TEXT
        )
    ''')

    # MIGRACIÓN: Si la tabla ya existía sin las columnas nuevas,
    # las agregamos sin borrar los datos. El bloque try/except evita
    # el error "duplicate column name" si ya fueron agregadas antes.
    try:
        cursor.execute("ALTER TABLE propiedades ADD COLUMN departamento TEXT DEFAULT 'Antioquia'")
    except:
        pass  # La columna ya existe — no hay problema.

    try:
        cursor.execute("ALTER TABLE propiedades ADD COLUMN municipio TEXT DEFAULT ''")
    except:
        pass  # La columna ya existe — no hay problema.

    conn.commit()
    conn.close()


# Ejecutamos la inicialización una sola vez al arrancar la aplicación.
inicializar_tabla()


# ==============================================================================
# FILTRO JINJA2: formato_precio
# Convierte 1700000000 → $1.700.000.000
# Se usa en el HTML como: {{ propiedad['precio'] | formato_precio }}
# ==============================================================================
@app.template_filter('formato_precio')
def formato_precio(valor):
    # '{:,}'.format() agrega comas cada 3 dígitos → 1,700,000,000
    # .replace(',', '.') cambia comas por puntos → 1.700.000.000
    return '$' + '{:,}'.format(int(valor)).replace(',', '.')


# ==============================================================================
# RUTA: / (Página principal — vitrina pública)
# ==============================================================================
@app.route('/')
def inicio():
    # Capturamos todos los parámetros de filtro que puede enviar el usuario por URL.
    filtro_actual    = request.args.get('filtro', None)
    sub_departamento = request.args.get('departamento', 'Todos')
    sub_municipio    = request.args.get('municipio', 'Todos')
    sub_precio       = request.args.get('precio_max', 'Todos')
    sub_marca        = request.args.get('marca', 'Todas')

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    propiedades = []
    total       = 0

    if filtro_actual:
        # Construimos la consulta SQL de forma dinámica según los filtros activos.
        # Empezamos siempre filtrando por la categoría principal.
        query  = "SELECT * FROM propiedades WHERE categoria = ?"
        params = [filtro_actual]

        # Filtro por departamento (ej: "Antioquia")
        if sub_departamento != 'Todos':
            query += " AND departamento = ?"
            params.append(sub_departamento)

        # Filtro por municipio (ej: "Medellín", "Guarne")
        if sub_municipio != 'Todos':
            query += " AND municipio = ?"
            params.append(sub_municipio)

        # Filtro por precio máximo
        if sub_precio != 'Todos':
            query += " AND precio <= ?"
            params.append(int(sub_precio))

        # Filtro por marca (solo aplica a vehículos)
        if filtro_actual == 'Carro' and sub_marca != 'Todas':
            query += " AND marca = ?"
            params.append(sub_marca)

        cursor.execute(query, params)
        filas = cursor.fetchall()
        total = len(filas)

        # Convertimos cada fila a diccionario y parseamos imagen_url de JSON a lista.
        # Esto permite que el HTML itere las fotos con un bucle {% for %}.
        propiedades = []
        for fila in filas:
            p = dict(fila)
            try:
                # json.loads convierte el texto JSON → lista Python.
                imagenes = json.loads(p['imagen_url'])
                # Si por algún motivo no es lista (datos viejos), lo envolvemos en una.
                p['imagenes'] = imagenes if isinstance(imagenes, list) else [p['imagen_url']]
            except:
                # Si el valor no es JSON válido (datos de prueba viejos), lo usamos directo.
                p['imagenes'] = [p['imagen_url']]
            propiedades.append(p)

    # Consultamos los municipios únicos que tienen propiedades en la BD
    # para construir el filtro dinámico en la vista.
    cursor.execute("SELECT DISTINCT municipio FROM propiedades WHERE municipio != '' ORDER BY municipio")
    municipios_disponibles = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template(
        'index.html',
        filtro_actual         = filtro_actual,
        sub_departamento      = sub_departamento,
        sub_municipio         = sub_municipio,
        sub_precio            = sub_precio,
        sub_marca             = sub_marca,
        propiedades           = propiedades,
        total                 = total,
        municipios_disponibles = municipios_disponibles,
    )


# ==============================================================================
# RUTA: /admin (Panel de administración — agregar propiedades)
# ==============================================================================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Capturamos cada campo del formulario HTML.
        titulo       = request.form.get('titulo')
        categoria    = request.form.get('categoria')
        departamento = request.form.get('departamento', 'Antioquia')
        municipio    = request.form.get('municipio')
        ubicacion    = request.form.get('ubicacion')
        precio       = int(request.form.get('precio'))
        descripcion  = request.form.get('descripcion')
        marca        = request.form.get('marca', None)

        # Subida de MÚLTIPLES imágenes a Cloudinary.
        # getlist() captura todos los archivos enviados bajo el mismo nombre de campo.
        archivos = request.files.getlist('imagenes')
        urls = []

        # Iteramos cada archivo seleccionado por el usuario.
        for archivo in archivos:
            if archivo and archivo.filename != '':
                # CLAVE: leemos los bytes completos en memoria antes de enviar a Cloudinary.
                # Sin este paso, el stream llega vacío y genera el error "Invalid image file".
                file_bytes = archivo.read()
                if file_bytes:
                    # Enviamos los bytes. Cloudinary los convierte a WebP automáticamente.
                    resultado = cloudinary.uploader.upload(file_bytes, format='webp', quality='auto')
                    urls.append(resultado['secure_url'])

        # Si no subió ninguna foto, usamos un placeholder por defecto.
        # json.dumps convierte la lista Python → texto JSON para guardar en la BD.
        # Ejemplo: ["https://cloudinary.com/foto1.jpg", "https://cloudinary.com/foto2.jpg"]
        imagen_url = json.dumps(urls) if urls else json.dumps(['placeholder.jpg'])

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO propiedades
                (titulo, categoria, departamento, municipio, ubicacion, precio, descripcion, imagen_url, marca)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, categoria, departamento, municipio, ubicacion, precio, descripcion, imagen_url, marca))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('admin.html')


# Bloque estándar de arranque en modo desarrollo.
if __name__ == '__main__':
    app.run(debug=True)
