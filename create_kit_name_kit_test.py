# create_kit_name_kit_test.py
import pytest
from data import base_kit, base_user
from sender_stand_request import post_new_client_kit, post_new_user

def get_new_user_token():
    """
    Crea un usuario usando los datos base y retorna el authToken.
    Se asume que la respuesta exitosa es HTTP 201 y que el token viene en el campo "authToken".
    """
    response = post_new_user(base_user)
    assert response.status_code == 201, f"Error al crear el usuario, se recibió: {response.status_code}"
    user_json = response.json()
    token = user_json.get("authToken")
    assert token, "No se obtuvo el authToken del usuario"
    return token

def get_kit_body(name):
    """
    Retorna una copia del diccionario base del kit, asignando el valor recibido al campo "name".
    """
    kit = base_kit.copy()  # Evitamos modificar el diccionario original
    kit["name"] = name
    return kit

def positive_assert(kit_body):
    """
    Envía la solicitud para crear un kit y verifica que la respuesta sea 201,
    además de que el campo "name" en la respuesta coincida con el enviado.
    """
    token = get_new_user_token()
    response = post_new_client_kit(kit_body, token)
    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    response_json = response.json()
    assert response_json.get("name") == kit_body.get("name"), "El nombre en la respuesta no coincide con el de la solicitud"

def negative_assert_code_400(kit_body):
    """
    Envía la solicitud para crear un kit y verifica que la respuesta sea 400.
    """
    token = get_new_user_token()
    response = post_new_client_kit(kit_body, token)
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"

# Caso 1: El número permitido de caracteres (1)
def test_nombre_minimo():
    kit_body = get_kit_body("a")
    positive_assert(kit_body)

# Caso 2: El número permitido de caracteres (511)
def test_nombre_511_caracteres():
    # Generamos una cadena de 511 caracteres.
    kit_body = get_kit_body("A" * 511)
    positive_assert(kit_body)

# Caso 3: El número de caracteres es menor que lo permitido (0)
def test_nombre_vacio():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)

# Caso 4: El número de caracteres es mayor que lo permitido (512)
def test_nombre_512_caracteres():
    kit_body = get_kit_body("A" * 512)
    negative_assert_code_400(kit_body)

# Caso 5: Se permiten caracteres especiales
def test_caracteres_especiales():
    # Ejemplo de caracteres especiales, según lo indicado en la lista de comprobación.
    kit_body = get_kit_body("№%@,")
    positive_assert(kit_body)

# Caso 6: Se permiten espacios
def test_espacios_permitidos():
    kit_body = get_kit_body(" A Aaa ")
    positive_assert(kit_body)

# Caso 7: Se permiten números (pasados como string)
def test_numeros_permitidos():
    kit_body = get_kit_body("123")
    positive_assert(kit_body)

# Caso 8: El parámetro no se pasa en la solicitud
def test_parametro_no_incluido():
    kit_body = base_kit.copy()
    # Eliminamos el campo "name" para simular que no se pasó el parámetro
    kit_body.pop("name", None)
    negative_assert_code_400(kit_body)

# Caso 9: Se ha pasado un tipo de parámetro diferente (número en lugar de string)
def test_tipo_parametro_incorrecto():
    kit_body = base_kit.copy()
    kit_body["name"] = 123  # Se asigna un número en vez de un string
    negative_assert_code_400(kit_body)
