from fractions import Fraction

def a_subindice(numero):
    """Convierte un entero a su equivalente en subíndice Unicode (ej: 1 -> ₁)"""
    subindices = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(numero).translate(subindices)

def parsear_entrada(texto):
    """Convierte texto de celda (entero, decimal, coma o fracción a/b) a Fraction exacta."""
    if texto is None:
        raise ValueError("Celda vacía")
    normalizado = str(texto).strip().replace(",", ".")
    if normalizado == "":
        raise ValueError("Celda vacía")
    try:
        return Fraction(normalizado).limit_denominator(10**6)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"Valor no numérico: {texto}") from exc

def a_fraccion(valor):
    """Normaliza un valor (Fraction, int, float o str) a Fraction."""
    if isinstance(valor, Fraction):
        return valor
    if isinstance(valor, str):
        return parsear_entrada(valor)
    if isinstance(valor, int):
        return Fraction(valor)
    return Fraction(valor).limit_denominator(1000)

def a_fraccion_str(valor):
    """Convierte un número o Fraction a un string formateado como fracción."""
    f = a_fraccion(valor)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


class AlgebraModel:

    # --- MÓDULO 1: ELIMINACIÓN GAUSSIANA ORIGINAL ---
    @staticmethod
    def _copiar_matriz(Ab):
        return [fila[:] for fila in Ab]

    @staticmethod
    def detectar_pivotes(m, n, Ab):
        """Devuelve pares (fila, columna) del primer no-cero de cada fila no nula."""
        pivotes_pos = []
        for i in range(m):
            for j in range(n):
                if Ab[i][j] != 0:
                    pivotes_pos.append((i, j))
                    break
        return pivotes_pos

    @staticmethod
    def es_inconsistente(m, n, Ab):
        for i in range(m):
            if all(Ab[i][j] == 0 for j in range(n)) and Ab[i][n] != 0:
                return True, i
        return False, None

    @staticmethod
    def eliminacion_gaussiana(m, n, Ab_float):
        """Ejecuta la eliminación gaussiana hacia abajo con pivoteo parcial."""
        Ab = [[a_fraccion(val) for val in fila] for fila in Ab_float]
        pasos = []
        pivotes_pos = []
        fila_pivote = 0

        for j in range(n):
            if fila_pivote >= m:
                break

            max_fila = fila_pivote
            for i in range(fila_pivote + 1, m):
                if abs(Ab[i][j]) > abs(Ab[max_fila][j]):
                    max_fila = i

            if Ab[max_fila][j] == 0:
                pasos.append(("info", f"Columna x{a_subindice(j+1)} sin pivote válido. Saltando."))
                continue

            if max_fila != fila_pivote:
                Ab[fila_pivote], Ab[max_fila] = Ab[max_fila], Ab[fila_pivote]
                pasos.append(("pivoteo", f"Pivoteo Parcial (Fila {fila_pivote+1} ↔ Fila {max_fila+1})", AlgebraModel._copiar_matriz(Ab)))

            hubo_cambio = False
            for i in range(fila_pivote + 1, m):
                factor = Ab[i][j] / Ab[fila_pivote][j]
                if factor != 0:
                    for k in range(j, n + 1):
                        Ab[i][k] -= factor * Ab[fila_pivote][k]
                    hubo_cambio = True
                    pasos.append(("operacion", f"F{a_subindice(i+1)} = F{a_subindice(i+1)} - ({a_fraccion_str(factor)}) * F{a_subindice(fila_pivote+1)}", AlgebraModel._copiar_matriz(Ab)))

            pivotes_pos.append((fila_pivote, j))
            fila_pivote += 1

        return Ab, pasos, pivotes_pos

    @staticmethod
    def completar_rref(m, n, Ab_escalonada):
        """Parte de una matriz escalonada: pivotes a 1 y ceros por encima."""
        Ab = AlgebraModel._copiar_matriz(Ab_escalonada)
        pasos = []
        pivotes_pos = AlgebraModel.detectar_pivotes(m, n, Ab)

        for f_piv, c_piv in pivotes_pos:
            pivote_val = Ab[f_piv][c_piv]
            if pivote_val != 1:
                for k in range(c_piv, n + 1):
                    Ab[f_piv][k] /= pivote_val
                pasos.append(("operacion", f"F{a_subindice(f_piv+1)} = F{a_subindice(f_piv+1)} / ({a_fraccion_str(pivote_val)})", AlgebraModel._copiar_matriz(Ab)))

        for f_piv, c_piv in reversed(pivotes_pos):
            for i in range(f_piv - 1, -1, -1):
                factor = Ab[i][c_piv]
                if factor != 0:
                    for k in range(c_piv, n + 1):
                        Ab[i][k] -= factor * Ab[f_piv][k]
                    pasos.append(("operacion", f"F{a_subindice(i+1)} = F{a_subindice(i+1)} - ({a_fraccion_str(factor)}) * F{a_subindice(f_piv+1)}", AlgebraModel._copiar_matriz(Ab)))

        return Ab, pivotes_pos, pasos

    @staticmethod
    def sustitucion_hacia_atras(m, n, Ab):
        """Calcula las soluciones por sustitución hacia atrás."""
        x = [Fraction(0) for _ in range(n)]
        for i in range(n - 1, -1, -1):
            suma = sum(Ab[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (Ab[i][n] - suma) / Ab[i][i]
        return x

    # --- MÓDULO 2: GAUSS-JORDAN CON ESTRATEGIA PARA EVITAR FRACCIONES ---
    @staticmethod
    def gauss_jordan_rref(m, n, Ab_float):
        """
        Ejecuta la reducción de Gauss-Jordan priorizando pivotes enteros (1 o -1)
        para evitar trabajar con fracciones en pasos intermedios.
        """
        Ab = [[a_fraccion(val) for val in fila] for fila in Ab_float]
        pasos = []
        pivotes_pos = []
        fila_pivote = 0

        # FASE 1: Hacia Abajo
        for j in range(n):
            if fila_pivote >= m:
                break

            # 1. Buscar si hay una fila disponible con un 1 o -1 en la columna j
            fila_elegida = -1
            for i in range(fila_pivote, m):
                if abs(Ab[i][j]) == 1:
                    fila_elegida = i
                    break

            # 2. Si no hay 1 o -1, tomar la fila con el máximo valor absoluto
            if fila_elegida == -1:
                max_fila = fila_pivote
                for i in range(fila_pivote + 1, m):
                    if abs(Ab[i][j]) > abs(Ab[max_fila][j]):
                        max_fila = i
                fila_elegida = max_fila

            if Ab[fila_elegida][j] == 0:
                continue

            # Intercambio de filas si aplica
            if fila_elegida != fila_pivote:
                Ab[fila_pivote], Ab[fila_elegida] = Ab[fila_elegida], Ab[fila_pivote]
                pasos.append(("pivoteo", f"Selección de Pivote Óptimo: Fila {fila_pivote+1} ↔ Fila {fila_elegida+1} (para evitar fracciones)", [f[:] for f in Ab]))

            # Si el pivote es -1, multiplicamos la fila por -1
            if Ab[fila_pivote][j] == -1:
                for k in range(j, n + 1):
                    Ab[fila_pivote][k] *= -1
                pasos.append(("operacion", f"F{a_subindice(fila_pivote+1)} = -1 * F{a_subindice(fila_pivote+1)}", [f[:] for f in Ab]))

            # Normalizar el pivote a 1 si es diferente de 1
            pivote_val = Ab[fila_pivote][j]
            if pivote_val != 1:
                for k in range(j, n + 1):
                    Ab[fila_pivote][k] /= pivote_val
                pasos.append(("operacion", f"F{a_subindice(fila_pivote+1)} = F{a_subindice(fila_pivote+1)} / ({a_fraccion_str(pivote_val)})", [f[:] for f in Ab]))

            pivotes_pos.append((fila_pivote, j))

            # Eliminar elementos debajo del pivote
            for i in range(fila_pivote + 1, m):
                factor = Ab[i][j]
                if factor != 0:
                    for k in range(j, n + 1):
                        Ab[i][k] -= factor * Ab[fila_pivote][k]
                    pasos.append(("operacion", f"F{a_subindice(i+1)} = F{a_subindice(i+1)} - ({a_fraccion_str(factor)}) * F{a_subindice(fila_pivote+1)}", [f[:] for f in Ab]))

            fila_pivote += 1

        # Verificar inconsistencia [0 0 ... 0 | b] con b != 0
        for i in range(m):
            if all(Ab[i][j] == 0 for j in range(n)) and Ab[i][n] != 0:
                return Ab, pivotes_pos, pasos, True

        # FASE 2: Hacia Arriba (Ceros por encima)
        for f_piv, c_piv in reversed(pivotes_pos):
            for i in range(f_piv - 1, -1, -1):
                factor = Ab[i][c_piv]
                if factor != 0:
                    for k in range(c_piv, n + 1):
                        Ab[i][k] -= factor * Ab[f_piv][k]
                    pasos.append(("operacion", f"F{a_subindice(i+1)} = F{a_subindice(i+1)} - ({a_fraccion_str(factor)}) * F{a_subindice(f_piv+1)}", [f[:] for f in Ab]))

        return Ab, pivotes_pos, pasos, False

    @staticmethod
    def construir_solucion_general(m, n, Ab, pivotes_pos):
        """Calcula la clasificación de variables y genera la solución paramétrica o única."""
        cols_pivote = set(p[1] for p in pivotes_pos)
        vars_basicas = [j for j in range(n) if j in cols_pivote]
        vars_libres = [j for j in range(n) if j not in cols_pivote]

        lineas_solucion = []

        if len(vars_libres) == 0:
            lineas_solucion.append("Solución Única (Sistema Consistente Determinado):")
            for f, c in pivotes_pos:
                lineas_solucion.append(f"  x{a_subindice(c+1)} = {a_fraccion_str(Ab[f][n])}")
        else:
            lineas_solucion.append(f"Solución General Paramétrica ({len(vars_libres)} variable(s) libre(s)):")
            
            for f, c in pivotes_pos:
                terminos = [a_fraccion_str(Ab[f][n])] if Ab[f][n] != 0 else []
                for jl in vars_libres:
                    coef = Ab[f][jl]
                    if coef != 0:
                        coef_inv = -coef
                        signo = "+" if coef_inv > 0 and terminos else ("-" if coef_inv < 0 and terminos else "")
                        val_str = a_fraccion_str(abs(coef_inv))
                        str_final = f"x{a_subindice(jl+1)}" if val_str == "1" else f"{val_str}·x{a_subindice(jl+1)}"
                        
                        if terminos:
                            terminos.append(f"{signo} {str_final}".strip())
                        else:
                            terminos.append(f"{'-' if coef_inv < 0 else ''}{str_final}")

                expresion = " + ".join(terminos) if terminos else "0"
                expresion = expresion.replace("+ -", "- ")
                lineas_solucion.append(f"  x{a_subindice(c+1)} = {expresion}")

            for jl in vars_libres:
                lineas_solucion.append(f"  x{a_subindice(jl+1)}  (libre, ∈ ℝ)")

        return vars_basicas, vars_libres, lineas_solucion

    # --- MÓDULO 3: ECUACIÓN MATRICIAL ---
    @staticmethod
    def producto_ax(m, n, A_float, x_float):
        """Calcula el producto Ax utilizando objetos Fraction."""
        A = [[a_fraccion(val) for val in fila] for fila in A_float]
        x = [a_fraccion(val) for val in x_float]
        
        b = []
        detalles = []
        for i in range(m):
            suma = Fraction(0)
            detalle = []
            for j in range(n):
                suma += A[i][j] * x[j]
                detalle.append(f"({a_fraccion_str(A[i][j])} * {a_fraccion_str(x[j])})")
            b.append(suma)
            detalles.append(f"Fila {i+1} * Vector x: {' + '.join(detalle)} = {a_fraccion_str(suma)}")
        return b, detalles