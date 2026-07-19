---
title: Lecciones aprendidas
tags: [lecciones, errores, soluciones, patrones]
type: note
created: 2026-07-19
updated: 2026-07-19
status: growing
summary: Errores que ocurrieron, por qué pasaron y cómo se resolvieron.
---

# 📚 Lecciones aprendidas

> Cada error resuelto es una lección. Aquí quedan documentados para no repetirlos.

---

## 1. Cloudinary — stream vacío

**Error:** `BadRequest: Invalid image file`  
**Causa:** Se enviaba el objeto archivo directamente a Cloudinary sin leerlo primero. El stream llegaba vacío.  
**Solución:**
```python
file_bytes = archivo.read()   # Leer los bytes PRIMERO
cloudinary.uploader.upload(file_bytes, ...)   # Luego subir
```
**Lección:** Siempre leer bytes antes de enviar a cualquier API externa.

---

## 2. Archivos .wp2 — formato no soportado

**Error:** Cloudinary, ffmpeg, Pillow e ImageMagick rechazaban los archivos `.wp2`  
**Causa:** WebP2 es un formato experimental, no compatible con casi ninguna herramienta  
**Solución:** Convertir manualmente desde el panel de Cloudinary o usando otra herramienta externa  
**Lección:** Verificar compatibilidad de formatos antes de elegirlos

---

## 3. SQLite bloqueada por el servidor Flask

**Error:** `disk I/O error` al intentar insertar datos con un script Python mientras Flask corría  
**Causa:** Flask tenía la BD bloqueada con su conexión activa  
**Solución:** Detener Flask primero, ejecutar el script, volver a iniciar Flask  
**Lección:** SQLite solo permite una escritura a la vez — no correr scripts mientras el servidor está activo

---

## 4. Llave extra `}` en el CSS

**Error:** Estilos que fallaban sin razón aparente  
**Causa:** Una llave de cierre `}` extra al final del bloque `.btn-whatsapp-nav:hover`  
**Solución:** Eliminar el `}` sobrante  
**Lección:** Un solo carácter mal puesto puede romper todo el CSS que viene después. Revisar llaves siempre que algo falle sin razón.

---

## 5. git index.lock desde el sandbox

**Error:** `fatal: Unable to create '.git/index.lock': File exists`  
**Causa:** El sandbox de Claude no tiene permisos para escribir en los archivos internos de git  
**Solución:** Ejecutar `git add`, `git commit` y `git push` desde la terminal local de Windows  
**Lección:** Los comandos git siempre deben correrse desde la terminal local, no desde Claude.

---

## 6. Variables de entorno en Render

**Error:** Las fotos no se suben / el login no funciona en producción  
**Causa:** Las variables del `.env` no están configuradas en Render — el `.env` no va al repositorio  
**Solución:** Ir a Render → tu servicio → Environment → agregar `CLOUDINARY_URL`, `SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASS`  
**Lección:** Cada variable del `.env` debe configurarse manualmente en el servidor de producción.

---

→ [[estado-actual]] | [[Home]]
