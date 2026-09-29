from fractions import Fraction


# ============================================================
# PRESENTACIÓN MATEMÁTICA
# ============================================================

def a_subindice(numero):
    """
    Convierte números normales a subíndices Unicode.

    Ejemplos:
    1  -> ₁
    12 -> ₁₂
    """

    tabla = str.maketrans(
        "0123456789",
        "₀₁₂₃₄₅₆₇₈₉"
    )

    return str(numero).translate(tabla)


def variable(indice):
    """
    Genera el nombre matemático de una variable.

    Ejemplo:
    variable(1) -> x₁
    """

    return "x" + a_subindice(indice)


def nombre_fila(indice):
    """
    Genera el nombre matemático de una fila.

    Ejemplo:
    nombre_fila(2) -> F₂
    """

    return "F" + a_subindice(indice)


# ============================================================
# FRACCIONES Y ENTRADA DE DATOS
# ============================================================

def parsear_entrada(texto):
    """
    Convierte la entrada del usuario en una fracción exacta.

    Permite ingresar:
    5
    -3
    1/2
    -7/4
    2.5
    2,5

    Fraction permite mantener resultados exactos durante
    las operaciones algebraicas.
    """

    if texto is None:
        raise ValueError("Celda vacía.")

    texto = str(texto).strip()

    if texto == "":
        raise ValueError("Celda vacía.")

    texto = texto.replace(",", ".")

    try:
        return Fraction(texto).limit_denominator(1000000)

    except (ValueError, ZeroDivisionError):
        raise ValueError(
            "El valor '"
            + str(texto)
            + "' no es un número o una fracción válida."
        )


def a_fraccion(valor):
    """
    Convierte cualquier valor numérico recibido por
    el programa a Fraction.
    """

    if isinstance(valor, Fraction):
        return valor

    if isinstance(valor, str):
        return parsear_entrada(valor)

    if isinstance(valor, int):
        return Fraction(valor, 1)

    return Fraction(valor).limit_denominator(1000000)


def a_fraccion_str(valor):
    """
    Convierte una Fraction a una representación legible.

    Ejemplos:
    4/1 -> 4
    3/2 -> 3/2
    """

    valor = a_fraccion(valor)

    if valor.denominator == 1:
        return str(valor.numerator)

    return (
        str(valor.numerator)
        + "/"
        + str(valor.denominator)
    )


# ============================================================
# REPRESENTACIÓN DE VECTORES Y MATRICES
# ============================================================

def vector_a_texto(vector):
    """
    Convierte un vector en texto vertical.
    """

    texto = ""

    for valor in vector:
        texto += "[ " + a_fraccion_str(valor) + " ]\n"

    return texto.rstrip()


def matriz_a_texto(matriz):
    """
    Convierte una matriz en una representación de texto.
    """

    lineas = []

    for fila in matriz:

        valores = []

        for valor in fila:
            valores.append(
                a_fraccion_str(valor)
            )

        lineas.append(
            "[ " + "   ".join(valores) + " ]"
        )

    return "\n".join(lineas)


# ============================================================
# COPIA Y CONVERSIÓN
# ============================================================

def copiar_matriz(matriz):
    """
    Realiza una copia independiente de una matriz.

    Evita modificar accidentalmente la matriz original
    cuando se realizan operaciones elementales.
    """

    copia = []

    for fila in matriz:
        copia.append(fila[:])

    return copia


def convertir_matriz(matriz):
    """
    Convierte todos los elementos de una matriz a Fraction.
    """

    resultado = []

    for fila in matriz:

        nueva_fila = []

        for valor in fila:
            nueva_fila.append(
                a_fraccion(valor)
            )

        resultado.append(
            nueva_fila
        )

    return resultado


def convertir_vector(vector):
    """
    Convierte todos los elementos de un vector a Fraction.
    """

    resultado = []

    for valor in vector:
        resultado.append(
            a_fraccion(valor)
        )

    return resultado


# ============================================================
# VALIDACIONES
# ============================================================

def validar_matriz(matriz):
    """
    Comprueba que una matriz tenga filas y columnas
    y que todas sus filas tengan la misma longitud.
    """

    if len(matriz) == 0:
        raise ValueError(
            "La matriz no puede estar vacía."
        )

    if len(matriz[0]) == 0:
        raise ValueError(
            "La matriz debe tener columnas."
        )

    columnas = len(matriz[0])

    for fila in matriz:

        if len(fila) != columnas:
            raise ValueError(
                "Todas las filas de la matriz "
                "deben tener la misma cantidad "
                "de elementos."
            )

    return True


def validar_vector(vector):
    """
    Comprueba que un vector tenga al menos
    una componente.
    """

    if vector is None or len(vector) == 0:
        raise ValueError(
            "El vector no puede estar vacío."
        )

    return True


def validar_vectores_misma_dimension(vectores):
    """
    Comprueba que todos los vectores de una colección
    tengan la misma dimensión.

    Esta función será especialmente útil para el
    Programa 4 de Independencia Lineal.
    """

    if vectores is None or len(vectores) == 0:
        raise ValueError(
            "Debe ingresar al menos un vector."
        )

    dimension = len(vectores[0])

    if dimension == 0:
        raise ValueError(
            "Los vectores deben tener al menos una componente."
        )

    for vector in vectores:

        if len(vector) != dimension:
            raise ValueError(
                "Todos los vectores deben tener "
                "la misma dimensión."
            )

    return True