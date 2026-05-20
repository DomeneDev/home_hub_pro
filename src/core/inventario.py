"""
Módulo de Gestión de Inventario para el Home Operations Hub.

Este módulo define y administra la estructura de datos central de la despensa.
Utiliza un diccionario anidado donde cada clave única representa un código de 
producto (SKU) y el valor es otro diccionario con los detalles del artículo.

Estructura del Diccionario 'despensa':
-------------------------------------
{
    "CODIGO-PRODUCTO": {
        "nombre": str,            # Nombre descriptivo del producto.
        "categoria": str,         # Categoría de organización (Despensa, Limpieza, etc.).
        "cantidad_actual": int,   # Unidades físicas disponibles en casa.
        "cantidad_minima": int,   # Stock de seguridad antes de necesitar reponer.
        "precio_unitario": float, # Coste estimado por unidad.
        "fecha_caducidad": str    # Fecha en formato 'AAAA-MM-DD' o None si no aplica.
    }
}
"""

despensa = {
    "ACEITE-001": {
        "nombre": "Aceite de oliva", "categoria": "Despensa",
        "cantidad_actual": 5, "cantidad_minima": 1, "precio_unitario": 5,
        "fecha_caducidad": "2028-12-12"
    },
    "SAL-001": {
        "nombre": "Sal de mesa", "categoria": "Despensa",
        "cantidad_actual": 2, "cantidad_minima": 1, "precio_unitario": 1,
        "fecha_caducidad": None
    },
    "FRIEGAPLATOS-001": {
        "nombre": "Friegaplatos Flota", "categoria": "Limpieza",
        "cantidad_actual": 0, "cantidad_minima": 1, "precio_unitario": 1.5,
        "fecha_caducidad": None
    },
    "PASTA-001": {
        "nombre": "Pasta-espaguetti", "categoria": "Pastas",
        "cantidad_actual": 1, "cantidad_minima": 1, "precio_unitario": 1.2,
        "fecha_caducidad": "2026-10-25"
    }
}
