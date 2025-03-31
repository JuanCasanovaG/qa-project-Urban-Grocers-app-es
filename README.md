# Proyecto Urban Grocers 
# Proyecto QA: Urban Grocers App

Este proyecto contiene pruebas automatizadas para validar la creación de kits de productos en la aplicación Urban Grocers. Se implementan pruebas tanto positivas como negativas para verificar el comportamiento del endpoint de creación de kits, de acuerdo a la lista de comprobación definida.

## Contenido del Proyecto

- **configuration.py:**  
  Configuración de la URL del servidor y rutas de la API (para crear usuarios y kits).  
- **sender_stand_request.py:**  
  Funciones para enviar solicitudes HTTP para la creación de un usuario y de un kit.
- **data.py:**  
  Diccionarios base con datos para la creación de un usuario y un kit, que se reutilizan en las pruebas.
- **create_kit_name_kit_test.py:**  
  Conjunto de pruebas automatizadas (usando Pytest) que validan los distintos escenarios para el campo "name" en la creación de un kit.
- **.gitignore:**  
  Archivo para ignorar archivos y carpetas innecesarias (ya configurado).
- **README.md:**  
  Este archivo, que contiene una breve descripción del proyecto y las instrucciones para ejecutar las pruebas.

## Requisitos

- Python 3.x
- [Pytest](https://docs.pytest.org/)
- [Requests](https://docs.python-requests.org/)

## Configuración

1. Actualiza la URL del servidor en `configuration.py` según sea necesario.  
   Ejemplo:
   ```python
   URL_SERVICE = "https://tu-url-actual.containerhub.tripleten-services.com"
   CREATE_USER_PATH = "/api/v1/users"
   KITS_PATH = "/api/v1/kits"
Asegúrate de que el servidor esté activo y accesible.

Ejecución de las Pruebas
Abre la terminal en la raíz del proyecto.

Ejecuta el siguiente comando para correr las pruebas:

pytest

Informe de Pruebas – Validación de Creación de Kits:
Durante la ejecución de las pruebas automatizadas se identificaron las siguientes discrepancias:

Nombre vacío: Se esperaba un error 400, pero la API creó el kit con un nombre vacío (201).

Nombre de 512 caracteres: Se esperaba un error 400 por exceder el límite de 511 caracteres, pero la API creó el kit (201).

Parámetro "name" no incluido: Se esperaba un error 400, pero la API generó un error 500, lo que indica un fallo interno.

Tipo de dato incorrecto para "name": Se esperaba un error 400 al enviar un número en lugar de una cadena, pero la API creó el kit (201).

Se recomienda revisar la lógica de validación en el endpoint de creación de kits para asegurarse de que cumpla con las especificaciones definidas en la documentación.
