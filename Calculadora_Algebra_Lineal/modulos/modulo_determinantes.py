from modulos.utilidades import  (
    convertir_matriz,
    validar_matriz
)


# ============================================================
# MÓDULO 4
# DETERMINANTES
# ============================================================

LOGO_DETERMINANTES = """
======================================================
   | a  b |
   | c  d |       MÓDULO: DETERMINANTES
                Próximamente: determinantes e inversa
======================================================
"""


# ============================================================
# VALIDACIÓN DE MATRIZ CUADRADA
# ============================================================

def es_matriz_cuadrada(A):
    """
    Determina si una matriz es cuadrada.

    Una matriz es cuadrada cuando:

        número de filas = número de columnas
    """

    validar_matriz(A)

    filas = len(A)
    columnas = len(A[0])

    return filas == columnas


def validar_matriz_cuadrada(A):
    """
    Comprueba que una matriz sea cuadrada.

    Los determinantes solamente están definidos
    para matrices cuadradas.
    """

    validar_matriz(A)

    if not es_matriz_cuadrada(A):

        filas = len(A)
        columnas = len(A[0])

        raise ValueError(
            "No se puede calcular el determinante.\n"
            "La matriz es de orden "
            + str(filas)
            + " × "
            + str(columnas)
            + " y no es cuadrada."
        )

    return True


# ============================================================
# INFORMACIÓN DEL MÓDULO
# ============================================================

def informacion_modulo():
    """
    Devuelve información sobre el estado actual
    del módulo de determinantes.

    Este módulo queda preparado para integrar
    posteriormente los programas correspondientes
    a determinantes e inversa.
    """

    return [
        "MÓDULO DE DETERMINANTES",
        "",
        "Este módulo forma parte de la estructura "
        "general de la Calculadora de Álgebra Lineal.",
        "",
        "Actualmente se encuentra preparado para "
        "incorporar las operaciones de determinantes "
        "que correspondan a las próximas tareas.",
        "",
        "No se agregan todavía métodos de cálculo "
        "que no hayan sido solicitados en el proyecto."
    ]