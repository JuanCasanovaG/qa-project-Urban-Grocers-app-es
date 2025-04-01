# sender_stand_request.py

import requests
from configuration import URL_SERVICE, CREATE_USER_PATH, KITS_PATH


def post_new_user(user_body):
    """
    Envía una solicitud POST para crear un nuevo usuario o usuaria.

    Parámetros:
      - user_body: Diccionario con los datos del usuario, por ejemplo:
          {
              "firstName": "Max",
              "phone": "+10005553535",
              "address": "8042 Lancaster Ave.Hamburg, NY"
          }

    Retorna:
      La respuesta del servidor (objeto response).

    Ejemplo de respuesta exitosa (HTTP 201):
      {
          "authToken": "jknnFApafP4awfAIFfafam2fma"
      }
    En caso de error (HTTP 400):
      {
          "code": 400,
          "message": "No se han aprobado todos los parámetros requeridos. Parámetros requeridos: nombre, teléfono, dirección"
      }
    """
    url = URL_SERVICE + CREATE_USER_PATH
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=user_body, headers=headers)
    return response


def post_new_client_kit(kit_body, auth_token):
    """
    Envía una solicitud POST para crear un kit personal para un usuario.

    Parámetros:
      - kit_body: Diccionario con los datos del kit, por ejemplo:
          {
              "name": "Mi conjunto"
          }
      - auth_token: Token de autenticación obtenido al crear el usuario.

    Importante: Se debe pasar el encabezado Authorization con el valor Bearer {authToken}.

    Retorna:
      La respuesta del servidor (objeto response).

    Ejemplo de respuesta exitosa (HTTP 201):
      {
          "name": "Mi conjunto",
          "card": {
              "id": 1,
              "name": "Para la situación"
          },
          "productsList": null,
          "id": 7,
          "productsCount": 0
      }
    En caso de error (HTTP 400):
      {
          "code": 400,
          "message": "No se han aprobado todos los parámetros requeridos"
      }
    """
    url = URL_SERVICE + KITS_PATH
    headers = {
        "Content-Type": "application/json"
    }
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    response = requests.post(url, json=kit_body, headers=headers)
    return response


# Bloque principal para pruebas
if __name__ == '__main__':
    # Datos para la creación de usuario
    user_data = {
        "firstName": "Max",
        "phone": "+10005553535",
        "address": "8042 Lancaster Ave.Hamburg, NY"
    }

    print("Creando usuario...")
    user_response = post_new_user(user_data)
    print("Código de estado (usuario):", user_response.status_code)
    print("Respuesta (usuario):", user_response.text)

    # Si el usuario se creó correctamente, extraemos el authToken
    if user_response.status_code == 201:
        user_json = user_response.json()
        auth_token = user_json.get("authToken")
        print("Token de autenticación obtenido:", auth_token)
    else:
        auth_token = None
        print("Error al crear el usuario; no se puede continuar con la creación del kit.")

    # Datos para la creación de kit
    if auth_token:
        kit_data = {
            "name": "Mi conjunto"
        }
        print("Creando kit...")
        kit_response = post_new_client_kit(kit_data, auth_token)
        print("Código de estado (kit):", kit_response.status_code)
        print("Respuesta (kit):", kit_response.text)
    else:
        print("No se creó el kit, ya que no se obtuvo un token de autenticación.")
