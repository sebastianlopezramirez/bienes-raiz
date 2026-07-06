# 🏡 Alquiler & Montaña — README Maestro

> Aplicación web para listado y gestión de propiedades y vehículos en La Estrella, Antioquia.
> **Dirección del negocio:** Cra 51 # 96 Sur 27, La Estrella
> **Contacto:** 313 792 1336 · alc@alc.com

---

## 📌 ¿Qué es este proyecto?

**Alquiler & Montaña** es una aplicación web construida en Flask que permite publicar, listar y administrar:

| Categoría | Descripción |
|-----------|-------------|
| 🏠 Casas | Propiedades en arriendo o venta |
| 🌿 Lotes | Terrenos disponibles |
| 🚗 Carros | Vehículos en venta o arriendo |

El sistema tiene una vista pública para visitantes y un panel de administración para gestionar los registros.

---

## 🛠️ Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Python + Flask | 3.x / 2.x |
| Base de datos | SQLite | 3 (vía `sqlite3` estándar) |
| Templates | Jinja2 | (incluido con Flask) |
| Frontend | HTML5 + CSS3 (vanilla) | — |
| Servidor dev | Flask built-in (`flask run`) | — |
| Editor | VS Code | — |
| Shell | PowerShell (Windows) | — |

> **Sin frameworks de JS externos.** El frontend es HTML y CSS puro.

---

## 📁 Estructura del proyecto

```
bienes raiz/
│
├── app.py                  # Núcleo de la aplicación: rutas, lógica, conexión a DB
├── bienes_raiz.db          # Base de datos SQLite (generada automáticamente)
│
├── templates/
│   ├── index.html          # Página principal pública
│   ├── admin.html          # Panel de administración
│   ├── casas.html          # Listado de casas
│   ├── lotes.html          # Listado de lotes
│   └── carros.html         # Listado de carros
│
├── static/
│   ├── css/
│   │   └── estilo.css      # Estilos globales + footer con brand colors
│   └── img/                # Imágenes de propiedades (formato .webp recomendado)
│
└── README.md               # Este archivo
```

---

## ⚙️ Cómo instalar y correr el proyecto

### Requisitos previos
- Python 3.x instalado
- pip disponible en el sistema

### Pasos

```powershell
# 1. Ir a la carpeta del proyecto
cd "D:\proyectos\bienes raiz"

# 2. (Opcional) Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar Flask
pip install flask

# 4. Correr la aplicación
python app.py
```

La app queda disponible en: **http://127.0.0.1:5000**

---

## 🗄️ Base de datos

- **Motor:** SQLite (archivo local `bienes_raiz.db`)
- **Tabla principal:** `propiedades`
- **Ruta construida con:** `os.path.abspath(__file__)` para evitar problemas de path relativo

### Esquema actual — tabla `propiedades`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INTEGER PK | Identificador único |
| `titulo` | TEXT | Nombre de la propiedad |
| `descripcion` | TEXT | Descripción detallada |
| `precio` | REAL | Precio en COP |
| `categoria` | TEXT | `casas`, `lotes` o `carros` |
| `imagen` | TEXT | Nombre del archivo en `static/img/` |

> ⚠️ El nombre en la columna `imagen` debe coincidir **exactamente** con el archivo en `static/img/`, incluyendo extensión (`.webp`, `.jpg`, etc.). Una discrepancia causa que la página se congele silenciosamente.

---

## 🎨 Diseño y estilos

- **Colores de marca:**
  - Fondo oscuro principal: `#0f172a`
  - Fondo secundario: `#1e293b`
  - Acento verde: `#059669`

- **Footer implementado** en `index.html` y `admin.html` con:
  - Logo con borde circular y efecto hover
  - Información de contacto (nombre, teléfono, email, dirección)
  - Íconos de redes sociales como SVG inline: Instagram, Facebook, TikTok

---

## ✅ Estado actual del proyecto

| Funcionalidad | Estado |
|---------------|--------|
| Listado de propiedades por categoría | ✅ Funcionando |
| Panel de administración | ✅ Funcionando |
| Base de datos SQLite conectada | ✅ Funcionando |
| Footer moderno con redes sociales | ✅ Implementado |
| Imágenes por propiedad (1 foto) | ✅ Funcionando |
| Multi-foto (hasta 10 por propiedad) | 🔲 Pendiente |
| Hosting en producción | 🔲 Pendiente |
| Autenticación en panel admin | 🔲 Pendiente |

---

## 🚧 Pendientes y roadmap

### Inmediato
- [ ] **Multi-foto:** Crear tabla `fotos` con FK a `propiedades` para soportar hasta 10 imágenes por listado
- [ ] **Autenticación:** Proteger `/admin` con usuario y contraseña

### A mediano plazo
- [ ] **Hosting:** Desplegar en **Render.com** o **PythonAnywhere** (Vercel no es compatible con Flask)
- [ ] **Búsqueda y filtros** en el listado público
- [ ] **Formulario de contacto** por propiedad

---

## ⚠️ Reglas y notas técnicas importantes

1. **Imágenes:** Siempre verificar que el nombre en DB coincida con el archivo real en `static/img/`.
2. **Jinja2:** Los operadores en templates son estrictos — `==` no puede escribirse como `= =` (con espacio).
3. **DB Path:** `app.py` usa `os.path.abspath(__file__)` para construir `DB_PATH`. Si la DB no refleja cambios, eliminarla y recrearla es el reset más confiable.
4. **PowerShell:** Los comandos del proyecto están pensados para correr en PowerShell en Windows.

---

## 🌐 Opciones de hosting evaluadas

| Plataforma | ¿Compatible con Flask? | Notas |
|------------|----------------------|-------|
| Vercel | ❌ No recomendado | Pensado para JS/static |
| Render.com | ✅ Sí | Gratis tier disponible, recomendado |
| PythonAnywhere | ✅ Sí | Fácil para Flask, buena opción para comenzar |

---

*Última actualización: Julio 2026*
*Proyecto en desarrollo activo*
