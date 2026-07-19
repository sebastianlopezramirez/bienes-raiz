---
title: Funcionalidades implementadas
tags: [frontend, bootstrap, javascript, whatsapp, carousel, lightbox, filtros]
type: note
created: 2026-07-16
updated: 2026-07-16
status: evergreen
related: ["[[flask-backend]]", "[[arquitectura]]"]
summary: Todo lo que el usuario puede hacer en la vitrina y cómo está construido.
---

# ✨ Funcionalidades

## 1. Vitrina de categorías (página de inicio)

Al entrar al sitio sin filtro, se muestran 3 tarjetas grandes:
- **Lotes en Venta** → `/?filtro=Lote`
- **Casas & Fincas** → `/?filtro=Casa`
- **Vehículos** → `/?filtro=Carro`

Cada tarjeta tiene imagen de portada, título y descripción corta.

---

## 2. Carrusel de fotos por propiedad

Cada tarjeta de propiedad tiene un carrusel Bootstrap con:
- Todas las fotos de esa propiedad (pueden ser 1 o hasta 20+)
- Puntitos indicadores (si hay más de 1 foto)
- Flechas de navegación (si hay más de 1 foto)

Las fotos se guardan en Cloudinary. La BD almacena la lista de URLs como JSON.

---

## 3. Lightbox — ver fotos ampliadas

Al hacer clic en cualquier foto del carrusel:
- Se abre un modal de pantalla completa (negro)
- Muestra todas las fotos de esa propiedad con flechas de navegación
- Contador "3 / 19" en la parte inferior
- Se cierra con la X o haciendo clic fuera

Tecnología: Bootstrap Modal + JavaScript vanilla.

---

## 4. Filtros de búsqueda

Disponibles en el catálogo (`?filtro=Casa` por ejemplo):
- **Departamento** — lista fija de Colombia
- **Municipio** — lista dinámica (solo muestra municipios con propiedades en la BD)
- **Precio máximo** — opciones predefinidas
- **Marca** — solo visible en la sección Vehículos

Los filtros se combinan: puedes filtrar por municipio Y precio al mismo tiempo.

---

## 5. Descripción desplegable

Cada tarjeta tiene un botón "📋 Ver descripción ▾" que despliega el texto  
usando **Bootstrap Collapse** — sin recargar la página, solo con CSS y JS de Bootstrap.

---

## 6. Precio formateado

El precio se muestra con puntos colombianos:  
`1700000000` → `$1.700.000.000`

Esto se hace con un filtro personalizado de Jinja2 en `app.py`:
```python
@app.template_filter('formato_precio')
def formato_precio(valor):
    return '$' + '{:,}'.format(int(valor)).replace(',', '.')
```

---

## 7. Modo oscuro

Botón 🌙 / ☀️ en la navbar que:
- Cambia el tema entre `light` y `dark` usando `data-bs-theme` de Bootstrap 5.3
- Guarda la preferencia en `localStorage` del navegador
- Se aplica automáticamente en la siguiente visita

---

## 8. Botón WhatsApp — consultar disponibilidad

En cada tarjeta hay un botón verde que abre WhatsApp con mensaje pre-escrito:
```
https://wa.me/573137921336?text=Hola, estoy interesado en...
```
El número es `313 792 1336`.

---

## 9. Botón Compartir por WhatsApp

Botón "📤 Compartir" que:
1. Construye el link directo a la página de esa propiedad: `https://tusitio.com/propiedad/5`
2. Arma un mensaje: *"🏡 Casa de Lujo... 💰 $1.700M... ¡Mira aquí! [link]"*
3. Abre WhatsApp con ese mensaje listo para enviar a cualquier contacto

El link lleva a `[[#10-Página individual por propiedad|la página individual]]`.

---

## 10. Página individual por propiedad

Ruta: `/propiedad/<id>`  
Ejemplo: `https://tusitio.com/propiedad/3`

Muestra:
- Galería grande con carrusel (altura 380px en escritorio)
- Título, ubicación, descripción completa
- Precio destacado
- Botón "Consultar Disponibilidad" (WhatsApp al vendedor)
- Botón "Compartir esta propiedad"
- Lightbox al hacer clic en fotos

Incluye **meta tags OpenGraph** para que WhatsApp muestre previsualización con foto, título y descripción al pegar el link.

---

## 11. Diseño responsivo

El sitio se adapta a cualquier tamaño de pantalla:
- **Móvil (< 576px):** 1 tarjeta por fila, navbar compacta, fotos más pequeñas
- **Tablet (576–768px):** 2 tarjetas por fila
- **Escritorio (> 992px):** 3 tarjetas por fila

Implementado con clases Bootstrap `col-12 col-sm-6 col-md-4` + media queries en `estilo.css`.

→ [[flask-backend]] | [[proyecto-moc]] | [[Home]]
