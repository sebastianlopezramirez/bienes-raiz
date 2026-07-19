---
title: "ADR-001: Flask sobre Django"
tags: [decision, flask, django, python]
type: note
created: 2026-07-19
updated: 2026-07-19
status: evergreen
summary: Por qué elegimos Flask y no Django para este proyecto de aprendizaje.
---

# ADR-001 — Flask sobre Django

**Estado:** ✅ Decidido  
**Fecha:** Julio 2026

## Contexto
Necesitábamos un framework web Python para construir la vitrina. Las dos opciones principales eran Flask y Django.

## Decisión
Usar **Flask**.

## Por qué Flask
- Más simple para aprender — menos "magia" oculta
- Ves exactamente lo que pasa en cada línea
- Ideal cuando el proyecto es pequeño y el objetivo es aprender
- No impone estructura: tú decides cómo organizar el código

## Por qué NO Django (por ahora)
- Tiene demasiadas capas automáticas para alguien que está aprendiendo
- El ORM y el admin automático ocultan cómo funciona realmente la BD
- Mejor estudiarlo cuando ya se entienda Flask por completo

## Consecuencias
- Tenemos que construir cosas manualmente (login, filtros, etc.)
- Pero eso es exactamente lo que queremos: entender cada pieza

→ [[arquitectura]] | [[Home]]
