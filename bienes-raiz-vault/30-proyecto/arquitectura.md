---
title: Arquitectura del proyecto
tags: [stack, flask, python, bootstrap, cloudinary, sqlite, render]
type: note
created: 2026-07-16
updated: 2026-07-16
status: evergreen
related: ["[[flask-backend]]", "[[cloudinary]]", "[[github-render]]"]
summary: Stack completo del proyecto — qué herramienta hace qué.
---

# 🏗️ Arquitectura del Proyecto

## Stack completo

| Capa | Tecnología | Para qué sirve |
|---|---|---|
| Backend | **Python 3 + Flask** | Servidor web, rutas, lógica de negocio |
| Base de datos | **SQLite** (archivo `.db`) | Almacenar propiedades localmente |
| Imágenes | **Cloudinary** | Subir, convertir a WebP y servir fotos |
| Frontend | **Bootstrap 5.3 + Jinja2** | HTML responsivo, componentes UI |
| CSS propio | `static/css/estilo.css` | Estilos personalizados, modo oscuro, animaciones |
| Despliegue | **Render.com** | Servidor en la nube (gratuito) |
| Control de versiones | **GitHub** | Repositorio + auto-deploy a Render |

---

## Flujo de una visita al sitio

```
Usuario abre el navegador
        ↓
Render recibe la petición HTTP
        ↓
Gunicorn (servidor WSGI) la pasa a Flask
        ↓
Flask ejecuta la función de la ruta (ej: inicio())
        ↓
Flask consulta SQLite y arma el contexto de datos
        ↓
Jinja2 rellena el template HTML con esos datos
        ↓
El HTML llega al navegador del usuario
        ↓
Bootstrap + CSS hacen que se vea bien
        ↓
Las fotos se cargan desde Cloudinary (CDN)
```

---

## Flujo de subida de una foto

```
Admin sube foto en /admin
        ↓
Flask captura el archivo con request.files.getlist('imagenes')
        ↓
Lee los bytes: file_bytes = archivo.read()
        ↓
Sube a Cloudinary: cloudinary.uploader.upload(file_bytes, format='webp', quality='auto')
        ↓
Cloudinary devuelve una URL segura (HTTPS)
        ↓
Flask guarda la URL en SQLite como JSON: '["https://res.cloudinary.com/..."]'
        ↓
La tarjeta en la vitrina carga la imagen desde esa URL
```

---

## Archivos principales

```
bienes raiz/
├── app.py                  ← Motor principal (rutas, lógica, BD)
├── requirements.txt        ← Dependencias Python
├── .env                    ← Credenciales (NUNCA al repo)
├── .gitignore              ← Excluye .env y *.db de git
├── bienes_raiz.db          ← Base de datos SQLite (solo local)
├── templates/
│   ├── index.html          ← Vitrina pública (home + catálogos)
│   ├── admin.html          ← Panel para agregar propiedades
│   └── propiedad.html      ← Página individual por propiedad
└── static/
    ├── css/estilo.css      ← Estilos propios
    └── img/                ← Imágenes locales (logo, portadas)
```

---

## Por qué estas tecnologías

- **Flask** sobre Django: más simple para aprender, menos "magia" oculta.
- **SQLite** sobre PostgreSQL: sin configurar servidor, perfecto para aprender. Migrar a PostgreSQL cuando se despliegue en producción real.
- **Cloudinary** sobre subir al servidor: las fotos sobreviven aunque Render reinicie el servidor (Render tiene almacenamiento efímero).
- **Bootstrap** sobre CSS puro: componentes listos (carrusel, modal, grid responsivo) sin escribir CSS desde cero.

→ [[proyecto-moc]] | [[Home]]
