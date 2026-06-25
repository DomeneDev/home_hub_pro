"""Módulo de persistencia y almacenamiento local para Home Hub Pro.

Este módulo centraliza la persistencia del estado de la despensa familiar mediante
operaciones de lectura y escritura en archivos locales de formato JSON. Permite que
los cambios del inventario se mantengan entre diferentes ejecuciones de la aplicación.

Funciones incluidas:
    * guardar_inventario: Exporta el estado del inventario actual a un JSON.
    * cargar_inventario: Importa los datos del inventario desde un JSON o recupera el fallback.
"""

import json


def guardar_inventario(inventario: dict, ruta_archivo: str) -> bool:
    """Exporta el estado actual del inventario y lo almacena en un archivo JSON.

    Toma el diccionario que representa la despensa y lo escribe con un formato
    legible (indentado) en el disco duro. Maneja excepciones de tipo de entrada/salida
    (I/O) para evitar caídas de la aplicación si el directorio o el archivo no son accesibles.

    Args:
        inventario (dict): Diccionario estructurado con los productos de la despensa.
        ruta_archivo (str): Ruta local (relativa o absoluta) donde se guardará el archivo.

    Returns:
        bool: True si la operación de guardado finalizó con éxito; False si ocurrió
            algún error de escritura (ej. PermissionError, FileNotFoundError, IOError).
    """
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(inventario, f, indent=4)
            return True
    except OSError:
        print("Error al guardar inventario..")
        return False


def cargar_inventario(ruta_archivo: str) -> dict:
    """Importa el inventario guardado desde un archivo JSON local.

    Intenta abrir y decodificar el archivo JSON especificado por la ruta. Si el archivo
    no existe o su estructura de datos está corrupta, la función intercepta el error de
    forma segura y retorna el diccionario base de la despensa por defecto para no romper
    el arranque de la aplicación.

    Args:
        ruta_archivo (str): Ruta local del archivo JSON que se desea leer.

    Returns:
        dict: Diccionario que contiene el inventario cargado con éxito, o en su defecto,
            el diccionario inicial cargado desde el módulo central de la aplicación.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8')as f:
            print("Despensa cargada existosamente...")
            return json.load(f)
    except FileNotFoundError:
        productos = {}
        print("No existe despensa en la ruta especificada, se crea una despensa nueva...")
        return productos
    except json.JSONDecodeError:
        productos = {}
        print(
            "El archivo de despensa está corrupto, no se puede cargar, se crea una depensa nueva..."
        )
        return productos
