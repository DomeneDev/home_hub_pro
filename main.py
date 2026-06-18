"""Fichero principal de entrada para la aplicación Home Hub Pro.

Este módulo orquesta la interfaz de línea de comandos (CLI) del sistema,
permitiendo al usuario interactuar de manera interactiva con la gestión de la
despensa. Coordina el flujo principal mediante un menú visual para listar el
inventario actual, registrar nuevas compras y descontar productos consumidos.

Funciones incluidas:
    * menu: Renderiza las opciones disponibles en la interfaz visual de la consola.
    * main: Controla el bucle de ejecución, valida las entradas del usuario y
            deriva las acciones hacia la lógica de negocio.
"""

from src.core.core import verificar_conexion
from src.core.inventario import despensa
from src.business_logic.operaciones import registrar_compra, consumir_producto


def menu():
    """Muestra de manera visual las opciones del menú interactivo en la terminal.

    Imprime un encabezado formateado que enumera las acciones disponibles en el
    sistema (Visualización, Registro de compras, Consumo y Salida).
    """
    print("----Menu HomeHubPro----")
    print("-----------------------")
    print(" 1 - Ver despensa")
    print(" 2 - Registrar compra")
    print(" 3 - Consumir producto")
    print(" 4 - Salir")
    print("-----------------------")
    print("\n\n")


def main():
    """Punto de entrada principal que controla el ciclo de vida de la aplicación.

    Inicializa comprobando la conectividad de red y arranca un bucle continuo de
    ejecución. Solicita de forma segura la opción deseada por el usuario (manejando
    excepciones de tipado), y evalúa la selección mediante una estructura de control
    `match-case` para ejecutar los subprocesos correspondientes de inventario o
    finalizar el programa.
    """
    if verificar_conexion():
        print("Status: Conectado a la red exitosamente.\n")
    else:
        print("Status: Modo offline de manera local.\n")

    ejecutando = True
    while ejecutando:
        menu()
        while True:
            try:
                opcion = int(input("Introduce una opción: "))
                print("\n\n")
                break
            except ValueError:
                print("Debe introducir una opción valida")
                print("\n\n")
        match opcion:
            case 1:
                for producto, datos in despensa.items():
                    caducidad_formato = ""
                    if datos["fecha_caducidad"] is None:
                        caducidad_formato = "No perecedero"
                    else:
                        caducidad_formato = datos["fecha_caducidad"]
                    print(
                        f"\t{producto}:\n"
                        + f"- Nombre: {datos["nombre"]}\n"
                        + f"- Categoria: {datos["categoria"]}\n"
                        + f"- Cantidad: {datos["cantidad_actual"]}\n"
                        + f"- Fecha de caducidad: {caducidad_formato}\n"
                        + "-"*30
                    )
                print("\n\n")
            case 2:
                sku = input("Intoduce el identificador de producto").upper()
                cantidad = float(input("Introduce la cantidad: "))
                registrar_compra(sku, cantidad)
                print("\n\n")
            case 3:
                sku = input(
                    "Introduce el identificador del producto: ").upper()
                cantidad = float(input("Introduce la cantidad: "))
                consumir_producto(sku, cantidad)
                print("\n\n")
            case 4:
                print("Saliendo de HomeHubPro....")
                ejecutando = False
            case _:
                print("¡¡¡Error: opción no valida")


if __name__ == "__main__":
    main()
