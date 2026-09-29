from fractions import Fraction

from modulos.utilidades import (
    a_subindice,
    variable,
    nombre_fila,
    a_fraccion_str,
    copiar_matriz,
    convertir_matriz
)


# ============================================================
# MÓDULO 1
# SISTEMAS DE ECUACIONES LINEALES
# ============================================================

LOGO_SISTEMAS = """
======================================================
 [ [1 2 | 3] ] MÓDULO: SISTEMAS DE ECUACIONES (SEL)
 [ [0 1 | 5] ] Métodos: Gauss, Gauss-Jordan
======================================================
"""


# ============================================================
# DETECCIÓN DE PIVOTES
# ============================================================

def detectar_pivotes(m, n, Ab):
    """
    Busca el primer elemento distinto de cero
    en cada fila de una matriz escalonada.

    Retorna las posiciones de los pivotes.
    """

    pivotes = []

    for i in range(m):

        for j in range(n):

            if Ab[i][j] != 0:

                pivotes.append(
                    (i, j)
                )

                break

    return pivotes


# ============================================================
# DETECCIÓN DE INCONSISTENCIA
# ============================================================

def es_inconsistente(m, n, Ab):
    """
    Detecta una fila de la forma:

    [0 0 ... 0 | c]

    donde c != 0.

    Esta fila representa algebraicamente:

    0 = c

    por lo tanto, el sistema es inconsistente.
    """

    for i in range(m):

        coeficientes_cero = True

        for j in range(n):

            if Ab[i][j] != 0:

                coeficientes_cero = False
                break

        if (
            coeficientes_cero
            and
            Ab[i][n] != 0
        ):

            return True, i

    return False, None


# ============================================================
# ELIMINACIÓN GAUSSIANA
# ============================================================

def eliminacion_gaussiana(m, n, Ab_float):
    """
    Aplica eliminación Gaussiana.

    Transforma la matriz aumentada [A | b]
    en una matriz escalonada utilizando
    operaciones elementales entre filas.

    Además guarda cada paso realizado para que
    la interfaz pueda explicar el procedimiento.
    """

    Ab = convertir_matriz(
        Ab_float
    )

    pasos = []
    pivotes_pos = []

    fila_pivote = 0

    pasos.append(
        (
            "info",
            "Comenzamos con la matriz aumentada [A | b].",
            copiar_matriz(Ab)
        )
    )

    for columna in range(n):

        if fila_pivote >= m:
            break

        fila_elegida = -1

        # ----------------------------------------------------
        # Primero buscamos 1 o -1 para simplificar cálculos.
        # ----------------------------------------------------

        for i in range(
            fila_pivote,
            m
        ):

            if (
                Ab[i][columna] == 1
                or
                Ab[i][columna] == -1
            ):

                fila_elegida = i
                break

        # ----------------------------------------------------
        # Si no encontramos 1 o -1, utilizamos cualquier
        # elemento distinto de cero.
        # ----------------------------------------------------

        if fila_elegida == -1:

            for i in range(
                fila_pivote,
                m
            ):

                if Ab[i][columna] != 0:

                    fila_elegida = i
                    break

        # ----------------------------------------------------
        # Si toda la columna contiene ceros, no hay pivote.
        # ----------------------------------------------------

        if fila_elegida == -1:

            pasos.append(
                (
                    "info",

                    "No existe pivote disponible "
                    "en la columna de "
                    + variable(columna + 1)
                    + ". Esta columna puede "
                    "corresponder a una variable libre."
                )
            )

            continue

        # ----------------------------------------------------
        # INTERCAMBIO DE FILAS
        # ----------------------------------------------------

        if fila_elegida != fila_pivote:

            Ab[fila_pivote], Ab[fila_elegida] = (
                Ab[fila_elegida],
                Ab[fila_pivote]
            )

            pasos.append(
                (
                    "pivoteo",

                    "Intercambiamos "
                    + nombre_fila(fila_pivote + 1)
                    + " ↔ "
                    + nombre_fila(fila_elegida + 1)
                    + " para colocar un elemento "
                    + "no nulo en la posición del pivote.",

                    copiar_matriz(Ab)
                )
            )

        pivote = Ab[fila_pivote][columna]

        pasos.append(
            (
                "info",

                "El pivote seleccionado es "
                + a_fraccion_str(pivote)
                + " en la columna correspondiente a "
                + variable(columna + 1)
                + "."
            )
        )

        # ----------------------------------------------------
        # CREAR CEROS DEBAJO DEL PIVOTE
        # ----------------------------------------------------

        for i in range(
            fila_pivote + 1,
            m
        ):

            if Ab[i][columna] == 0:
                continue

            valor_eliminar = Ab[i][columna]

            factor = (
                valor_eliminar
                /
                pivote
            )

            for j in range(
                columna,
                n + 1
            ):

                Ab[i][j] = (
                    Ab[i][j]
                    -
                    factor
                    * Ab[fila_pivote][j]
                )

            pasos.append(
                (
                    "operacion",

                    "Queremos convertir en cero el valor "
                    + a_fraccion_str(valor_eliminar)
                    + " de "
                    + nombre_fila(i + 1)
                    + ".\n\n"

                    + "Factor = "
                    + a_fraccion_str(valor_eliminar)
                    + " / "
                    + a_fraccion_str(pivote)
                    + " = "
                    + a_fraccion_str(factor)
                    + "\n\n"

                    + "Operación elemental:\n"
                    + nombre_fila(i + 1)
                    + " = "
                    + nombre_fila(i + 1)
                    + " - ("
                    + a_fraccion_str(factor)
                    + ")"
                    + nombre_fila(fila_pivote + 1),

                    copiar_matriz(Ab)
                )
            )

        pivotes_pos.append(
            (fila_pivote, columna)
        )

        fila_pivote += 1

    pasos.append(
        (
            "info",

            "La eliminación hacia adelante ha terminado. "
            "Todos los elementos situados debajo "
            "de los pivotes son cero.",

            copiar_matriz(Ab)
        )
    )

    return (
        Ab,
        pasos,
        pivotes_pos
    )


# ============================================================
# SUSTITUCIÓN HACIA ATRÁS
# ============================================================

def sustitucion_hacia_atras(m, n, Ab_float):
    """
    Resuelve un sistema determinado después de
    obtener su matriz escalonada.

    El procedimiento comienza desde la última
    ecuación y continúa hacia arriba.
    """

    Ab = convertir_matriz(
        Ab_float
    )

    inconsistente, fila_error = (
        es_inconsistente(
            m,
            n,
            Ab
        )
    )

    pasos = []

    if inconsistente:

        pasos.append(
            "La fila "
            + str(fila_error + 1)
            + " representa una contradicción."
        )

        return None, pasos

    pivotes = detectar_pivotes(
        m,
        n,
        Ab
    )

    columnas_pivote = []

    for fila, columna in pivotes:

        if columna < n:

            columnas_pivote.append(
                columna
            )

    if len(columnas_pivote) < n:

        pasos.append(
            "Existen variables libres. "
            "La sustitución hacia atrás no produce "
            "una única solución."
        )

        return None, pasos

    solucion = []

    for i in range(n):

        solucion.append(
            Fraction(0, 1)
        )

    # --------------------------------------------------------
    # Recorremos los pivotes desde abajo hacia arriba.
    # --------------------------------------------------------

    for indice in range(
        len(pivotes) - 1,
        -1,
        -1
    ):

        fila = pivotes[indice][0]
        columna = pivotes[indice][1]

        termino_independiente = (
            Ab[fila][n]
        )

        suma_conocida = Fraction(0, 1)

        desarrollo = []

        for j in range(
            columna + 1,
            n
        ):

            if Ab[fila][j] != 0:

                producto = (
                    Ab[fila][j]
                    * solucion[j]
                )

                suma_conocida += producto

                desarrollo.append(
                    "("
                    + a_fraccion_str(Ab[fila][j])
                    + ")("
                    + a_fraccion_str(solucion[j])
                    + ")"
                )

        numerador = (
            termino_independiente
            -
            suma_conocida
        )

        valor = (
            numerador
            /
            Ab[fila][columna]
        )

        solucion[columna] = valor

        texto = (
            "De la ecuación correspondiente a "
            + nombre_fila(fila + 1)
            + ":\n"
        )

        if len(desarrollo) > 0:

            texto += (
                a_fraccion_str(
                    Ab[fila][columna]
                )
                + variable(columna + 1)
                + " + "
                + " + ".join(desarrollo)
                + " = "
                + a_fraccion_str(
                    termino_independiente
                )
                + "\n"
            )

        else:

            texto += (
                a_fraccion_str(
                    Ab[fila][columna]
                )
                + variable(columna + 1)
                + " = "
                + a_fraccion_str(
                    termino_independiente
                )
                + "\n"
            )

        texto += (
            variable(columna + 1)
            + " = ("
            + a_fraccion_str(
                termino_independiente
            )
            + " - "
            + a_fraccion_str(
                suma_conocida
            )
            + ") / "
            + a_fraccion_str(
                Ab[fila][columna]
            )
            + "\n"
            + variable(columna + 1)
            + " = "
            + a_fraccion_str(valor)
        )

        pasos.append(
            texto
        )

    return solucion, pasos


# ============================================================
# GAUSS-JORDAN / RREF
# ============================================================

def gauss_jordan_rref(m, n, Ab_float):
    """
    Aplica Gauss-Jordan para obtener la forma
    escalonada reducida por filas (RREF).

    Cada pivote se convierte en 1 y todos los demás
    elementos de su columna se convierten en 0.

    También se conserva el procedimiento completo.
    """

    Ab = convertir_matriz(
        Ab_float
    )

    pasos = []
    pivotes_pos = []

    fila_pivote = 0

    pasos.append(
        (
            "info",

            "Iniciamos Gauss-Jordan con la "
            "matriz aumentada [A | b].",

            copiar_matriz(Ab)
        )
    )

    for columna in range(n):

        if fila_pivote >= m:
            break

        fila_elegida = -1

        # ----------------------------------------------------
        # Intentamos utilizar primero 1 o -1.
        # ----------------------------------------------------

        for i in range(
            fila_pivote,
            m
        ):

            if (
                Ab[i][columna] == 1
                or
                Ab[i][columna] == -1
            ):

                fila_elegida = i
                break

        # ----------------------------------------------------
        # Si no existe, buscamos cualquier elemento no nulo.
        # ----------------------------------------------------

        if fila_elegida == -1:

            for i in range(
                fila_pivote,
                m
            ):

                if Ab[i][columna] != 0:

                    fila_elegida = i
                    break

        if fila_elegida == -1:

            pasos.append(
                (
                    "info",

                    "La columna de "
                    + variable(columna + 1)
                    + " no contiene un pivote disponible. "
                    + "Esta variable puede ser libre."
                )
            )

            continue

        # ----------------------------------------------------
        # INTERCAMBIO
        # ----------------------------------------------------

        if fila_elegida != fila_pivote:

            Ab[fila_pivote], Ab[fila_elegida] = (
                Ab[fila_elegida],
                Ab[fila_pivote]
            )

            pasos.append(
                (
                    "pivoteo",

                    "Intercambiamos "
                    + nombre_fila(fila_pivote + 1)
                    + " ↔ "
                    + nombre_fila(fila_elegida + 1)
                    + ".",

                    copiar_matriz(Ab)
                )
            )

        pivote_original = (
            Ab[fila_pivote][columna]
        )

        # ----------------------------------------------------
        # NORMALIZAR PIVOTE
        # ----------------------------------------------------

        if pivote_original != 1:

            for j in range(
                columna,
                n + 1
            ):

                Ab[fila_pivote][j] = (
                    Ab[fila_pivote][j]
                    /
                    pivote_original
                )

            pasos.append(
                (
                    "operacion",

                    "El pivote actual es "
                    + a_fraccion_str(
                        pivote_original
                    )
                    + ". Para convertirlo en 1:\n\n"

                    + nombre_fila(fila_pivote + 1)
                    + " = "
                    + nombre_fila(fila_pivote + 1)
                    + " / ("
                    + a_fraccion_str(
                        pivote_original
                    )
                    + ")",

                    copiar_matriz(Ab)
                )
            )

        pivotes_pos.append(
            (fila_pivote, columna)
        )

        # ----------------------------------------------------
        # CREAR CEROS ARRIBA Y ABAJO
        # ----------------------------------------------------

        for i in range(m):

            if i == fila_pivote:
                continue

            factor = Ab[i][columna]

            if factor == 0:
                continue

            for j in range(
                columna,
                n + 1
            ):

                Ab[i][j] = (
                    Ab[i][j]
                    -
                    factor
                    * Ab[fila_pivote][j]
                )

            pasos.append(
                (
                    "operacion",

                    "Eliminamos "
                    + a_fraccion_str(factor)
                    + " de "
                    + nombre_fila(i + 1)
                    + ".\n\n"

                    + nombre_fila(i + 1)
                    + " = "
                    + nombre_fila(i + 1)
                    + " - ("
                    + a_fraccion_str(factor)
                    + ")"
                    + nombre_fila(fila_pivote + 1),

                    copiar_matriz(Ab)
                )
            )

        fila_pivote += 1

    inconsistente, fila_error = (
        es_inconsistente(
            m,
            n,
            Ab
        )
    )

    if inconsistente:

        pasos.append(
            (
                "info",

                "La fila "
                + str(fila_error + 1)
                + " representa una contradicción "
                + "porque todos los coeficientes "
                + "son cero y el término "
                + "independiente no es cero."
            )
        )

    else:

        pasos.append(
            (
                "info",

                "La reducción ha terminado. "
                "La matriz está en forma "
                "escalonada reducida por filas (RREF).",

                copiar_matriz(Ab)
            )
        )

    return (
        Ab,
        pivotes_pos,
        pasos,
        inconsistente
    )


# ============================================================
# COMPLETAR RREF
# ============================================================

def completar_rref(m, n, Ab_escalonada):
    """
    Recibe una matriz escalonada y continúa
    el procedimiento hasta obtener RREF.
    """

    rref, pivotes, pasos, inconsistente = (
        gauss_jordan_rref(
            m,
            n,
            Ab_escalonada
        )
    )

    return rref, pivotes, pasos


# ============================================================
# CLASIFICACIÓN DEL SISTEMA
# ============================================================

def clasificar_sistema(m, n, Ab, pivotes_pos):
    """
    Clasifica un sistema según sus pivotes.

    determinado:
        una única solución.

    indeterminado:
        infinitas soluciones.

    inconsistente:
        no tiene solución.
    """

    inconsistente, fila = (
        es_inconsistente(
            m,
            n,
            Ab
        )
    )

    if inconsistente:

        return {
            "tipo": "inconsistente",

            "descripcion":
                "Sistema inconsistente: "
                "no tiene solución.",

            "fila_inconsistente": fila
        }

    columnas_pivote = []

    for fila, columna in pivotes_pos:

        if columna < n:

            if columna not in columnas_pivote:

                columnas_pivote.append(
                    columna
                )

    if len(columnas_pivote) == n:

        return {
            "tipo": "determinado",

            "descripcion":
                "Sistema consistente determinado: "
                "tiene una única solución."
        }

    return {
        "tipo": "indeterminado",

        "descripcion":
            "Sistema consistente indeterminado: "
            "tiene infinitas soluciones."
    }


# ============================================================
# SOLUCIÓN GENERAL DESDE RREF
# ============================================================

def construir_solucion_general(
    m,
    n,
    Ab,
    pivotes_pos
):
    """
    Construye la solución de un sistema que se
    encuentra en RREF.

    Las variables sin pivote se representan mediante:

    t₁, t₂, t₃, ...
    """

    columnas_pivote = []

    for fila, columna in pivotes_pos:

        if (
            columna < n
            and
            columna not in columnas_pivote
        ):

            columnas_pivote.append(
                columna
            )

    variables_basicas = []
    variables_libres = []

    for j in range(n):

        if j in columnas_pivote:

            variables_basicas.append(
                j
            )

        else:

            variables_libres.append(
                j
            )

    lineas = []

    inconsistente, fila_error = (
        es_inconsistente(
            m,
            n,
            Ab
        )
    )

    # --------------------------------------------------------
    # SISTEMA INCONSISTENTE
    # --------------------------------------------------------

    if inconsistente:

        lineas.append(
            "SISTEMA INCONSISTENTE"
        )

        lineas.append(
            "La fila "
            + str(fila_error + 1)
            + " representa una contradicción."
        )

        lineas.append(
            "Por tanto, el sistema no tiene solución."
        )

        return (
            variables_basicas,
            variables_libres,
            lineas
        )

    # --------------------------------------------------------
    # SOLUCIÓN ÚNICA
    # --------------------------------------------------------

    if len(variables_libres) == 0:

        lineas.append(
            "SOLUCIÓN ÚNICA:"
        )

        for fila, columna in pivotes_pos:

            if columna < n:

                lineas.append(
                    variable(columna + 1)
                    + " = "
                    + a_fraccion_str(
                        Ab[fila][n]
                    )
                )

        return (
            variables_basicas,
            variables_libres,
            lineas
        )

    # --------------------------------------------------------
    # SOLUCIÓN PARAMÉTRICA
    # --------------------------------------------------------

    lineas.append(
        "SOLUCIÓN GENERAL PARAMÉTRICA:"
    )

    parametros = {}

    for i in range(
        len(variables_libres)
    ):

        columna = variables_libres[i]

        parametro = (
            "t"
            + a_subindice(i + 1)
        )

        parametros[columna] = parametro

    # --------------------------------------------------------
    # VARIABLES BÁSICAS
    # --------------------------------------------------------

    for fila, columna in pivotes_pos:

        if columna >= n:
            continue

        expresion = (
            a_fraccion_str(
                Ab[fila][n]
            )
        )

        for libre in variables_libres:

            coeficiente = (
                -Ab[fila][libre]
            )

            if coeficiente == 0:
                continue

            parametro = parametros[
                libre
            ]

            if coeficiente > 0:

                if coeficiente == 1:

                    expresion += (
                        " + "
                        + parametro
                    )

                else:

                    expresion += (
                        " + "
                        + a_fraccion_str(
                            coeficiente
                        )
                        + parametro
                    )

            else:

                positivo = -coeficiente

                if positivo == 1:

                    expresion += (
                        " - "
                        + parametro
                    )

                else:

                    expresion += (
                        " - "
                        + a_fraccion_str(
                            positivo
                        )
                        + parametro
                    )

        lineas.append(
            variable(columna + 1)
            + " = "
            + expresion
        )

    # --------------------------------------------------------
    # VARIABLES LIBRES
    # --------------------------------------------------------

    for columna in variables_libres:

        lineas.append(
            variable(columna + 1)
            + " = "
            + parametros[columna]
            + ", "
            + parametros[columna]
            + " ∈ ℝ"
        )

    return (
        variables_basicas,
        variables_libres,
        lineas
    )