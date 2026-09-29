 

# ============================================================
# MÓDULO 1
# SISTEMAS DE ECUACIONES LINEALES
# ============================================================

def teoremas_sistemas():
    """
    Retorna los conceptos y teoremas principales
    relacionados con sistemas de ecuaciones lineales.
    """

    return """
============================================================
TEOREMAS CLAVE — SISTEMAS DE ECUACIONES LINEALES
============================================================

1. SISTEMA CONSISTENTE

Un sistema de ecuaciones lineales es consistente cuando
posee al menos una solución.

Puede tener:

• Una única solución.
• Infinitas soluciones.


2. SISTEMA INCONSISTENTE

Un sistema es inconsistente cuando no posee solución.

Durante la reducción por filas puede identificarse mediante
una fila de la forma:

[ 0   0   ...   0 | b ]

donde:

b ≠ 0

Esto representa una contradicción:

0 = b


3. SISTEMA DETERMINADO

Si todas las variables poseen pivote y no existe ninguna
contradicción, el sistema tiene una única solución.


4. SISTEMA INDETERMINADO

Si el sistema es consistente pero existen variables libres,
entonces posee infinitas soluciones.


5. OPERACIONES ELEMENTALES POR FILAS

Las operaciones elementales permitidas son:

• Intercambiar dos filas.

• Multiplicar una fila por un escalar diferente de cero.

• Sumar a una fila un múltiplo de otra fila.

Estas operaciones permiten transformar la matriz sin cambiar
el conjunto de soluciones del sistema.


6. FORMA ESCALONADA

Una matriz está en forma escalonada cuando:

• Las filas completamente nulas aparecen al final.

• Cada pivote se encuentra más a la derecha que el pivote
  de la fila anterior.

• Debajo de cada pivote existen ceros.


7. FORMA ESCALONADA REDUCIDA

Además de cumplir las condiciones de la forma escalonada:

• Cada pivote es igual a 1.

• Cada pivote es el único elemento distinto de cero
  de su columna.
"""


# ============================================================
# MÓDULO 2
# VECTORES E INDEPENDENCIA LINEAL
# ============================================================

def teoremas_vectores():
    """
    Retorna los conceptos y teoremas principales
    relacionados con vectores, combinación lineal
    e independencia lineal.
    """

    return """
============================================================
TEOREMAS CLAVE — VECTORES E INDEPENDENCIA LINEAL
============================================================

1. COMBINACIÓN LINEAL

Dados los vectores:

v₁, v₂, ..., vₖ

una combinación lineal tiene la forma:

c₁v₁ + c₂v₂ + ... + cₖvₖ

donde:

c₁, c₂, ..., cₖ

son escalares.


2. COMBINACIÓN LINEAL DE UN VECTOR b

Para determinar si un vector b es combinación lineal de:

v₁, v₂, ..., vₖ

se plantea:

c₁v₁ + c₂v₂ + ... + cₖvₖ = b

Esto puede escribirse como:

Ax = b

donde los vectores se colocan como columnas de A.


3. ECUACIÓN DE INDEPENDENCIA LINEAL

Para estudiar la independencia lineal de:

{v₁, v₂, ..., vₖ}

se plantea la ecuación homogénea:

c₁v₁ + c₂v₂ + ... + cₖvₖ = 0

En forma matricial:

Ax = 0


4. SOLUCIÓN TRIVIAL

Todo sistema homogéneo Ax = 0 posee al menos la solución:

c₁ = 0
c₂ = 0
...
cₖ = 0

Esta se conoce como solución trivial.


5. LINEALMENTE INDEPENDIENTE — L.I.

Los vectores:

{v₁, v₂, ..., vₖ}

son linealmente independientes si la ecuación:

c₁v₁ + c₂v₂ + ... + cₖvₖ = 0

posee únicamente la solución trivial:

c₁ = c₂ = ... = cₖ = 0


6. CRITERIO MEDIANTE PIVOTES

Si la matriz:

A = [v₁  v₂  ...  vₖ]

posee un pivote en cada columna, entonces no existen
variables libres.

Por lo tanto:

Ax = 0

solo tiene la solución trivial y los vectores son:

LINEALMENTE INDEPENDIENTES (L.I.)


7. LINEALMENTE DEPENDIENTE — L.D.

Los vectores son linealmente dependientes cuando existen
escalares, no todos iguales a cero, tales que:

c₁v₁ + c₂v₂ + ... + cₖvₖ = 0


8. CRITERIO MEDIANTE VARIABLES LIBRES

Si después de reducir A existe al menos una variable libre,
entonces Ax = 0 posee soluciones no triviales.

Por lo tanto, los vectores son:

LINEALMENTE DEPENDIENTES (L.D.)


9. RESUMEN DEL CRITERIO

Sin variables libres
        ↓
Solo solución trivial
        ↓
L.I.


Con una o más variables libres
        ↓
Existen soluciones no triviales
        ↓
L.D.
"""


# ============================================================
# MÓDULO 3
# MATRICES Y SUS OPERACIONES
# ============================================================

def teoremas_matrices():
    """
    Retorna conceptos importantes relacionados
    con matrices y sus operaciones.
    """

    return """
============================================================
TEOREMAS CLAVE — MATRICES Y SUS OPERACIONES
============================================================

1. IGUALDAD DE MATRICES

Dos matrices A y B son iguales cuando:

• Tienen las mismas dimensiones.
• Todos sus elementos correspondientes son iguales.


2. SUMA DE MATRICES

Para calcular:

A + B

las matrices deben tener las mismas dimensiones.

La suma se realiza elemento por elemento.


3. RESTA DE MATRICES

Para calcular:

A - B

las matrices deben tener las mismas dimensiones.

La resta se realiza elemento por elemento.


4. MULTIPLICACIÓN POR ESCALAR

Para calcular:

cA

cada elemento de A se multiplica por el escalar c.


5. MULTIPLICACIÓN DE MATRICES

El producto:

AB

está definido únicamente cuando:

número de columnas de A
=
número de filas de B

Si:

A es m × n

y:

B es n × p

entonces:

AB es m × p


6. PRODUCTO FILA POR COLUMNA

Cada elemento del producto AB se obtiene mediante el
producto de una fila de A por una columna de B.


7. PRODUCTO MATRIZ-VECTOR

Si A tiene n columnas y x posee n componentes,
entonces el producto:

Ax

está definido.


8. MATRIZ TRANSPUESTA

La transpuesta de A se representa:

Aᵀ

y se obtiene convirtiendo las filas de A en columnas.


9. MATRIZ IDENTIDAD

La matriz identidad I posee:

• 1 en su diagonal principal.
• 0 en las demás posiciones.

Para una matriz compatible:

AI = IA = A
"""


# ============================================================
# MÓDULO 4
# DETERMINANTES
# ============================================================

def teoremas_determinantes():
    """
    Información correspondiente al módulo de
    determinantes.

    Se mantiene breve porque este módulo todavía
    no ha sido desarrollado dentro del proyecto.
    """

    return """
============================================================
TEOREMAS CLAVE — DETERMINANTES
============================================================

Este módulo queda preparado para las siguientes etapas
del proyecto.

Concepto básico:

El determinante es un valor asociado a una matriz cuadrada.

Por lo tanto, para hablar de determinante primero debe
cumplirse:

número de filas = número de columnas

Las reglas, propiedades y métodos específicos para calcular
determinantes se incorporarán cuando se desarrolle
formalmente este módulo.
"""


# ============================================================
# FUNCIÓN GENERAL
# ============================================================

def obtener_teoremas(modulo):
    """
    Permite obtener los teoremas utilizando el número
    o nombre del módulo.

    Ejemplos:

    obtener_teoremas(1)
    obtener_teoremas("sistemas")

    obtener_teoremas(2)
    obtener_teoremas("vectores")
    """

    if isinstance(modulo, str):
        modulo = modulo.strip().lower()

    if modulo == 1 or modulo == "sistemas":
        return teoremas_sistemas()

    if modulo == 2 or modulo == "vectores":
        return teoremas_vectores()

    if modulo == 3 or modulo == "matrices":
        return teoremas_matrices()

    if modulo == 4 or modulo == "determinantes":
        return teoremas_determinantes()

    raise ValueError(
        "El módulo solicitado no existe."
    )