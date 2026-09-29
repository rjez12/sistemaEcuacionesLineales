from fractions import Fraction

from modulos.utilidades import (
    a_subindice,
    variable,
    a_fraccion_str,
    vector_a_texto,
    matriz_a_texto,
    convertir_vector,
    convertir_matriz,
    copiar_matriz,
    validar_vector,
    validar_vectores_misma_dimension
)

from modulos.modulo_sistemas import (
    gauss_jordan_rref,
    construir_solucion_general
)


# ============================================================
# MÓDULO 2
# VECTORES E INDEPENDENCIA LINEAL
# ============================================================

LOGO_VECTORES = """
======================================================
   →u   →v
    \\   /
     \\ /
      •       MÓDULO: VECTORES E INDEPENDENCIA LINEAL
     / \\
    /   \\      Combinaciones lineales, L.I./L.D., Ax = 0
======================================================
"""


# ============================================================
# VALIDACIONES GENERALES
# ============================================================

def validar_dos_vectores(u, v):
    """
    Comprueba que dos vectores sean válidos
    y tengan la misma dimensión.
    """

    validar_vector(u)
    validar_vector(v)

    if len(u) != len(v):
        raise ValueError(
            "Los vectores deben tener la misma dimensión."
        )

    return True


# ============================================================
# SUMA DE VECTORES
# ============================================================

def sumar_vectores(u, v):
    """
    Calcula:

        u + v

    componente por componente.

    Retorna:
        resultado
        pasos
    """

    validar_dos_vectores(u, v)

    u = convertir_vector(u)
    v = convertir_vector(v)

    resultado = []
    pasos = []

    pasos.append(
        "SUMA DE VECTORES"
    )

    pasos.append(
        "Los vectores tienen dimensión "
        + str(len(u))
        + ", por lo tanto pueden sumarse."
    )

    pasos.append(
        "La suma de vectores se realiza "
        "componente por componente."
    )

    for i in range(len(u)):

        valor = u[i] + v[i]

        resultado.append(valor)

        pasos.append(
            "Componente "
            + str(i + 1)
            + ":\n"
            + a_fraccion_str(u[i])
            + " + "
            + a_fraccion_str(v[i])
            + " = "
            + a_fraccion_str(valor)
        )

    pasos.append(
        "Resultado:\n"
        + vector_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# RESTA DE VECTORES
# ============================================================

def restar_vectores(u, v):
    """
    Calcula:

        u - v

    componente por componente.
    """

    validar_dos_vectores(u, v)

    u = convertir_vector(u)
    v = convertir_vector(v)

    resultado = []
    pasos = []

    pasos.append(
        "RESTA DE VECTORES"
    )

    pasos.append(
        "Los vectores tienen la misma dimensión."
    )

    pasos.append(
        "La resta se realiza componente por componente."
    )

    for i in range(len(u)):

        valor = u[i] - v[i]

        resultado.append(valor)

        pasos.append(
            "Componente "
            + str(i + 1)
            + ":\n"
            + a_fraccion_str(u[i])
            + " - "
            + a_fraccion_str(v[i])
            + " = "
            + a_fraccion_str(valor)
        )

    pasos.append(
        "Resultado:\n"
        + vector_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# MULTIPLICACIÓN DE VECTOR POR ESCALAR
# ============================================================

def multiplicar_vector_escalar(escalar, vector):
    """
    Calcula:

        c · v
    """

    validar_vector(vector)

    vector = convertir_vector(vector)

    if isinstance(escalar, Fraction):
        c = escalar
    else:
        c = Fraction(escalar)

    resultado = []
    pasos = []

    pasos.append(
        "MULTIPLICACIÓN DE UN VECTOR POR UN ESCALAR"
    )

    pasos.append(
        "Escalar utilizado: "
        + a_fraccion_str(c)
    )

    pasos.append(
        "Cada componente del vector se multiplica "
        "por el mismo escalar."
    )

    for i in range(len(vector)):

        valor = c * vector[i]

        resultado.append(valor)

        pasos.append(
            "Componente "
            + str(i + 1)
            + ":\n"
            + a_fraccion_str(c)
            + "("
            + a_fraccion_str(vector[i])
            + ") = "
            + a_fraccion_str(valor)
        )

    pasos.append(
        "Resultado:\n"
        + vector_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# COMBINACIÓN LINEAL CON COEFICIENTES CONOCIDOS
# ============================================================

def combinacion_lineal(vectores, escalares):
    """
    Calcula una combinación lineal:

        c1*v1 + c2*v2 + ... + ck*vk

    cuando los escalares ya son conocidos.
    """

    validar_vectores_misma_dimension(vectores)

    if len(vectores) != len(escalares):
        raise ValueError(
            "Debe existir un escalar por cada vector."
        )

    vectores_convertidos = []

    for v in vectores:
        vectores_convertidos.append(
            convertir_vector(v)
        )

    escalares_convertidos = []

    for escalar in escalares:

        if isinstance(escalar, Fraction):
            escalares_convertidos.append(escalar)
        else:
            escalares_convertidos.append(
                Fraction(escalar)
            )

    dimension = len(
        vectores_convertidos[0]
    )

    resultado = [
        Fraction(0, 1)
        for _ in range(dimension)
    ]

    pasos = []

    pasos.append(
        "COMBINACIÓN LINEAL"
    )

    pasos.append(
        "Calculamos:\n"
        "c₁v₁ + c₂v₂ + ... + cₖvₖ"
    )

    for j in range(
        len(vectores_convertidos)
    ):

        pasos.append(
            "Multiplicamos v"
            + a_subindice(j + 1)
            + " por "
            + a_fraccion_str(
                escalares_convertidos[j]
            )
            + "."
        )

        for i in range(dimension):

            resultado[i] += (
                escalares_convertidos[j]
                * vectores_convertidos[j][i]
            )

    pasos.append(
        "Sumando las componentes obtenemos:\n"
        + vector_a_texto(resultado)
    )

    return resultado, pasos


# ============================================================
# CONSTRUIR MATRIZ A A PARTIR DE VECTORES
# ============================================================

def construir_matriz_desde_vectores(vectores):
    """
    Construye:

        A = [v1 v2 ... vk]

    colocando cada vector como una COLUMNA.

    Esto es fundamental para combinación lineal
    e independencia lineal.
    """

    validar_vectores_misma_dimension(
        vectores
    )

    vectores_convertidos = []

    for vector_actual in vectores:

        vectores_convertidos.append(
            convertir_vector(vector_actual)
        )

    dimension = len(
        vectores_convertidos[0]
    )

    cantidad_vectores = len(
        vectores_convertidos
    )

    A = []

    for i in range(dimension):

        fila = []

        for j in range(
            cantidad_vectores
        ):

            fila.append(
                vectores_convertidos[j][i]
            )

        A.append(fila)

    return A


# ============================================================
# ¿b ES COMBINACIÓN LINEAL?
# ============================================================

def verificar_combinacion_lineal(vectores, b):
    """
    Determina si:

        b ∈ Span{v1, v2, ..., vk}

    resolviendo:

        A x = b

    donde:

        A = [v1 v2 ... vk]

    Retorna información suficiente para que
    la interfaz muestre el procedimiento completo.
    """

    validar_vectores_misma_dimension(
        vectores
    )

    validar_vector(b)

    b = convertir_vector(b)

    dimension = len(vectores[0])

    if len(b) != dimension:

        raise ValueError(
            "El vector objetivo debe tener "
            "la misma dimensión que los vectores dados."
        )

    A = construir_matriz_desde_vectores(
        vectores
    )

    m = len(A)
    n = len(A[0])

    Ab = []

    for i in range(m):

        fila = A[i][:]

        fila.append(
            b[i]
        )

        Ab.append(fila)

    rref, pivotes, pasos_reduccion, inconsistente = (
        gauss_jordan_rref(
            m,
            n,
            Ab
        )
    )

    basicas, libres, solucion = (
        construir_solucion_general(
            m,
            n,
            rref,
            pivotes
        )
    )

    explicacion = []

    explicacion.append(
        "COMBINACIÓN LINEAL"
    )

    explicacion.append(
        "Queremos determinar si el vector b "
        "puede escribirse como:"
    )

    expresion = ""

    for i in range(n):

        if i > 0:
            expresion += " + "

        expresion += (
            "c"
            + a_subindice(i + 1)
            + "v"
            + a_subindice(i + 1)
        )

    expresion += " = b"

    explicacion.append(
        expresion
    )

    explicacion.append(
        "Colocamos los vectores como columnas "
        "de la matriz A."
    )

    explicacion.append(
        "Matriz A:\n"
        + matriz_a_texto(A)
    )

    explicacion.append(
        "Construimos la matriz aumentada [A | b]:\n"
        + matriz_a_texto(Ab)
    )

    if inconsistente:

        pertenece = False

        explicacion.append(
            "La reducción produjo una contradicción."
        )

        explicacion.append(
            "Por lo tanto, el sistema Ax = b "
            "no tiene solución."
        )

        explicacion.append(
            "CONCLUSIÓN:\n"
            "b NO es combinación lineal "
            "de los vectores dados."
        )

    else:

        pertenece = True

        explicacion.append(
            "El sistema Ax = b es consistente."
        )

        explicacion.append(
            "Por lo tanto, existen coeficientes "
            "que permiten expresar b utilizando "
            "los vectores dados."
        )

        explicacion.append(
            "CONCLUSIÓN:\n"
            "b SÍ es combinación lineal "
            "de los vectores dados."
        )

    return {
        "pertenece": pertenece,
        "A": A,
        "Ab": Ab,
        "rref": rref,
        "pivotes": pivotes,
        "variables_basicas": basicas,
        "variables_libres": libres,
        "solucion": solucion,
        "pasos_reduccion": pasos_reduccion,
        "explicacion": explicacion
    }


# ============================================================
# PROGRAMA 4
# INDEPENDENCIA LINEAL
# ============================================================

def analizar_independencia_lineal(vectores):
    """
    Determina si un conjunto:

        {v1, v2, ..., vk}

    es linealmente independiente o dependiente.

    Procedimiento:

    1. Construir A = [v1 v2 ... vk].
    2. Plantear Ax = 0.
    3. Reducir mediante Gauss-Jordan.
    4. Localizar columnas pivote.
    5. Detectar variables libres.
    6. Analizar si Ax = 0 tiene únicamente
       la solución trivial.

    Si no existen variables libres:
        L.I.

    Si existe al menos una variable libre:
        L.D.
    """

    validar_vectores_misma_dimension(
        vectores
    )

    cantidad_vectores = len(
        vectores
    )

    dimension = len(
        vectores[0]
    )

    # --------------------------------------------------------
    # PASO 1
    # Construir A con los vectores como columnas.
    # --------------------------------------------------------

    A = construir_matriz_desde_vectores(
        vectores
    )

    # --------------------------------------------------------
    # PASO 2
    # Construir [A | 0].
    # --------------------------------------------------------

    Ab = []

    for fila in A:

        nueva_fila = fila[:]

        nueva_fila.append(
            Fraction(0, 1)
        )

        Ab.append(
            nueva_fila
        )

    m = dimension
    n = cantidad_vectores

    # --------------------------------------------------------
    # PASO 3
    # Obtener RREF.
    # --------------------------------------------------------

    rref, pivotes, pasos_reduccion, inconsistente = (
        gauss_jordan_rref(
            m,
            n,
            Ab
        )
    )

    # En un sistema homogéneo Ax = 0 no debería
    # aparecer inconsistencia.
    # Conservamos la variable como comprobación interna.

    # --------------------------------------------------------
    # PASO 4
    # Determinar columnas pivote.
    # --------------------------------------------------------

    columnas_pivote = []

    for fila, columna in pivotes:

        if (
            columna < n
            and
            columna not in columnas_pivote
        ):

            columnas_pivote.append(
                columna
            )

    # --------------------------------------------------------
    # PASO 5
    # Determinar variables básicas y libres.
    # --------------------------------------------------------

    variables_basicas = []
    variables_libres = []

    for columna in range(n):

        if columna in columnas_pivote:

            variables_basicas.append(
                columna
            )

        else:

            variables_libres.append(
                columna
            )

    numero_pivotes = len(
        columnas_pivote
    )

    numero_libres = len(
        variables_libres
    )

    # --------------------------------------------------------
    # PASO 6
    # Criterio de independencia lineal.
    # --------------------------------------------------------

    es_independiente = (
        numero_libres == 0
    )

    # --------------------------------------------------------
    # Solución general de Ax = 0
    # --------------------------------------------------------

    basicas_solucion, libres_solucion, solucion = (
        construir_solucion_general(
            m,
            n,
            rref,
            pivotes
        )
    )

    # --------------------------------------------------------
    # EXPLICACIÓN COMPLETA
    # --------------------------------------------------------

    explicacion = []

    explicacion.append(
        "PROGRAMA 4 — INDEPENDENCIA LINEAL"
    )

    explicacion.append(
        "Se ingresaron "
        + str(cantidad_vectores)
        + " vectores de dimensión "
        + str(dimension)
        + "."
    )

    explicacion.append(
        "Queremos determinar si el conjunto "
        "de vectores es Linealmente Independiente "
        "(L.I.) o Linealmente Dependiente (L.D.)."
    )

    # --------------------------------------------------------
    # Ecuación vectorial
    # --------------------------------------------------------

    ecuacion = ""

    for i in range(
        cantidad_vectores
    ):

        if i > 0:
            ecuacion += " + "

        ecuacion += (
            "c"
            + a_subindice(i + 1)
            + "v"
            + a_subindice(i + 1)
        )

    ecuacion += " = 0"

    explicacion.append(
        "PASO 1. Planteamos la ecuación de "
        "independencia lineal:\n"
        + ecuacion
    )

    # --------------------------------------------------------
    # Matriz A
    # --------------------------------------------------------

    explicacion.append(
        "PASO 2. Colocamos los vectores como "
        "columnas de la matriz A:\n\n"
        + matriz_a_texto(A)
    )

    explicacion.append(
        "Cada columna de A representa uno "
        "de los vectores del conjunto."
    )

    # --------------------------------------------------------
    # Ax = 0
    # --------------------------------------------------------

    explicacion.append(
        "PASO 3. La ecuación vectorial se "
        "convierte en el sistema homogéneo:\n\n"
        "Ax = 0"
    )

    explicacion.append(
        "Matriz aumentada [A | 0]:\n\n"
        + matriz_a_texto(Ab)
    )

    # --------------------------------------------------------
    # Reducción
    # --------------------------------------------------------

    explicacion.append(
        "PASO 4. Reducimos la matriz mediante "
        "operaciones elementales por filas."
    )

    explicacion.append(
        "Forma escalonada reducida (RREF):\n\n"
        + matriz_a_texto(rref)
    )

    # --------------------------------------------------------
    # Pivotes
    # --------------------------------------------------------

    explicacion.append(
        "PASO 5. Analizamos los pivotes."
    )

    explicacion.append(
        "Número de columnas de A: "
        + str(n)
    )

    explicacion.append(
        "Número de pivotes: "
        + str(numero_pivotes)
    )

    if numero_pivotes > 0:

        texto_pivotes = (
            "Columnas pivote: "
        )

        for i in range(
            len(columnas_pivote)
        ):

            if i > 0:
                texto_pivotes += ", "

            texto_pivotes += str(
                columnas_pivote[i] + 1
            )

        explicacion.append(
            texto_pivotes
        )

    # --------------------------------------------------------
    # Variables básicas
    # --------------------------------------------------------

    if len(variables_basicas) > 0:

        texto_basicas = (
            "Variables básicas: "
        )

        for i in range(
            len(variables_basicas)
        ):

            if i > 0:
                texto_basicas += ", "

            texto_basicas += (
                "c"
                + a_subindice(
                    variables_basicas[i] + 1
                )
            )

        explicacion.append(
            texto_basicas
        )

    # --------------------------------------------------------
    # Variables libres
    # --------------------------------------------------------

    if numero_libres == 0:

        explicacion.append(
            "Variables libres: ninguna."
        )

    else:

        texto_libres = (
            "Variables libres: "
        )

        for i in range(
            len(variables_libres)
        ):

            if i > 0:
                texto_libres += ", "

            texto_libres += (
                "c"
                + a_subindice(
                    variables_libres[i] + 1
                )
            )

        explicacion.append(
            texto_libres
        )

    # --------------------------------------------------------
    # Conclusión
    # --------------------------------------------------------

    if es_independiente:

        explicacion.append(
            "PASO 6. Como existe un pivote "
            "en cada columna, no existen "
            "variables libres."
        )

        solucion_trivial = []

        for i in range(
            cantidad_vectores
        ):

            solucion_trivial.append(
                "c"
                + a_subindice(i + 1)
                + " = 0"
            )

        explicacion.append(
            "El sistema Ax = 0 solamente tiene "
            "la solución trivial:\n\n"
            + "\n".join(solucion_trivial)
        )

        explicacion.append(
            "VEREDICTO:\n"
            "LOS VECTORES SON LINEALMENTE "
            "INDEPENDIENTES (L.I.)."
        )

    else:

        explicacion.append(
            "PASO 6. Como no existe un pivote "
            "en cada columna, aparece al menos "
            "una variable libre."
        )

        explicacion.append(
            "Por lo tanto, Ax = 0 posee "
            "soluciones no triviales."
        )

        explicacion.append(
            "Esto significa que existen "
            "coeficientes, no todos iguales a cero, "
            "que satisfacen:\n\n"
            + ecuacion
        )

        explicacion.append(
            "VEREDICTO:\n"
            "LOS VECTORES SON LINEALMENTE "
            "DEPENDIENTES (L.D.)."
        )

    return {
        "independiente": es_independiente,
        "dependiente": not es_independiente,

        "cantidad_vectores": cantidad_vectores,
        "dimension": dimension,

        "A": A,
        "Ab": Ab,
        "rref": rref,

        "pivotes": pivotes,
        "columnas_pivote": columnas_pivote,
        "numero_pivotes": numero_pivotes,

        "variables_basicas": variables_basicas,
        "variables_libres": variables_libres,
        "numero_variables_libres": numero_libres,

        "solucion": solucion,

        "pasos_reduccion": pasos_reduccion,
        "explicacion": explicacion
    }


# ============================================================
# ALIAS MÁS CORTO PARA LA INTERFAZ
# ============================================================

def independencia_lineal(vectores):
    """
    Alias para analizar_independencia_lineal().
    """

    return analizar_independencia_lineal(
        vectores
    )