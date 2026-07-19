---
title: Aprendizaje — Flask
tags: [flask, rutas, jinja2, sesiones, decoradores]
type: note
created: 2026-07-19
updated: 2026-07-19
status: growing
summary: Cómo funciona Flask por dentro — rutas, templates, sesiones y formularios.
---

# 🌶️ Aprendizaje — Flask

> Flask es el framework que convierte Python en un servidor web. Aquí están los patrones clave aprendidos.

---

## Cómo funciona una ruta

```python
@app.route('/')          # URL que activa esta función
def inicio():            # Nombre de la función (puede ser cualquiera)
    return render_template('index.html')   # Qué mostrar al usuario
```

Cuando el usuario entra a `/`, Flask ejecuta `inicio()` y devuelve el HTML procesado.

---

## Métodos GET y POST

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # El usuario envió el formulario
        usuario = request.form.get('usuario')
    else:
        # El usuario solo está viendo la página
        return render_template('login.html')
```

- **GET** = el usuario visita la URL (o hace clic en un link)
- **POST** = el usuario envió un formulario con datos

---

## Pasar datos al template

```python
return render_template(
    'index.html',
    propiedades = lista_de_propiedades,
    total       = len(lista_de_propiedades),
    filtro      = 'Casa'
)
```

En el HTML, esos datos se usan con `{{ variable }}` o `{% lógica %}`:

```html
<p>Encontramos {{ total }} propiedades</p>
{% for p in propiedades %}
    <h3>{{ p['titulo'] }}</h3>
{% endfor %}
```

---

## Filtros personalizados de Jinja2

```python
@app.template_filter('formato_precio')
def formato_precio(valor):
    return '$' + '{:,}'.format(int(valor)).replace(',', '.')
```

Se usa en el template así:
```html
{{ propiedad['precio'] | formato_precio }}
```

Un filtro transforma un valor antes de mostrarlo. `|` es el operador de filtro.

---

## Sesiones — mantener el login activo

```python
from flask import session

app.secret_key = 'clave-secreta'   # Obligatorio para cifrar la sesión

# Guardar dato en sesión:
session['logged_in'] = True

# Leer dato de sesión:
if session.get('logged_in'):
    # El usuario está autenticado

# Borrar sesión (logout):
session.clear()
```

La `session` es un diccionario especial que Flask guarda cifrado en una cookie del navegador. Persiste mientras el usuario no cierre el navegador o haga logout.

---

## Redirigir al usuario

```python
from flask import redirect

return redirect('/')          # Manda al inicio
return redirect('/login')     # Manda al login
return redirect('/admin')     # Manda al admin
```

---

## Leer parámetros de la URL

URL: `/?filtro=Casa&municipio=Rionegro`

```python
filtro    = request.args.get('filtro', None)       # 'Casa'
municipio = request.args.get('municipio', 'Todos') # 'Rionegro'
```

`request.args` contiene todos los parámetros `?clave=valor` de la URL.

---

## Rutas con parámetros dinámicos

```python
@app.route('/propiedad/<int:id>')
def ver_propiedad(id):
    # id = 5 si la URL es /propiedad/5
    cursor.execute("SELECT * FROM propiedades WHERE id = ?", (id,))
```

`<int:id>` captura el número de la URL y lo pasa a la función.

---

→ [[aprendizaje-python]] | [[aprendizaje-javascript]] | [[Home]]
