from fractions import Fraction

from modulos.utilidades import (
    a_fraccion,
    a_fraccion_str,
    matriz_a_texto,
    convertir_matriz,
    convertir_vector,
    validar_matriz
)


# ============================================================
# MÓDULO 3
# MATRICES Y OPERACIONES
# ============================================================

LOGO_MATRICES = """
======================================================
   [ a  b ]       MÓDULO: MATRICES
   [ c  d ]       Operaciones y producto Ax
======================================================
"""


# ============================================================
# DIMENSIONES
# ============================================================

def dimensiones_matriz(A):
    """
    Retorna las dimensiones de una matriz.

    Resultado:
        filas, columnas
    """

    validar_matriz(A)

    return len(A), len(A[0])


# ============================================================
# VALIDACIONES
# ============================================================

def validar_misma_dimension(A, B):
    """
    Comprueba que A y B tengan exactamente
    la misma cantidad de filas y columnas.
    """

    validar_matriz(A)
    validar_matriz(B)

    filas_a, columnas_a = dimensiones_matriz(A)
    filas_b, columnas_b = dimensiones_matriz(B)

    if (
        filas_a != filas_b
        or
        columnas_a != columnas_b
    ):
        raise ValueError(
            "Las matrices deben tener las mismas "
            "dimensiones para realizar esta operación."
        )

    return True


def validar_multiplicacion(A, B):
    """
    Para que A · B exista:

        columnas de A = filas de B
    """

    validar_matriz(A)
    validar_matriz(B)

    filas_a, columnas_a = dimensiones_matriz(A)
    filas_b, columnas_b = dimensiones_matriz(B)

    if columnas_a != filas_b:
        raise ValueError(
            "No se pueden multiplicar las matrices.\n"
            "El número de columnas de A debe ser igual "
            "al número de filas de B."
        )

    return True


# ============================================================
# SUMA DE MATRICES
# ============================================================

def sumar_matrices(A, B):
    """
    Calcula:

        A + B

    elemento por elemento.

    Retorna:
        resultado
        pasos
    """

    validar_misma_dimension(A, B)

    A = convertir_matriz(A)
    B = convertir_matriz(B)

    filas = len(A)
    columnas = len(A[0])

    resultado = []
    pasos = []

    pasos.append(
        "SUMA DE MATRICES"
    )

    pasos.append(
        "Para sumar dos matrices deben tener "
        "las mismas dimensiones."
    )

    pasos.append(
        "A es de orden "
        + str(filas)
        + " × "
        + str(columnas)
        + " y B también."
    )

    pasos.append(
        "Matriz A:\n\n"
        + matriz_a_texto(A)
    )

    pasos.append(
        "Matriz B:\n\n"
        + matriz_a_texto(B)
    )

    pasos.append(
        "Sumamos los elementos que ocupan "
        "la misma posición."
    )

    for i in range(filas):

        fila_resultado = []

        for j in range(columnas):

            valor = A[i][j] + B[i][j]

            fila_resultado.append(valor)

            pasos.append(
                "Posición ("
                + str(i + 1)
                + ", "
                + str(j + 1)
                + "):\n"
                + a_fraccion_str(A[i][j])
                + " + "
                + a_fraccion_str(B[i][j])
                + " = "
                + a_fraccion_str(valor)
            )

        resultado.append(
            fila_resultado
        )

    pasos.append(
        "RESULTADO:\n\n"
        + matriz_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# RESTA DE MATRICES
# ============================================================

def restar_matrices(A, B):
    """
    Calcula:

        A - B
    """

    validar_misma_dimension(A, B)

    A = convertir_matriz(A)
    B = convertir_matriz(B)

    filas = len(A)
    columnas = len(A[0])

    resultado = []
    pasos = []

    pasos.append(
        "RESTA DE MATRICES"
    )

    pasos.append(
        "Para restar matrices deben tener "
        "las mismas dimensiones."
    )

    pasos.append(
        "Restamos los elementos correspondientes "
        "posición por posición."
    )

    for i in range(filas):

        fila_resultado = []

        for j in range(columnas):

            valor = A[i][j] - B[i][j]

            fila_resultado.append(valor)

            pasos.append(
                "Posición ("
                + str(i + 1)
                + ", "
                + str(j + 1)
                + "):\n"
                + a_fraccion_str(A[i][j])
                + " - "
                + a_fraccion_str(B[i][j])
                + " = "
                + a_fraccion_str(valor)
            )

        resultado.append(
            fila_resultado
        )

    pasos.append(
        "RESULTADO:\n\n"
        + matriz_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# MULTIPLICACIÓN DE MATRIZ POR ESCALAR
# ============================================================

def multiplicar_matriz_escalar(escalar, A):
    """
    Calcula:

        cA
    """

    validar_matriz(A)

    A = convertir_matriz(A)
    c = a_fraccion(escalar)

    filas = len(A)
    columnas = len(A[0])

    resultado = []
    pasos = []

    pasos.append(
        "MULTIPLICACIÓN DE UNA MATRIZ POR UN ESCALAR"
    )

    pasos.append(
        "Escalar:\n"
        + a_fraccion_str(c)
    )

    pasos.append(
        "Multiplicamos cada elemento de A "
        "por el escalar."
    )

    for i in range(filas):

        fila_resultado = []

        for j in range(columnas):

            valor = c * A[i][j]

            fila_resultado.append(valor)

            pasos.append(
                "Posición ("
                + str(i + 1)
                + ", "
                + str(j + 1)
                + "):\n"
                + a_fraccion_str(c)
                + "("
                + a_fraccion_str(A[i][j])
                + ") = "
                + a_fraccion_str(valor)
            )

        resultado.append(
            fila_resultado
        )

    pasos.append(
        "RESULTADO:\n\n"
        + matriz_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# MULTIPLICACIÓN DE MATRICES
# ============================================================

def multiplicar_matrices(A, B):
    """
    Calcula:

        AB

    utilizando producto fila por columna.

    Cada entrada c_ij se obtiene mediante:

        c_ij =
        a_i1 b_1j +
        a_i2 b_2j +
        ... +
        a_in b_nj
    """

    validar_multiplicacion(A, B)

    A = convertir_matriz(A)
    B = convertir_matriz(B)

    filas_a = len(A)
    columnas_a = len(A[0])

    filas_b = len(B)
    columnas_b = len(B[0])

    resultado = []
    pasos = []

    pasos.append(
        "MULTIPLICACIÓN DE MATRICES"
    )

    pasos.append(
        "A tiene orden "
        + str(filas_a)
        + " × "
        + str(columnas_a)
        + "."
    )

    pasos.append(
        "B tiene orden "
        + str(filas_b)
        + " × "
        + str(columnas_b)
        + "."
    )

    pasos.append(
        "Como el número de columnas de A ("
        + str(columnas_a)
        + ") es igual al número de filas de B ("
        + str(filas_b)
        + "), el producto AB está definido."
    )

    pasos.append(
        "El resultado tendrá orden "
        + str(filas_a)
        + " × "
        + str(columnas_b)
        + "."
    )

    pasos.append(
        "Matriz A:\n\n"
        + matriz_a_texto(A)
    )

    pasos.append(
        "Matriz B:\n\n"
        + matriz_a_texto(B)
    )

    pasos.append(
        "Cada elemento del resultado se obtiene "
        "multiplicando una fila de A por una "
        "columna de B."
    )

    for i in range(filas_a):

        fila_resultado = []

        for j in range(columnas_b):

            suma = Fraction(0, 1)
            productos = []

            for k in range(columnas_a):

                producto = (
                    A[i][k]
                    * B[k][j]
                )

                suma += producto

                productos.append(
                    "("
                    + a_fraccion_str(A[i][k])
                    + ")("
                    + a_fraccion_str(B[k][j])
                    + ")"
                )

            fila_resultado.append(suma)

            pasos.append(
                "Elemento ("
                + str(i + 1)
                + ", "
                + str(j + 1)
                + "):\n"
                + " + ".join(productos)
                + " = "
                + a_fraccion_str(suma)
            )

        resultado.append(
            fila_resultado
        )

    pasos.append(
        "RESULTADO AB:\n\n"
        + matriz_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# PRODUCTO MATRIZ POR VECTOR
# ============================================================

def multiplicar_matriz_vector(A, x):
    """
    Calcula:

        Ax

    donde x es un vector columna.

    Esta operación también sirve para verificar
    soluciones de sistemas de ecuaciones.
    """

    validar_matriz(A)

    A = convertir_matriz(A)
    x = convertir_vector(x)

    filas = len(A)
    columnas = len(A[0])

    if len(x) != columnas:

        raise ValueError(
            "No se puede calcular Ax.\n"
            "El vector x debe tener "
            + str(columnas)
            + " componentes."
        )

    resultado = []
    pasos = []

    pasos.append(
        "PRODUCTO MATRIZ POR VECTOR"
    )

    pasos.append(
        "Queremos calcular:\n\n"
        "Ax"
    )

    pasos.append(
        "A tiene "
        + str(columnas)
        + " columnas y x tiene "
        + str(len(x))
        + " componentes, por lo tanto "
        "el producto está definido."
    )

    pasos.append(
        "Matriz A:\n\n"
        + matriz_a_texto(A)
    )

    pasos.append(
        "Vector x:\n\n"
        + "\n".join(
            "[ " + a_fraccion_str(valor) + " ]"
            for valor in x
        )
    )

    for i in range(filas):

        suma = Fraction(0, 1)
        productos = []

        for j in range(columnas):

            producto = (
                A[i][j]
                * x[j]
            )

            suma += producto

            productos.append(
                "("
                + a_fraccion_str(A[i][j])
                + ")("
                + a_fraccion_str(x[j])
                + ")"
            )

        resultado.append(suma)

        pasos.append(
            "Componente "
            + str(i + 1)
            + " de Ax:\n"
            + " + ".join(productos)
            + " = "
            + a_fraccion_str(suma)
        )

    pasos.append(
        "RESULTADO Ax:\n\n"
        + "\n".join(
            "[ " + a_fraccion_str(valor) + " ]"
            for valor in resultado
        )
    )

    return resultado, pasos


# ============================================================
# TRANSPUESTA
# ============================================================

def transponer_matriz(A):
    """
    Calcula la matriz transpuesta:

        A^T

    Las filas de A se convierten en columnas.
    """

    validar_matriz(A)

    A = convertir_matriz(A)

    filas = len(A)
    columnas = len(A[0])

    resultado = []

    for j in range(columnas):

        nueva_fila = []

        for i in range(filas):

            nueva_fila.append(
                A[i][j]
            )

        resultado.append(
            nueva_fila
        )

    pasos = []

    pasos.append(
        "TRANSPUESTA DE UNA MATRIZ"
    )

    pasos.append(
        "La matriz A tiene orden "
        + str(filas)
        + " × "
        + str(columnas)
        + "."
    )

    pasos.append(
        "Para obtener Aᵀ, las filas de A "
        "se convierten en columnas."
    )

    pasos.append(
        "Matriz A:\n\n"
        + matriz_a_texto(A)
    )

    pasos.append(
        "Matriz Aᵀ:\n\n"
        + matriz_a_texto(resultado)
    )

    pasos.append(
        "Por tanto, Aᵀ tiene orden "
        + str(columnas)
        + " × "
        + str(filas)
        + "."
    )

    return resultado, pasos


# ============================================================
# MATRIZ IDENTIDAD
# ============================================================

def matriz_identidad(n):
    """
    Construye la matriz identidad I_n.
    """

    if n <= 0:
        raise ValueError(
            "El tamaño de la matriz identidad "
            "debe ser mayor que cero."
        )

    I = []

    for i in range(n):

        fila = []

        for j in range(n):

            if i == j:
                fila.append(
                    Fraction(1, 1)
                )
            else:
                fila.append(
                    Fraction(0, 1)
                )

        I.append(fila)

    return I


# ============================================================
# MATRIZ CERO
# ============================================================

def matriz_cero(filas, columnas):
    """
    Construye una matriz cero de orden:

        filas × columnas
    """

    if filas <= 0 or columnas <= 0:

        raise ValueError(
            "Las dimensiones de la matriz "
            "deben ser mayores que cero."
        )

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            fila.append(
                Fraction(0, 1)
            )

        resultado.append(fila)

    return resultado


# ============================================================
# COMPARACIÓN DE MATRICES
# ============================================================

def matrices_iguales(A, B):
    """
    Comprueba si dos matrices son iguales.
    """

    validar_matriz(A)
    validar_matriz(B)

    if len(A) != len(B):
        return False

    if len(A[0]) != len(B[0]):
        return False

    A = convertir_matriz(A)
    B = convertir_matriz(B)

    for i in range(len(A)):

        for j in range(len(A[0])):

            if A[i][j] != B[i][j]:
                return False

    return True