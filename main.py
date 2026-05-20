from src.core import verificar_conexion


def ejecutar_aplicacion():
    """Inicia el ciclo de vida de la aplicación Home Hub Pro y valida su conectividad.

    Imprime el mensaje de bienvenida del sistema y realiza una comprobación
    de red llamando a `verificar_conexion()`. Dependiendo del resultado,
    notifica al usuario si el estado actual es de conexión exitosa o si
    existe un problema de red.
    """
    print("Iniciando Home Hub Pro...")
    if verificar_conexion():
        print("Status: Conectado a la red Existosamente.")
    else:
        print("Status: Error de conexión. Revisa tu conexión a internet.")


if __name__ == "__main__":
    ejecutar_aplicacion()
