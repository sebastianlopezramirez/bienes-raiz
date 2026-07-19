---
title: Base de Datos SQLite
tags: [sqlite, base-de-datos, migracion, esquema]
type: note
created: 2026-07-16
updated: 2026-07-16
status: evergreen
related: ["[[flask-backend]]", "[[arquitectura]]"]
summary: Esquema de la tabla propiedades y patrón de migración segura.
---

# 🗄️ Base de Datos — SQLite

## Archivo

- **Nombre:** `bienes_raiz.db`
- **Ubicación:** misma carpeta que `app.py`
- **Motor:** SQLite (archivo local, sin servidor separado)
- **Importante:** está en `.gitignore` — no va al repositorio de GitHub

---

## Esquema de la tabla `propiedades`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | INTEGER PK | Identificador único, se autoincrementa |
| `titulo` | TEXT | Nombre del anuncio |
| `categoria` | TEXT | `'Lote'`, `'Casa'` o `'Carro'` |
| `departamento` | TEXT | Departamento de Colombia (default: `'Antioquia'`) |
| `municipio` | TEXT | Municipio específico |
| `ubicacion` | TEXT | Barrio, vereda o sector |
| `precio` | INTEGER | Precio en pesos colombianos (sin puntos) |
| `descripcion` | TEXT | Descripción detallada |
| `imagen_url` | TEXT | JSON con lista de URLs de Cloudinary |
| `marca` | TEXT | Solo para vehículos (Toyota, Nissan, etc.) |

---

## Patrón de migración sin borrar datos

Cuando se agrega una columna nueva, NO se borra y recrea la tabla.  
En cambio, se usa `ALTER TABLE` con `try/except`:

```python
try:
    cursor.execute("ALTER TABLE propiedades ADD COLUMN nueva_columna TEXT DEFAULT ''")
except:
    pass   # Si ya existe, SQLite lanza error → lo ignoramos
```

Esto garantiza que los datos existentes sobreviven cualquier cambio de estructura.

---

## Cómo se guardan las imágenes

El campo `imagen_url` guarda un **texto JSON** con una lista de URLs:

```
["https://res.cloudinary.com/yskbxdm4/image/upload/.../foto1.webp",
 "https://res.cloudinary.com/yskbxdm4/image/upload/.../foto2.webp"]
```

Al leer en Python: `json.loads(p['imagen_url'])` → convierte a lista Python.

---

## Consulta de ejemplo con filtros dinámicos

```python
query  = "SELECT * FROM propiedades WHERE categoria = ?"
params = ['Casa']

if municipio != 'Todos':
    query  += " AND municipio = ?"
    params.append('Rionegro')

cursor.execute(query, params)
```

Los `?` son **parámetros seguros** — evitan inyección SQL.

---

## Migración futura: SQLite → PostgreSQL

Render.com tiene almacenamiento efímero: si el servidor se reinicia, el archivo `.db` se borra. Para producción real hay que migrar a PostgreSQL:

1. Agregar `psycopg2` a `requirements.txt`
2. Cambiar `sqlite3.connect()` por conexión PostgreSQL
3. Agregar `DATABASE_URL` como variable de entorno en Render
4. Exportar datos de SQLite e importar a PostgreSQL

→ [[flask-backend]] | [[arquitectura]] | [[Home]]
