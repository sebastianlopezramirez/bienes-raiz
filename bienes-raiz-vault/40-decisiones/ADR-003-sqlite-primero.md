---
title: "ADR-003: SQLite primero, PostgreSQL después"
tags: [decision, sqlite, postgresql, base-de-datos]
type: note
created: 2026-07-19
updated: 2026-07-19
status: evergreen
summary: Por qué empezamos con SQLite sabiendo que habrá que migrar a PostgreSQL.
---

# ADR-003 — SQLite primero, PostgreSQL después

**Estado:** ✅ Decidido (migración pendiente)  
**Fecha:** Julio 2026

## Contexto
Para producción real en Render, SQLite no es ideal porque el archivo `.db` se borra cuando el servidor se reinicia. PostgreSQL es la solución correcta a largo plazo.

## Decisión
Empezar con **SQLite** y migrar a PostgreSQL cuando el proyecto esté más maduro.

## Por qué SQLite primero
- Sin configurar ningún servidor externo
- El archivo `.db` vive junto al código
- Perfecto para aprender — cero fricción
- `sqlite3` viene incluido en Python, sin instalar nada

## Cuándo migrar
Cuando se necesite que los datos sobrevivan reinicios de Render, o cuando haya usuarios reales usando el sitio.

## Cómo migrar (cuando llegue el momento)
1. Agregar `psycopg2-binary` a `requirements.txt`
2. Cambiar la conexión en `app.py` para leer `DATABASE_URL` del entorno
3. Configurar `DATABASE_URL` en Render → Environment
4. Exportar datos de SQLite e importar a PostgreSQL

→ [[base-de-datos]] | [[github-render]] | [[Home]]
