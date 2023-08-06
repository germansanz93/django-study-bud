#Notas sobre Django

## MVT
Model - Data Access Layer
Template - Presentation Layer
View - Business Logic

## Django admin
Si ejecuto django-admin en la terminal puedo ver todos los comandos que tengo disponibles con django.
Algunos de los mas importantes son:
- makemigrations
- migrate
- runserver
- startapp
- startproject

para ejecutar el server en local puedo ejecutar:
```bash
python manage.py runserver
```

## Nociones básicas

WSGI: Web Server Gateway Interface, a mediator that communicates between web servers and Python web applications
ASGI: Asynchronous Server Gateway Interface, is the specification which Channels and Daphne are built upon, designed to untie Channels apps from a specific application server and provide a common way to write application and middleware code

En el archivo urls.py es donde vamos a mapear todo el routing de nuestra app

En el archivo settings.py es donde tenemos las configuraciones principales del proyecto.

En django vamos a trabajar con algo llamado apps, podemos ver que por defecto tenemos algunas apps ya creadas. Basicamente las apps son pequeños componentes de nuestra web que nos permiten administrar diferentes partes del sitio.

Para crear nuestro app base con django ejecutamos el comando:
```bash
python manage.py startapp base 
```
Este app que estamos creando en este caso lo llamamos base porque va a ser nuestro app base.
Veremos que se creo un nuevo directorio que se llama igual que nuestro app, sin embargo el proyecto en django no tiene idea de que este app existe. Debemos conectarlos.

Para esto debemos indicar nuestro app en el archivo settings.py dentro de INSTALLED_APPS.

Luego para definir una vista lo hacemos a traves de una función. Dicha función debe tener como parámetro a request, que es donde obtendremos la info del request que estamos atendiendo.
```python
def home(request):
  return
```

Como el proyecto puede crecer demasiado, conviene crear un archivo urls.py por cada app para que el archivo urls.py del proyecto no crezca de forma exagerada.

Luego, una vez creado el archivo urls.py en nuestro app, debemos indicar el mismo al archivo urls.py principal y esto lo hacemos mediante la función include:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]
```

## templates
Para mantener la organizacion también es bueno crear un directorio exclusivamente para los templates. Luego de crear el directorio debemos indicarle a Django donde esta, para que pueda encontrar los templates, para esto lo indicamos en settings.py en TEMPLATES y en el valor de DIRS

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates' #nueva linea
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
```

Una vez definidos los templates podemos renderizarlos en nuestras views:
```python 
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
  return render(request, 'home.html')

def room(request):
  return render(request, 'room.html')
```

## Herencia de templates
Podemos importar templates desde otros templates, esto nos es util por ejemplo para un navbar o algún segmento de nuestra web que debe repetirse en varias paginas ya que nos permite crear el código una única vez y luego reutilizarlo.

Para esto podemos usar include en los archivos html e indicar que template queremos incluir:
```html
{% include 'navbar.html' %}
<h1>Home Template</h2>
```

Otra opcion que tenemos es dentro de un html, insertar un bloque en una posicion especifica. Para esto tenemos block:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  {% block content %}
  {% endblock  %}
</body>
</html>
```

y luego con extends indicamos el bloque en el otro html al que deseamos importar
```html
{% extends 'main.html' %}

{% block content %}
  <h1>Home Template</h2>
{% endblock  %}
```

## Django template engine
Podemos en los templates de Django enviar variables. (VER DOC.)

Ademas tenemos diferentes tipos de tags. Podemos usar condicionales, iterar, es muy similar a ejs.

Para enviar valores a las vistas lo hago a traves del contexto, el cual es un parametro opocional y espera recibir un map

```python
from django.shortcuts import render
from django.http import HttpResponse

rooms = [
  {'id': 1, 'name': 'Lets learn python!'},
  {'id': 2, 'name': 'Design with Me'},
  {'id': 3, 'name': 'Frontend Developers'},
]

def home(request):
  return render(request, 'home.html', {'rooms': rooms}) #context

def room(request):
  return render(request, 'room.html')
```

Luego podemos acceder a estos valores desde el template y utilizarlos:

```html
{% extends 'main.html' %}

{% block content %}
<h1>Home Template</h1>

<div>
  <div>
    {% for room in rooms %}
      <div>
        <h5>{{room.id}} -- {{room.name}}</h5>
      </div>
    {% endfor %}
  </div>
</div>

{% endblock  %}
```

OJO que si quremos separar los templates por app deben si o si estar dentro de un directorio con el nombre del app, de modo que por ejemplo para nuestro app base quedarian base/templates/base/


## Rutas dinamicas
Podemos pasar variables a las rutas en el archivo de urls.py y views.py de la siguiente forma:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
]
```

```python 
from django.shortcuts import render
from django.http import HttpResponse

rooms = [
  {'id': 1, 'name': 'Lets learn python!'},
  {'id': 2, 'name': 'Design with Me'},
  {'id': 3, 'name': 'Frontend Developers'},
]

def home(request):
  context = {'rooms': rooms}
  return render(request, 'base/home.html', context)

def room(request, pk):
  room = None
  for r in rooms:
    if r['id'] == int(pk):
      room = r
  context = {'room': room}
  return render(request, 'base/room.html', context)


```

```html
{% extends 'main.html' %}

{% block content %}
<h1>Home Template</h1>

<div>
  <div>
    {% for room in rooms %}
      <div>
        <h5>{{room.id}} -- <a href="/room/{{room.id}}">{{room.name}}</a></h5>
      </div>
    {% endfor %}
  </div>
</div>

{% endblock  %}
```

```html
{% extends 'main.html' %}

{% block content %}
  <h1>{{room.name}}</h1>
{% endblock  %}
```

## Nombres de rutas
Si queremos cambiar alguna ruta en un archivo urls.py tendremos que ir a todos los otros archivos donde utilizamos esa ruta y modificarla. En cambio si la referimos por su nombre esto ya no sera necesario debido a que el nombre no cambiara nunca por mas que modifiquemos el path.
Esto lo conseguimos en los templates reemplazando el valor de la url por el tag de url de django

```python
{% extends 'main.html' %}

{% block content %}
<h1>Home Template</h1>

<div>
  <div>
    {% for room in rooms %}
      <div>
        <h5>{{room.id}} -- <a href="{% url 'room' room.id %}">{{room.name}}</a></h5>
      </div>
    {% endfor %}
  </div>
</div>

{% endblock  %}
```

## Apps instaladas
Si observamos en settings.py en INSTALLED_APPS veremos que tenemos varias apps instaladas y la mayoria de estas ya vienen con migraciones para crear las tablas en base de datos y poder comenzar a utilizarse.

Para ejecutar todas las migraciones puedo ejecutar el siguiente comando
```bash
python manage.py migrate
```

Y esto creara nuestra db por nosotros.

Ahora podemos acceder al django admin panel y administrar nuestro sistema.

Por el momento django viene con una db sqlite pero podemos reemplazarla por una db del tipo que nos de la gana.

Luego para crear nuestras propias entidades de bases de datos debemos hacerlo en models.py y esto lo haremos a traves de clases de python, de modo que una clase de python representa a una tabla en la base de datos.

```python
from django.db import models

class Room(models.Model):
    # host =
    # topic =
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants = 
    updated = models.DateTimeField(auto_now=True) # always
    created = models.DateTimeField(auto_now_add=True) # Only first time

    def __str__(self):
        return self.name
```

Luego de crear un modelo en python obviamente que lo primero que debemos hacer es migrar para que se cree nuestra tabla

```bash
python manage.py makemigrations
python manage.py migrate
```
Podemos ver que en el directorio migrations en nuestra app aparece una nueva migracion

Luego con el comando:
```bash
python manage.py createsuperuser
```

podemos crearnos un usuario para acceder al admin panel

A pesar de que agregamos la tabla room, no estamos pudiendo ver la tabla en el panel de administracion, esto se debe a que debemos primero registrar nuestro modelo en el archivo admin.py

```python
from django.contrib import admin
from .models import Room

admin.site.register(Room)

```

## Representando modelos en vistas
Primero debemos importar nuestro modelo al archivo views.py, luego debemos hacer uso del model manager para poder ejecutar queries a la base de datos.

```python 
from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

rooms = [
  {'id': 1, 'name': 'Lets learn python!'},
  {'id': 2, 'name': 'Design with Me'},
  {'id': 3, 'name': 'Frontend Developers'},
]

def home(request):
  rooms = Room.objects.all() #model manager, esta overrideando el valor de rooms
  context = {'rooms': rooms}
  return render(request, 'base/home.html', context)

def room(request, pk):
  room = None
  for r in rooms:
    if r['id'] == int(pk):
      room = r
  context = {'room': room}
  return render(request, 'base/room.html', context)

```