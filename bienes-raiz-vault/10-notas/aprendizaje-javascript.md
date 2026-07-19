---
title: Aprendizaje — JavaScript
tags: [javascript, frontend, pendiente]
type: note
created: 2026-07-19
updated: 2026-07-19
status: seedling
summary: Próximo lenguaje a aprender. Esta nota irá creciendo a medida que avancemos.
---

# 🟨 Aprendizaje — JavaScript

> **Estado:** Pendiente — próximo tema a estudiar en paralelo con Python.

---

## Por qué JavaScript después de Python

Python controla el **servidor** (lo que pasa antes de que llegue la página).  
JavaScript controla el **navegador** (lo que pasa después, sin recargar la página).

En este proyecto ya usamos JavaScript sin saberlo del todo:

```javascript
// Modo oscuro — guarda la preferencia del usuario
function toggleTema() {
    var nuevo = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
    localStorage.setItem('tema', nuevo);   // guarda en el navegador
}

// Compartir propiedad — construye el link y abre WhatsApp
function compartir(id, titulo, precio) {
    var link    = window.location.origin + '/propiedad/' + id;
    var mensaje = '🏡 ' + titulo + '\n💰 ' + precio + '\n\n' + link;
    window.open('https://wa.me/?text=' + encodeURIComponent(mensaje), '_blank');
}
```

---

## Conceptos que vienen

- Variables: `var`, `let`, `const`
- Funciones y eventos (`onclick`, `addEventListener`)
- `document.querySelector()` — seleccionar elementos del HTML
- `fetch()` — hacer peticiones al servidor sin recargar la página (AJAX)
- `localStorage` — guardar datos en el navegador
- `JSON.parse()` / `JSON.stringify()` — convertir entre texto y objetos

---

## Nota para cuando empecemos

Documentar aquí cada concepto nuevo con un ejemplo real del proyecto, igual que en [[aprendizaje-python]] y [[aprendizaje-flask]].

---

→ [[aprendizaje-flask]] | [[Home]]
