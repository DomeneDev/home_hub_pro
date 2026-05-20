import requests


def verificar_conexion():
    """Verifica si hay conectividad a Internet realizando una petición a la API de GitHub.

    Realiza una solicitud GET ligera con un tiempo de espera límite para comprobar
    si el entorno actual puede comunicarse con servicios externos. Captura cualquier
    excepción de la librería `requests` para evitar que el programa falle.

    Returns:
        bool: True si la conexión fue exitosa y el servidor respondió con un
            código de estado 200. False en caso contrario o si ocurrió un error
            de red (timeout, DNS, etc.).
    """
    try:
        # Hacemos una petición ligera a la API de GitHub para probar
        respuesta = requests.get("https://api.github.com", timeout=5)
        return respuesta.status_code == 200
    except requests.RequestException:
        return False
