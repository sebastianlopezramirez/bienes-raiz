---
title: GitHub + Render — Despliegue paso a paso
tags: [github, render, despliegue, git, produccion]
type: note
created: 2026-07-16
updated: 2026-07-16
status: evergreen
related: ["[[arquitectura]]"]
summary: Cómo el código va de tu computador al servidor en vivo, paso a paso.
---

# 🚀 GitHub + Render — Despliegue

## Flujo completo: del código al servidor

```
Tu computador (VSCode / editas el código)
        ↓  git add . && git commit && git push
GitHub (repositorio online — guarda el historial)
        ↓  Render detecta el push automáticamente
Render (servidor en la nube — ejecuta el sitio)
        ↓
Usuarios del mundo acceden al sitio
```

---

## Comandos git — subir cambios

Cada vez que terminas de hacer cambios, ejecuta esto en la terminal dentro de la carpeta del proyecto:

```bash
# 1. Marcar todos los archivos cambiados para subir
git add .

# 2. Guardar el estado con un mensaje que explique qué cambiaste
git commit -m "Descripción de lo que hiciste"

# 3. Enviar a GitHub
git push
```

Render detecta el push y re-despliega automáticamente en ~2 minutos.

---

## Archivos que NO deben subir a GitHub

El archivo `.gitignore` los excluye automáticamente:

```
.env          ← Credenciales de Cloudinary (SECRETO)
*.db          ← Base de datos local (efímera, no sirve en producción)
__pycache__/  ← Archivos compilados de Python (se generan solos)
.vs/          ← Configuración de Visual Studio
```

---

## Variables de entorno en Render

El archivo `.env` no va a GitHub (por seguridad). En Render hay que configurar las mismas variables manualmente:

1. Ir al dashboard de Render → tu servicio → **Environment**
2. Agregar:

| Key | Value |
|---|---|
| `CLOUDINARY_URL` | `cloudinary://API_KEY:API_SECRET@CLOUD_NAME` |

Sin esta variable, las fotos no se podrán subir desde el servidor de Render.

---

## Archivos necesarios para que Render funcione

### `requirements.txt`
```
flask
gunicorn
cloudinary
python-dotenv
```

### Por qué `gunicorn`
Flask tiene un servidor de desarrollo (`flask run`) que **no es seguro para producción**. Gunicorn es el servidor WSGI que Render usa para ejecutar la app de forma profesional.

Render ejecuta internamente: `gunicorn app:app`  
Esto significa: *"usa gunicorn para servir el objeto `app` del archivo `app.py`"*

---

## Links del proyecto

| Recurso | URL |
|---|---|
| Render Dashboard | https://dashboard.render.com |
| GitHub Repo | (agrega aquí tu URL de GitHub) |
| Sitio en producción | (agrega aquí tu URL de Render) |

---

## Solución de problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| El sitio no actualiza después del push | Render está re-desplegando | Esperar 2 min y recargar |
| Error 500 en producción | `CLOUDINARY_URL` no configurada en Render | Agregar en Environment |
| Las fotos no cargan | URLs de Cloudinary incorrectas en la BD | Revisar en /admin que se subieron bien |
| La BD se borró | Render reinició el servidor (storage efímero) | Migrar a PostgreSQL |

→ [[arquitectura]] | [[Home]]
