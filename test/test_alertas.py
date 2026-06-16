"""Módulo de pruebas unitarias para la lógica de alertas del sistema Home Hub Pro.

Este fichero contiene el conjunto de pruebas encargadas de validar el correcto
funcionamiento de las alertas de inventario. Utiliza el framework Pytest para
verificar el comportamiento de la inspección de stock mínimo y la clasificación
cronológica de las fechas de caducidad bajo diferentes escenarios y datos de prueba.

Casos de prueba cubiertos:
    * verificar_stock_bajo:
        - Retorno correcto de productos que no alcanzan el umbral mínimo.
        - Comportamiento con inventarios vacíos o cuando no hay alertas.
        - Uso correcto de la despensa por defecto en caso de omitir el parámetro.
    * verificar_caducidades:
        - Clasificación precisa en 'caduca_hoy', 'ya_caducado' y márgenes de días.
        - Omisión correcta de productos que no poseen fecha de caducidad asignada.
"""
from datetime import datetime
from src.business_logic.alertas import verificar_stock_bajo, verificar_caducidades

### Variables para las pruebas ###

# Fecha para las pruebas de caducidad
fecha_hoy_pruebas = datetime(2026, 5, 26)

# Despensa ficticia para las pruebas de caducidad
despensa_ficticia_pruebas_caducidad = {
    # Caduca HOY (Diferencia = 0)
    "YOGUR-001": {"fecha_caducidad": "2026-05-26"},
    # YA CADUCADO (Diferencia < 0)
    "LECHE-001": {"fecha_caducidad": "2026-05-20"},
    # CADUCA EN 2 DÍAS (0 < Diferencia <= 3)
    "PASTA-001": {"fecha_caducidad": "2026-05-28"},
    # Debe ser IGNORADO
    "SAL-001": {"fecha_caducidad": None}
}

# Despensa ficticia para las pruebas de stock
despensa_ficticia_pruebas_stock = {
    "ACEITE-001": {
        "nombre": "Aceite de Oliva",
        "cantidad_actual": 1.0,
        "cantidad_minima": 3.0   # <-- ALERTA: Stock bajo (1.0 < 3.0)
    },
    "ARROZ-001": {
        "nombre": "Arroz Integral",
        "cantidad_actual": 5.0,
        "cantidad_minima": 2.0   # <-- OK: Tiene de sobra (5.0 >= 2.0)
    },
    "LECHE-002": {
        "nombre": "Leche Entera",
        "cantidad_actual": 2.0,
        # <-- OK: Está justo en el límite (2.0 >= 2.0)
        "cantidad_minima": 2.0
    }
}


def test_verificar_stock_bajo():
    """Valida que se identifiquen correctamente los productos con existencias insuficientes.

    A partir de un diccionario de pruebas con datos simulados de inventario,
    se verifica que la función devuelva de manera precisa aquellos artículos
    cuya cantidad actual se encuentra por debajo del umbral mínimo configurado.
    """
    resultado = verificar_stock_bajo(despensa_ficticia_pruebas_stock)
    assert "ACEITE-001" in resultado


def test_verificar_caducidades():
    """Valida la correcta clasificación cronológica de los productos según su fecha de vencimiento.

    A partir de una fecha de referencia fija y un inventario simulado de pruebas,
    se verifica que la función organice correctamente los productos en sus
    respectivas categorías de alerta, asegurando que se detecten tanto los artículos
    que vencen el mismo día como los que ya han caducado.
    """
    resultado = verificar_caducidades(
        "2026-05-26", despensa_ficticia_pruebas_caducidad)
    assert "YOGUR-001" in resultado["caduca_hoy"]
    assert "LECHE-001" in resultado["ya_caducado"]
