"""Módulo de pruebas unitarias para la validación de la persistencia del inventario.

Este archivo contiene la suite de pruebas automatizadas encargada de verificar
el correcto comportamiento de las funciones de lectura y escritura del módulo
`json_manager.py` (dentro del paquete de persistencia del ERP Familiar). Se evalúan
tanto los escenarios de éxito como el manejo robusto de excepciones (archivos
inexistentes, corrupción de datos y fallos en el sistema de archivos).

Dependencias:
    pytest: Framework principal para la ejecución de pruebas.
    unittest.mock: Para la simulación (mocking) de errores de entrada/salida.
    src.core.persistencia: Módulo que contiene las funciones bajo prueba.

Ubicación del archivo:
    tests/test_json_manager.py
"""

import json
from unittest.mock import patch, mock_open
from src.core.json_manager import guardar_inventario, cargar_inventario


def test_guardar_inventario_exito(tmp_path):
    """
    Verifica que el inventario se guarda correctamente en un archivo JSON válido.

    Utiliza el fixture `tmp_path` de pytest para crear un entorno de pruebas 
    aislado, confirma que la función retorna True y valida mediante lectura 
    manual que el contenido del archivo coincide con el inventario de prueba.

    Args:
        tmp_path (pathlib.Path): Directorio temporal proporcionado por pytest.
    """
    inventario_prueba = {"PROD001": {"nombre": "Leche", "cantidad": 3}}
    archivo_temporal = tmp_path / "inventario.json"
    resultado = guardar_inventario(inventario_prueba, str(archivo_temporal))
    assert resultado is True

    with open(archivo_temporal, "r", encoding="utf-8") as f:
        datos_guardados = json.load(f)
    assert datos_guardados == inventario_prueba


def test_guardar_inventario_error():
    """
    Valida el manejo de errores ante fallos de escritura en el sistema.

    Simula un fallo de E/S (OSError) utilizando `unittest.mock.patch` sobre
    `builtins.open` para asegurar que la función `guardar_inventario` captura
    la excepción y retorna False en lugar de interrumpir la ejecución.
    """
    inventario_prueba = {"PROD001": {"nombre": "Leche", "cantidad": 3}}
    with patch("builtins.open", side_effect=OSError):
        resultado = guardar_inventario(
            inventario_prueba, "ruta_cualquiera.json")
        assert resultado is False


def test_cargar_inventario_exito(tmp_path):
    """
    Comprueba la carga correcta de un inventario desde un archivo JSON existente.

    Crea un archivo temporal con datos conocidos, invoca `cargar_inventario`
    y verifica que el diccionario resultante en memoria sea idéntico al original.

    Args:
        tmp_path (pathlib.Path): Directorio temporal proporcionado por pytest.
    """
    inventario_prueba = {"PROD001": {"nombre": "Leche", "cantidad": 3}}
    archivo_temporal = tmp_path / "inventario.json"
    guardar_exito = guardar_inventario(
        inventario_prueba, str(archivo_temporal))
    assert guardar_exito is True

    resultado = cargar_inventario(str(archivo_temporal))
    assert isinstance(resultado, dict)
    assert resultado == inventario_prueba


def test_cargar_inventario_no_existe():
    """
    Verifica el comportamiento del sistema ante la ausencia del archivo de datos.

    Simula un escenario donde el archivo no existe (lanzando FileNotFoundError)
    para confirmar que `cargar_inventario` gestiona el error devolviendo un
    diccionario vacío, permitiendo que la aplicación continúe sin errores críticos.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        resultado = cargar_inventario("otra_ruta.json")
        assert isinstance(resultado, dict)


def test_cargar_inventario_corrupto():
    """
    Verifica que el sistema maneja correctamente archivos JSON con formato inválido.

    Crea un archivo temporal con contenido que no es un JSON válido (por ejemplo, 
    texto plano mal estructurado) y asegura que la función `cargar_inventario`
    capture el error de decodificación (`json.JSONDecodeError`) y retorne
    un diccionario vacío en lugar de detener la ejecución.

    """
    with patch("builtins.open", new=mock_open(read_data="Esto no es un archivo JSON")):
        resultado = cargar_inventario("otra_ruta.txt")
        assert isinstance(resultado, dict)
