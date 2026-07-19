---
title: Cloudinary — Gestión de imágenes
tags: [cloudinary, imagenes, webp, cdn, almacenamiento]
type: note
created: 2026-07-16
updated: 2026-07-16
status: evergreen
related: ["[[arquitectura]]", "[[flask-backend]]"]
summary: Cómo se suben, convierten y sirven las fotos en WebP desde Cloudinary.
---

# ☁️ Cloudinary — Gestión de imágenes

## ¿Por qué Cloudinary?

Render.com tiene **almacenamiento efímero**: si el servidor se reinicia, los archivos subidos directamente se borran. Cloudinary guarda las fotos en la nube de forma permanente.

Plan gratuito: **25 GB de storage + 25 GB de bandwidth/mes**.

---

## Configuración

La credencial se guarda en `.env` (nunca en el código):
```
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Cloudinary la lee automáticamente al importar la librería — no hay que configurar nada más.

---

## Dos formas de tener fotos en WebP

### Forma 1 — Upload directo como WebP (panel Admin)
Cuando se sube una foto desde `/admin`:
```python
resultado = cloudinary.uploader.upload(file_bytes, format='webp', quality='auto')
```
- El archivo se guarda físicamente como WebP en Cloudinary.
- Ocupa menos espacio en storage.
- URL resultante: `https://res.cloudinary.com/yskbxdm4/image/upload/v.../nombre.webp`

### Forma 2 — Transformación al vuelo (Casa Llanogrande)
Las 19 fotos se subieron como JPEG y se sirven con esta URL:
```
https://res.cloudinary.com/yskbxdm4/image/upload/f_webp,q_auto/public_id.jpg
```
- `f_webp` = servir como WebP aunque esté guardado como JPEG.
- `q_auto` = calidad automática (Cloudinary elige el balance óptimo).
- El storage guarda JPEG (más pesado), pero el navegador recibe WebP (más liviano).

---

## Parámetros de subida usados

| Parámetro | Valor | Efecto |
|---|---|---|
| `format` | `'webp'` | Guarda el archivo como WebP |
| `quality` | `'auto'` | Cloudinary optimiza la calidad automáticamente |

---

## Capacidad y escalabilidad

Con 25 GB gratuitos y fotos a ~200–500 KB por imagen WebP:
- Se pueden almacenar entre **50.000 y 125.000 fotos** aproximadamente.
- Para este proyecto (catálogo de propiedades con pocas decenas de listados), el plan gratuito es más que suficiente.

---

## Acceder a Cloudinary

- Dashboard: https://console.cloudinary.com
- Media Library: para ver, borrar y organizar las fotos subidas
- API Keys: en Settings → API Keys (donde está el `CLOUDINARY_URL`)

→ [[arquitectura]] | [[flask-backend]] | [[Home]]
