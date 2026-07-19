---
title: Aprendizaje — Python
tags: [python, aprendizaje, fundamentos]
type: note
created: 2026-07-19
updated: 2026-07-19
status: growing
summary: Conceptos de Python aprendidos construyendo este proyecto, con ejemplos reales del código.
---

# 🐍 Aprendizaje — Python

> Conceptos que aprendí construyendo este proyecto. Cada uno tiene un ejemplo real del código de `app.py`.

---

## Importaciones

```python
from flask import Flask, render_template, request, redirect, session
import sqlite3, os, json
from functools import wraps
from dotenv import load_dotenv
```

`import` trae herramientas externas al archivo. `from X import Y` trae solo la parte que necesitas.

---

## Variables de entorno con `os.getenv()`

```python
import os
valor = os.getenv('NOMBRE_VARIABLE', 'valor_por_defecto')
```

Lee datos del archivo `.env` sin escribirlos en el código. Si la variable no existe, usa el valor por defecto.

---

## Funciones

```python
def formato_precio(valor):
    return '$' + '{:,}'.format(int(valor)).replace(',', '.')
```

`def` define una función. `return` devuelve el resultado. Esta función convierte `1700000000` → `$1.700.000.000`.

---

## Decoradores

Un decorador **envuelve** una función para agregarle comportamiento extra.

```python
from functools import wraps

def login_required(f):      # f = la función que vamos a proteger
    @wraps(f)
    def decorador(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)
    return decorador

# Uso:
@login_required
def admin():
    ...
```

`@login_required` es como poner un guardia antes de la función. Si no hay sesión activa, redirige al login.

---

## Try / Except — manejo de errores

```python
try:
    cursor.execute("ALTER TABLE propiedades ADD COLUMN municipio TEXT")
except:
    pass   # Si ya existe la columna, SQLite lanza error → lo ignoramos
```

`try` intenta ejecutar el código. Si falla, `except` captura el error y decide qué hacer. `pass` significa "ignorar y continuar".

---

## JSON — convertir entre texto y listas

```python
import json

# Lista Python → texto para guardar en la BD
texto = json.dumps(["foto1.jpg", "foto2.jpg"])
# resultado: '["foto1.jpg", "foto2.jpg"]'

# Texto de la BD → lista Python para usar en el código
lista = json.loads(texto)
# resultado: ["foto1.jpg", "foto2.jpg"]
```

---

## Diccionarios

```python
propiedad = {
    'titulo': 'Casa Llanogrande',
    'precio': 1700000000,
    'municipio': 'Rionegro'
}

# Leer un valor:
print(propiedad['titulo'])   # Casa Llanogrande

# SQLite Row → diccionario:
conn.row_factory = sqlite3.Row
fila = cursor.fetchone()
p = dict(fila)   # Convierte la fila a diccionario
```

---

## Bucles

```python
archivos = request.files.getlist('imagenes')

for archivo in archivos:          # itera cada archivo
    if archivo.filename != '':    # solo si tiene nombre (no está vacío)
        file_bytes = archivo.read()
        resultado  = cloudinary.uploader.upload(file_bytes)
        urls.append(resultado['secure_url'])
```

`for X in Y` repite el bloque por cada elemento de la lista. `append()` agrega un elemento al final de una lista.

---

→ [[aprendizaje-flask]] | [[Home]]
