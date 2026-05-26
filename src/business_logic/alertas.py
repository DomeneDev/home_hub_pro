"""Módulo de gestión de alertas para el sistema Home Hub Pro.

Este módulo se encarga de centralizar la lógica de supervisión del inventario,
analizando el estado actual de la despensa para emitir notificaciones críticas
relacionadas con los niveles de existencias mínimos y las fechas de vencimiento
de los productos.

Funciones incluidas:
    * verificar_stock_bajo: Identifica productos con existencias críticas.
    * verifcar_caducidades: Detecta artículos vencidos o próximos a caducar.
"""
from src.core.inventario import despensa
from datetime import datetime


def verificar_stock_bajo(despensa_a_inspeccionar: dict = None) -> dict:
    """Identifica y recopila los productos del inventario que están por debajo
    de su stock mínimo.

    Evalúa cada artículo de la despensa comparando su cantidad acutal frente al
    umbral mínimo requerido. Si no se proporciona un inventario especifico,
    utilza el módulo de despensa global por defecto.

    Args:
        despensa_a_inspeccionar (dict, optional): Diccionario con la estructura
            de la despensa. Cada clave es el nombre del producto y su valor
            es un diccionario que de contener "cantidad_actual" y
            "cantidad_minima".Por defecto None (usa la despensa global).

    Returns:
        dict: Un diccionario con los productos en estado de alerta, donde las
        claves son los nombres de los articulos y los valores corresponden a
        su cantidad actual.
    """
    productos_en_alerta = {}
    if despensa_a_inspeccionar is None:
        despensa_a_inspeccionar = despensa
    for producto in despensa_a_inspeccionar:
        if despensa_a_inspeccionar[producto]["cantidad_actual"] < despensa_a_inspeccionar[producto]["cantidad_minima"]:
            productos_en_alerta[producto] = despensa_a_inspeccionar[producto]["cantidad actual"]
    return productos_en_alerta


def verificar_caducidades(fecha_hoy: datetime, despensa_a_inspeccionar: dict = None):
    """Clasifica los productos de la despensa según su proximidad a la fecha de
    caducidad.

    Compara la fecha de vencimiento de cada artículo con una fecha de
    referencia (el día de hoy) para organizar los productos en categorias
    críticas: vencidos, vencen hoy o vencen en un margen cercano. Los
    productos sin fecha de caducidad asignada son omitidos de la inspección.

    Args:
        fecha_hoy (datetime): Fecha de referencia objeto fecha datetime.
            formato: "AAAA-MM-DD"
        despensa_a_inspeccionar (dict, optional): Diccionario con el inventario
            a evaluar. Cada producto debe contener un subdiccionario con la
            clave "fecha_caducidad" (en formato: "AAAA-MM-DD" o None).
            Si es None, evalúa la despensa global

    Returns:
        _type_: Un diccionario estructurado con tres categorías principales:
            - "caduca_hoy" (list): Nombres de productos que vencen el día
                de referencia.
            - "ya_caducado" (list): Nombres de productos cuya fecha es
                anterior a la referencia.
            - "caduca_en_2_dias" (list): Nombres de productos que vencen
                en los próximos 3 días.
    """
    alertas_caducidad = {
        "caduca_hoy": [],
        "ya_caducado": [],
        "caduca_en_2_dias": []
    }
    if despensa_a_inspeccionar is None:
        despensa_a_inspeccionar = despensa
    for producto in despensa_a_inspeccionar:
        if despensa_a_inspeccionar[producto]["fecha_caducidad"] is None:
            continue
        else:
            fecha_caducidad_producto = datetime.strptime(
                despensa_a_inspeccionar[producto]["fecha_caducidad"], "%Y-%m-%d")
            diferencia = fecha_caducidad_producto - fecha_hoy
            if diferencia.days == 0:
                alertas_caducidad["caduca_hoy"].append(producto)
            elif diferencia.days < 0:
                alertas_caducidad["ya_caducado"].append(producto)
            elif 0 < diferencia.days <= 3:
                alertas_caducidad["caduca_en_2_dias"].append(producto)
    return alertas_caducidad
