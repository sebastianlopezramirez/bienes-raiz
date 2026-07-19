---
title: Flask Backend — app.py
tags: [flask, python, rutas, jinja2, sqlite]
type: note
created: 2026-07-16
updated: 2026-07-16
status: evergreen
related: ["[[arquitectura]]", "[[base-de-datos]]"]
summary: Todas las rutas de Flask, la función de inicialización y patrones de Python usados.
---

# 🐍 Flask Backend — `app.py`

## Importaciones y configuración inicial

```python
from flask import Flask, render_template, request, redirect
import sqlite3, os, json
from dotenv import load_dotenv
load_dotenv()                   # Lee el archivo .env y carga CLOUDINARY_URL
import cloudinary, cloudinary.uploader

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # Ruta de la carpeta del proyecto
DB_PATH  = os.path.join(BASE_DIR, 'bienes_raiz.db')     # Ruta completa a la BD
```

---

## Patrón de inicialización de la BD

```python
def inicializar_tabla():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS propiedades (...)')
    # Migración sin borrar datos:
    try:
        cursor.execute("ALTER TABLE propiedades ADD COLUMN nueva_columna TEXT DEFAULT ''")
    except:
        pass   # Ya existía → ignorar el error
    conn.commit()
    conn.close()

inicializar_tabla()   # Se ejecuta al arrancar la app
```

**Lección clave:** `CREATE TABLE IF NOT EXISTS` + `try/except ALTER TABLE` permite agregar columnas nuevas sin borrar los datos existentes.

---

## Filtro Jinja2 — formato_precio

```python
@app.template_filter('formato_precio')
def formato_precio(valor):
    return '$' + '{:,}'.format(int(valor)).replace(',', '.')
# 1700000000 → $1.700.000.000
```

Se usa en el HTML así: `{{ propiedad['precio'] | formato_precio }}`

---

## Rutas disponibles

### `GET /` — Vitrina pública

- Sin `?filtro`: muestra las 3 tarjetas de categoría (Lotes, Casas, Vehículos).
- Con `?filtro=Casa`: muestra el catálogo con filtros dinámicos.

Parámetros de URL que acepta:
| Parámetro | Ejemplo | Descripción |
|---|---|---|
| `filtro` | `Casa` | Categoría principal |
| `departamento` | `Antioquia` | Filtro por departamento |
| `municipio` | `Rionegro` | Filtro por municipio |
| `precio_max` | `500000000` | Precio máximo |
| `marca` | `Toyota` | Solo para vehículos |

### `GET/POST /admin` — Panel de administración

- `GET`: muestra el formulario vacío.
- `POST`: procesa el formulario, sube fotos a Cloudinary, inserta en BD, redirige a `/`.

Patrón crítico para subir fotos:
```python
archivos = request.files.getlist('imagenes')   # Lista de archivos
for archivo in archivos:
    file_bytes = archivo.read()                 # LEER BYTES primero (si no, llega vacío)
    resultado  = cloudinary.uploader.upload(file_bytes, format='webp', quality='auto')
    urls.append(resultado['secure_url'])
imagen_url = json.dumps(urls)                  # Guardar como JSON en la BD
```

### `GET /propiedad/<int:id>` — Página individual

Permite compartir un link directo a una propiedad.  
Ejemplo: `https://tusitio.com/propiedad/5`

```python
@app.route('/propiedad/<int:id>')
def ver_propiedad(id):
    cursor.execute("SELECT * FROM propiedades WHERE id = ?", (id,))
    # Si no existe → redirect('/')
    # Si existe → render_template('propiedad.html', propiedad=p)
```

---

## Patrón JSON para múltiples imágenes

Las fotos se guardan en el campo `imagen_url` de la BD como texto JSON:
```
'["https://cloudinary.com/foto1.webp", "https://cloudinary.com/foto2.webp"]'
```

Al leer:
```python
p['imagenes'] = json.loads(p['imagen_url'])   # texto JSON → lista Python
```

En el HTML, Jinja2 itera la lista:
```html
{% for img in propiedad['imagenes'] %}
    <img src="{{ img }}">
{% endfor %}
```

→ [[base-de-datos]] | [[arquitectura]] | [[Home]]
