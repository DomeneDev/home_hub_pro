"""Módulo de transacciones e inventario para el sistema Home Hub Pro.

Este módulo centraliza las operaciones del día a día sobre el stock de la despensa,
permitiendo actualizar dinámicamente las existencias disponibles mediante el registro
de nuevas compras (entradas) o el descuento por consumo doméstico (salidas).

Funciones incluidas:
    * registrar_compra: Incrementa las unidades de un producto mediante su SKU.
    * consumir_producto: Disminuye las unidades disponibles de un artículo específico.
"""

from src.core.inventario import despensa


def registrar_compra(sku: str, cantidad: float, despensa_a_modificar: dict = None):
    """Registra la entrada de un producto a la despensa incrementando su stock
    actual.

    Busca el articulo mediante su código identificador único (SKU) y añade la
    cantidad al inventario. Si no se proporciona una despensa especifica, las
    modificaciones se aplicarán sobre la despensa global del sistemas.

    Args:
        sku (str): Código identificador único del producto que se va a reponer.
            Ejemplo "ACEITE-001"
        cantidad (float): Cantidad o unidades del producto ingresados.
        despensa_a_modificiar (dict, optional): Diccionario que representa el
            inventario donde se va a realizar la actualización.
            Por defecto es None (usa la depensa global del sistema).
    """
    if despensa_a_modificar is None:
        despensa_a_modificar = despensa
    if sku not in despensa_a_modificar:
        print(f"¡¡¡ERROR: producto {sku}, no existe en el inventario!!!")
    else:
        despensa_a_modificar[sku]["cantidad_actual"] += cantidad


def consumir_producto(sku: str, cantidad: float, despensa_a_modificar: dict = None):
    """Registra la salida o consumo de un producto reduciendo su stock actual.

    Disminuye las existencias disponibles de un artículo específico en base a su SKU.
    Suele utilizarse para el control diario del hogar y puede requerir lógica adicional
    para evitar que las existencias adquieran valores negativos.

    Args:
        sku (str): Código identificador único del producto que se ha consumido.
        cantidad (float): Cantidad o unidades que se van a descontar del inventario.
        despensa_a_modificar (dict, optional): Diccionario que representa el inventario
            donde se descontará el producto. Por defecto es None (usa la despensa global).
    """
    if despensa_a_modificar is None:
        despensa_a_modificar = despensa
    if sku not in despensa_a_modificar:
        print(f"¡¡¡ERROR: producto {sku}, no existe en el inventario!!!")
    else:
        if despensa_a_modificar[sku]["cantidad_actual"] < cantidad:
            print(
                f"¡¡¡ERROR: No hay stock suficiente de {sku} para realizar esta acción")
        else:
            despensa_a_modificar[sku]["cantidad_actual"] -= cantidad
