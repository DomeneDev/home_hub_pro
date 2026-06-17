"""Módulo de pruebas unitarias para la lógica de operaciones de Home Hub Pro.

Este fichero contiene las suites de pruebas encargadas de validar las transacciones
de inventario del día a día (compras y consumos). Utiliza el framework Pytest
para asegurar el correcto flujo de datos sobre las existencias, verificando tanto
los casos de éxito como la gestión de límites críticos para evitar inconsistencias.

Casos de prueba cubiertos:
    * test_registrar_compra_incrementa_stock: Verifica el aumento del saldo actual.
    * test_consumir_producto_descuenta_stock: Verifica la reducción del saldo actual.
    * test_consumir_producto_impide_negativos: Valida que el stock no baje de cero.
"""

from src.business_logic.operaciones import registrar_compra, consumir_producto

# Despensa ficticia para las pruebas de stock
despensa_ficticia_pruebas_stock = {
    "ACEITE-001": {
        "nombre": "Aceite de Oliva",
        "cantidad_actual": 3.0,
        "cantidad_minima": 3.0
    },
    "ARROZ-001": {
        "nombre": "Arroz Integral",
        "cantidad_actual": 5.0,
        "cantidad_minima": 2.0
    },
    "LECHE-002": {
        "nombre": "Leche Entera",
        "cantidad_actual": 2.0,
        "cantidad_minima": 2.0
    }
}


def test_registrar_compra_incrementa_stock():
    """Valiada que el registro de una compra aumente correctamente las
    existencias del producto.

    A partir de la despensa de pruebas, ejecuta la función de compra para un
    SKU especifico y verifica mediante aserciones que la cantidad actual se
    incremente exactamente el valor indicado
    """
    registrar_compra("ARROZ-001", 3, despensa_ficticia_pruebas_stock)
    assert despensa_ficticia_pruebas_stock["ARROZ-001"]["cantidad_actual"] == 8.0


def test_consumir_producto_descuenta_stock():
    """Valida que el consumo de un producto ser reduzca de forma correcta
    sus existencias.

    Comprueba que, al procesar la salida de un articulo disponible, el
    inventario actualize la cantidad restante restando el valor consumido
    """
    consumir_producto("ACEITE-001", 2, despensa_ficticia_pruebas_stock)
    assert despensa_ficticia_pruebas_stock["ACEITE-001"]["cantidad_actual"] == 1.0


def test_consumir_producto_impide_negativos():
    """Garantiza que el consumo de un producto no permita que el stock sea
    inferior a cero.

    Evalúa el caso límite en el que se intenta consumir una cantidad mayor
    a la existente en el inventario, verificando que el sistema controle la
    operación para evitar incosistencias.
    """
    consumir_producto("LECHE-002", 4, despensa_ficticia_pruebas_stock)
    assert despensa_ficticia_pruebas_stock["LECHE-002"]["cantidad_actual"] == 2.0
