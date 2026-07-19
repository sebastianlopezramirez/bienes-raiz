---
title: "ADR-002: Cloudinary para imágenes"
tags: [decision, cloudinary, imagenes, render, storage]
type: note
created: 2026-07-19
updated: 2026-07-19
status: evergreen
summary: Por qué guardamos las fotos en Cloudinary y no en el servidor de Render.
---

# ADR-002 — Cloudinary para imágenes

**Estado:** ✅ Decidido  
**Fecha:** Julio 2026

## Contexto
Render.com tiene **almacenamiento efímero**: cuando el servidor se reinicia, cualquier archivo subido directamente se borra. Las fotos de propiedades deben sobrevivir reinicios.

## Decisión
Usar **Cloudinary** como CDN de imágenes.

## Por qué Cloudinary
- Las fotos quedan en la nube de forma permanente
- Convierte automáticamente a WebP con `format='webp', quality='auto'`
- CDN global — las fotos cargan rápido desde cualquier país
- Plan gratuito: 25 GB storage + 25 GB bandwidth/mes
- Con 50–500 propiedades, el plan gratuito es más que suficiente

## Implementación
```python
file_bytes = archivo.read()
resultado  = cloudinary.uploader.upload(file_bytes, format='webp', quality='auto')
urls.append(resultado['secure_url'])
```

## Lección aprendida
Si se pasa el objeto archivo directo (sin `.read()`), Cloudinary recibe un stream vacío y lanza `BadRequest: Invalid image file`. Siempre leer los bytes primero.

→ [[cloudinary]] | [[Home]]
