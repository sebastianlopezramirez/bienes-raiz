---
title: Estado actual del proyecto
tags: [estado, hoja-de-ruta, pendiente, completado]
type: note
created: 2026-07-16
updated: 2026-07-16
status: growing
related: ["[[funcionalidades]]", "[[github-render]]", "[[base-de-datos]]"]
summary: Qué está funcionando hoy, qué falta y cuál es el próximo paso lógico.
---

# 📋 Estado actual — 16 julio 2026

## ✅ Completado y funcionando

- [x] Flask + SQLite corriendo localmente
- [x] Panel `/admin` para agregar propiedades con fotos
- [x] Subida de múltiples imágenes a Cloudinary (hasta 10 por propiedad)
- [x] Conversión automática a WebP al subir
- [x] Carrusel de fotos por tarjeta de propiedad
- [x] Lightbox (ver fotos ampliadas haciendo clic)
- [x] Filtros dinámicos: departamento, municipio, precio, marca
- [x] 125 municipios de Antioquia con subregiones en el admin
- [x] Descripción desplegable (Bootstrap Collapse)
- [x] Precio formateado con puntos colombianos
- [x] Modo oscuro con persistencia en localStorage
- [x] Botón WhatsApp en cada tarjeta (consultar disponibilidad)
- [x] Botón Compartir por WhatsApp (link directo a la propiedad)
- [x] Página individual `/propiedad/<id>` con meta tags para WhatsApp
- [x] Diseño responsivo para celulares y tablets
- [x] Footer con redes sociales, teléfono y email
- [x] Propiedad ejemplo: Casa de Lujo Llanogrande (19 fotos reales)
- [x] Proyecto en GitHub
- [x] Sitio desplegado en Render.com

---

## ⚠️ Pendiente importante (antes de producción real)

- [ ] **Migrar SQLite → PostgreSQL** — Render reinicia el servidor y borra el `.db`
  - Agregar `psycopg2` a requirements.txt
  - Configurar `DATABASE_URL` en Render Environment
  - Exportar datos actuales e importar a PostgreSQL
- [ ] **Agregar CLOUDINARY_URL a las variables de Render** — sin esto las fotos no se suben desde el servidor
- [ ] **Dominio personalizado** — conectar un dominio propio en lugar de `.onrender.com`

---

## 🔮 Funcionalidades futuras (ideas)

- [ ] Autenticación del panel admin (login con contraseña)
- [ ] Editar o borrar propiedades desde el admin
- [ ] Formulario de contacto con email automático
- [ ] Búsqueda por texto libre (título o descripción)
- [ ] Ordenar por precio (menor a mayor / mayor a menor)
- [ ] Marcar propiedades como "vendido" o "disponible"
- [ ] WhatsApp Business API para respuestas automáticas
- [ ] Aprender JavaScript — paralelo al avance de Python

---

## 🏠 Propiedad de ejemplo en la BD

**Casa de Lujo – Unidad Cerrada Llanogrande**
- Categoría: Casa
- Municipio: Rionegro, Antioquia
- Precio: $1.700.000.000
- Fotos: 19 imágenes reales (exterior, sala, cocina, habitaciones, baños, jacuzzi, turco, closet)
- Descripción: 118 m², estrato 4, parqueadero doble, jacuzzi, sauna, 3 hab. con baño privado

---

## 🧑‍💻 Contexto de aprendizaje

Este proyecto se construyó para **aprender Python** desde cero.  
Metodología usada en cada sesión:
1. **ENTENDER** — ¿Qué vamos a crear y para qué sirve?
2. **PENSAR** — ¿Qué necesita ese archivo? ¿Qué problema resuelve?
3. **ESCRIBIR** — Línea por línea con explicación
4. **VERIFICAR** — ¿Funciona? ¿Tiene errores?

Próximo tema a aprender: **JavaScript** (en paralelo con el proyecto Python).

→ [[funcionalidades]] | [[github-render]] | [[Home]]
