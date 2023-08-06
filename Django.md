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

## Nociones basicas

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
Veremos que se creo un nuevo directorio que se llama igual que nuestro app, sin emabargo el proyecto en django no tiene idea de que este app existe. Debemos conectarlos.

Para esto debemos indicar nuestro app en el archivo settings.py dentro de INSTALLED_APPS.

Luego para definir una vista lo hacemos a traves de una funcion. Dicha funcion debe tener como parametro a request, que es donde obtendremos la info del request que estamos atendiendo.
```python
def home(request):
  return
```

Como el proyecto puede crecer demasiado, conviene crear un archivo urls.py por cada app para que el archivo urls.py del proyecto no crezca de forma exagerada.

Luego, una vez creado el archivo urls.py en nuestro app, debemos indicar el mismo al archivo urls.py principal y esto lo hacemos mediante la funcion include:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]
```

## templates
Para mantener la organizacion tambien es bueno crear un directorio exclusivamente para los templates. Luego de crear el directorio debemos indicarle a Django donde esta, para que pueda encontrar los templates, para esto lo indicamos en settings.py en TEMPLATES y en el valor de DIRS

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