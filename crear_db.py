
# SCRIPT DE CREACIÓN Y POBLADO DE LA BASE DE DATOS

#Importamos la librería nativa de Python para bases de datos relacionales.
import sqlite3 

def inicializar_sistema_datos():
    # Si el archivo 'database.db' no existe en la carpeta, Python lo crea mágicamente en el acto.
    conexion = sqlite3.connect('database.db')
    
    # PASO 3: Creamos el "Cursor". 
    # El cursor es como el brazo robótico que se mete a la base de datos a escribir o leer.
    cursor = conexion.cursor()

    print("Definiendo la estructura de la tabla 'propiedades'...")
    
    # PASO 4: Ejecutamos comandos SQL (Lenguaje Estructurado de Consultas).
    # Usamos TEXT para casi todo porque nos da flexibilidad absoluta (ej: precios con puntos o signos).
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS propiedades (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Un número único que Python autogestiona (1, 2, 3...)
            categoria TEXT NOT NULL CHECK(categoria IN ('Lote', 'Carro', 'Casa')), -- esto seria el ENUM
            titulo TEXT NOT NULL,                 -- El gancho comercial que leerá Google Ads
            precio TEXT NOT NULL,                 -- El valor monetario formateado para el cliente
            ubicacion TEXT NOT NULL,              -- Ubicación geográfica clave para filtros
            descripcion TEXT,                     -- Texto libre donde se guardan los datos específicos (km, m2, etc.)
            imagen_url TEXT,                      -- El nombre del archivo de la foto (ejemplo: lote1.webp)
            estado TEXT DEFAULT 'Disponible'       -- Control de inventario básico ('Disponible', 'Vendido')
        )
    ''')

    # Limpiamos datos viejos de prueba para que no se dupliquen si corres este archivo varias veces.
    cursor.execute('DELETE FROM propiedades')

    print("Inyectando activos de prueba (Lote, Carro y Casa)...")
    
    # Preparamos la lista de datos reales que simularán tu inventario.
    # Nota cómo en 'descripcion' adaptamos los detalles según la categoría.
    inventario_prueba = [
        (
            'Lote', 
            'Lote Premium en la Montaña', 
            '$135.000.000', 
            'Santa Elena, Medellín', 
            'Área: 1.800 m². Topografía: 70% plano. Cuenta con nacimiento de agua propio, energía de EPM y explanación lista para construir cabaña.', 
            'lote_montana.webp'
        ),
        (
            'Carro', 
            'Toyota Hilux 4x4 Diésel', 
            '$215.000.000', 
            'El Poblado, Medellín', 
            'Modelo: 2024. Kilometraje: 12.500 km. Caja: Automática. Cojinería en cuero, único dueño. Ideal para terrenos de montaña.', 
            'toyota_hilux.webp'
        ),
        (
            'Casa', 
            'Finca-Challet de Descanso', 
            '$450.000.000', 
            'Guarne, Antioquia', 
            'Área construida: 150 m². Habitaciones: 3. Baños: 2. Incluye zona de fogata, deck con vista al valle y parqueadero para 4 vehículos.', 
            'finca_guarne.webp'
        )
    ]

    # Insertamos los datos usando marcadores de posición '?' por seguridad (evita hackeos por inyección SQL).
    cursor.executemany('''
        INSERT INTO propiedades (categoria, titulo, precio, ubicacion, descripcion, imagen_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', inventario_prueba)

    # El "Commit". Esto es como darle al botón de 'Guardar' en Word. 
    # Si no haces commit, los datos se quedan flotando en la memoria RAM y se borran al cerrar el archivo.
    conexion.commit()
    
    # Cerramos el archivador para liberar memoria de la computadora.
    conexion.close()
    
    print("¡Base de datos 'database.db' configurada y poblada con éxito!")

# Este bloque asegura que el código solo se ejecute si le das "Play" directo a este archivo
if __name__ == '__main__':
    inicializar_sistema_datos()