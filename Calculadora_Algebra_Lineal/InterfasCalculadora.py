import tkinter as tk
from tkinter import ttk, messagebox

from modulos.utilidades import (
    a_subindice,
    a_fraccion_str,
    parsear_entrada
)

from modulos import modulo_sistemas
from modulos import modulo_vectores
from modulos import modulo_matrices
from modulos import modulo_determinantes

from teoremas.resumen_teoremas import obtener_teoremas


class InterfasCalculadora:

    # ============================================================
    # INICIO
    # ============================================================

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Suite de Álgebra Lineal - Programa 4"
        )

        self.root.geometry("1200x900")
        self.root.minsize(1050, 750)

        # ========================================================
        # COLORES
        # ========================================================

        self.colors = {
            "bg_main": "#1e1e2e",
            "bg_panel": "#252535",
            "bg_entry": "#313244",
            "fg_text": "#cdd6f4",
            "accent": "#89b4fa",
            "accent_hover": "#74c7ec",
            "vector_b": "#312635",
            "b_text": "#f38ba8",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "error": "#f38ba8",
            "comment": "#a6adc8"
        }

        self.root.configure(
            bg=self.colors["bg_main"]
        )

        # ========================================================
        # ESTILOS
        # ========================================================

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background=self.colors["bg_main"],
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=self.colors["bg_panel"],
            foreground=self.colors["fg_text"],
            font=("Segoe UI", 10, "bold"),
            padding=[10, 8],
            borderwidth=0
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", self.colors["accent"])
            ],
            foreground=[
                ("selected", "#11111b")
            ]
        )

        style.configure(
            "TFrame",
            background=self.colors["bg_main"]
        )

        style.configure(
            "TLabel",
            background=self.colors["bg_main"],
            foreground=self.colors["fg_text"],
            font=("Segoe UI", 10)
        )

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 17, "bold"),
            foreground=self.colors["accent"]
        )

        # ========================================================
        # TÍTULO
        # ========================================================

        ttk.Label(
            root,
            text="Suite de Álgebra Lineal - Programa 4",
            style="Header.TLabel"
        ).pack(
            pady=(15, 5)
        )

        # ========================================================
        # PESTAÑAS
        # ========================================================

        self.notebook = ttk.Notebook(root)

        self.notebook.pack(
            fill=tk.BOTH,
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.tab_gauss = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_gauss,
            text=" 1. Gauss (Ax=b) "
        )

        self.construir_modulo_gauss(
            self.tab_gauss
        )

        self.tab_rref = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_rref,
            text=" 2. RREF (Gauss-Jordan) "
        )

        self.construir_modulo_rref(
            self.tab_rref
        )

        self.tab_ax = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_ax,
            text=" 3. Ecuación Matricial (Ax) "
        )

        self.construir_modulo_ax(
            self.tab_ax
        )

        self.tab_vectores = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_vectores,
            text=" 4. Vectores e Independencia "
        )

        self.construir_modulo_vectores(
            self.tab_vectores
        )

        self.tab_matrices = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_matrices,
            text=" 5. Operaciones Matriciales "
        )

        self.construir_modulo_matrices(
            self.tab_matrices
        )

        self.tab_propiedades = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_propiedades,
            text=" 6. Propiedades Ax "
        )

        self.construir_modulo_propiedades(
            self.tab_propiedades
        )

    # ============================================================
    # FUNCIONES VISUALES
    # ============================================================

    def crear_entry_suave(
        self,
        parent,
        is_vector=False
    ):

        if is_vector:
            fondo = self.colors["vector_b"]
            texto = self.colors["b_text"]
        else:
            fondo = self.colors["bg_entry"]
            texto = self.colors["fg_text"]

        return tk.Entry(
            parent,
            width=8,
            justify="center",
            font=("Consolas", 11),
            bg=fondo,
            fg=texto,
            relief="flat",
            insertbackground=self.colors["fg_text"],
            highlightthickness=1,
            highlightbackground=self.colors["bg_panel"],
            highlightcolor=self.colors["accent"]
        )

    def crear_boton_suave(
        self,
        parent,
        texto,
        comando
    ):

        boton = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=self.colors["accent"],
            fg="#11111b",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            activebackground=self.colors[
                "accent_hover"
            ],
            activeforeground="#11111b",
            padx=15,
            pady=6,
            cursor="hand2"
        )

        boton.bind(
            "<Enter>",
            lambda e: boton.config(
                bg=self.colors["accent_hover"]
            )
        )

        boton.bind(
            "<Leave>",
            lambda e: boton.config(
                bg=self.colors["accent"]
            )
        )

        return boton

    def configurar_consola(
        self,
        frame_padre
    ):

        frame = tk.Frame(
            frame_padre,
            bg=self.colors["bg_panel"],
            highlightthickness=1,
            highlightbackground=self.colors["comment"]
        )

        frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        scroll_y = ttk.Scrollbar(frame)

        scroll_y.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        scroll_x = ttk.Scrollbar(
            frame,
            orient=tk.HORIZONTAL
        )

        scroll_x.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        consola = tk.Text(
            frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            font=("Consolas", 10),
            bg=self.colors["bg_panel"],
            fg=self.colors["fg_text"],
            padx=15,
            pady=15,
            relief="flat",
            wrap=tk.NONE
        )

        consola.pack(
            fill=tk.BOTH,
            expand=True
        )

        scroll_y.config(
            command=consola.yview
        )

        scroll_x.config(
            command=consola.xview
        )

        consola.tag_config(
            "titulo",
            font=("Consolas", 11, "bold"),
            foreground=self.colors["accent"]
        )

        consola.tag_config(
            "paso",
            font=("Consolas", 10, "bold"),
            foreground=self.colors["warning"]
        )

        consola.tag_config(
            "explicacion",
            foreground=self.colors["comment"]
        )

        consola.tag_config(
            "alerta",
            foreground=self.colors["error"],
            font=("Consolas", 10, "bold")
        )

        consola.tag_config(
            "exito",
            foreground=self.colors["success"],
            font=("Consolas", 10, "bold")
        )

        consola.tag_config(
            "matriz",
            foreground=self.colors["fg_text"],
            font=("Consolas", 11)
        )

        consola.tag_config(
            "variable",
            foreground=self.colors["warning"],
            font=("Consolas", 10, "bold")
        )

        return consola

    def log(
        self,
        consola,
        mensaje="",
        tipo="normal"
    ):

        consola.insert(
            tk.END,
            str(mensaje) + "\n",
            tipo
        )

        consola.see(tk.END)

    def titulo_resultado(
        self,
        consola,
        titulo
    ):

        self.log(
            consola,
            "=" * 72,
            "titulo"
        )

        self.log(
            consola,
            titulo,
            "titulo"
        )

        self.log(
            consola,
            "=" * 72,
            "titulo"
        )

        self.log(consola)

    def mostrar_vector(
        self,
        consola,
        vector,
        nombre=None,
        tipo="matriz"
    ):

        if nombre is not None:

            self.log(
                consola,
                nombre,
                "variable"
            )

        for valor in vector:

            self.log(
                consola,
                "[ " + a_fraccion_str(valor) + " ]",
                tipo
            )

    def formatear_matriz(
        self,
        matriz,
        consola,
        pivotes=None,
        aumentada=False
    ):

        if pivotes is None:
            pivotes = []

        for i in range(len(matriz)):

            texto = "   [ "

            for j in range(len(matriz[i])):

                valor = a_fraccion_str(
                    matriz[i][j]
                )

                if (
                    aumentada
                    and
                    j == len(matriz[i]) - 1
                ):

                    texto += (
                        " │ "
                        + "{:^10}".format(valor)
                    )

                else:

                    if (i, j) in pivotes:

                        texto += (
                            "[{:^8}] ".format(valor)
                        )

                    else:

                        texto += (
                            "{:^10} ".format(valor)
                        )

            texto += "]"

            self.log(
                consola,
                texto,
                "matriz"
            )

    def leer_matriz(
        self,
        entradas
    ):

        matriz = []

        for fila_entradas in entradas:

            fila = []

            for entrada in fila_entradas:

                fila.append(
                    parsear_entrada(
                        entrada.get()
                    )
                )

            matriz.append(fila)

        return matriz

    def leer_vector(
        self,
        entradas
    ):

        vector = []

        for entrada in entradas:

            vector.append(
                parsear_entrada(
                    entrada.get()
                )
            )

        return vector

    def registrar_pasos(
        self,
        consola,
        pasos,
        pivotes=None,
        aumentada=True
    ):

        if pivotes is None:
            pivotes = []

        numero = 1

        for item in pasos:

            tipo = item[0]
            mensaje = item[1]

            matriz = None

            if len(item) > 2:
                matriz = item[2]

            if tipo == "info":

                self.log(
                    consola,
                    "\nEXPLICACIÓN:",
                    "paso"
                )

                self.log(
                    consola,
                    mensaje,
                    "explicacion"
                )

                if matriz is not None:

                    self.formatear_matriz(
                        matriz,
                        consola,
                        pivotes,
                        aumentada
                    )

            else:

                self.log(
                    consola,
                    "\nPASO " + str(numero),
                    "paso"
                )

                numero += 1

                self.log(
                    consola,
                    mensaje,
                    "variable"
                )

                if matriz is not None:

                    self.log(
                        consola,
                        "\nMatriz resultante:"
                    )

                    self.formatear_matriz(
                        matriz,
                        consola,
                        pivotes,
                        aumentada
                    )

    # ============================================================
    # 1. GAUSS
    # ============================================================

    def construir_modulo_gauss(
        self,
        parent
    ):

        ttk.Label(
            parent,
            text=(
                "Eliminación Gaussiana "
                "con desarrollo paso a paso"
            ),
            foreground=self.colors["comment"]
        ).pack(pady=5)

        frame = ttk.Frame(parent)
        frame.pack()

        ttk.Label(
            frame,
            text="Ecuaciones (m):"
        ).grid(
            row=0,
            column=0
        )

        self.g_m = self.crear_entry_suave(
            frame
        )

        self.g_m.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            frame,
            text="Variables (n):"
        ).grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        self.g_n = self.crear_entry_suave(
            frame
        )

        self.g_n.grid(
            row=0,
            column=3,
            padx=5
        )

        self.crear_boton_suave(
            frame,
            "Generar",
            self.gauss_generar
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.g_frame = tk.Frame(
            parent,
            bg=self.colors["bg_main"]
        )

        self.g_frame.pack(
            pady=10
        )

        self.g_entradas = []

        self.g_resolver = (
            self.crear_boton_suave(
                parent,
                "Resolver por Gauss",
                self.gauss_resolver
            )
        )

        self.g_consola = (
            self.configurar_consola(
                parent
            )
        )

    def gauss_generar(self):

        try:

            self.gm = int(
                self.g_m.get()
            )

            self.gn = int(
                self.g_n.get()
            )

            if self.gm <= 0 or self.gn <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "m y n deben ser enteros positivos."
            )

            return

        for widget in self.g_frame.winfo_children():
            widget.destroy()

        self.g_entradas = []

        for j in range(self.gn):

            ttk.Label(
                self.g_frame,
                text="x" + a_subindice(j + 1)
            ).grid(
                row=0,
                column=j
            )

        ttk.Label(
            self.g_frame,
            text="b"
        ).grid(
            row=0,
            column=self.gn + 1
        )

        for i in range(self.gm):

            fila = []

            for j in range(self.gn):

                entrada = self.crear_entry_suave(
                    self.g_frame
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                fila.append(entrada)

            tk.Label(
                self.g_frame,
                text="│",
                bg=self.colors["bg_main"],
                fg=self.colors["comment"]
            ).grid(
                row=i + 1,
                column=self.gn
            )

            entrada = self.crear_entry_suave(
                self.g_frame,
                True
            )

            entrada.grid(
                row=i + 1,
                column=self.gn + 1,
                padx=2,
                pady=2
            )

            fila.append(entrada)

            self.g_entradas.append(fila)

        self.g_resolver.pack(pady=5)

    def gauss_resolver(self):

        self.g_consola.delete(
            "1.0",
            tk.END
        )

        try:
            Ab = self.leer_matriz(
                self.g_entradas
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.g_consola,
            "ELIMINACIÓN GAUSSIANA"
        )

        self.log(
            self.g_consola,
            "Matriz aumentada inicial [A | b]:",
            "paso"
        )

        self.formatear_matriz(
            Ab,
            self.g_consola,
            aumentada=True
        )

        escalonada, pasos, pivotes = (
            modulo_sistemas.eliminacion_gaussiana(
                self.gm,
                self.gn,
                Ab
            )
        )

        self.registrar_pasos(
            self.g_consola,
            pasos,
            pivotes,
            True
        )

        self.log(
            self.g_consola,
            "\nMATRIZ ESCALONADA FINAL:",
            "exito"
        )

        self.formatear_matriz(
            escalonada,
            self.g_consola,
            pivotes,
            True
        )

        clasificacion = (
            modulo_sistemas.clasificar_sistema(
                self.gm,
                self.gn,
                escalonada,
                pivotes
            )
        )

        self.log(
            self.g_consola,
            "\nCLASIFICACIÓN:",
            "paso"
        )

        self.log(
            self.g_consola,
            clasificacion["descripcion"],
            (
                "alerta"
                if clasificacion["tipo"]
                == "inconsistente"
                else "exito"
            )
        )

        if clasificacion["tipo"] == "inconsistente":

            self.log(
                self.g_consola,
                "\nCONCLUSIÓN:",
                "paso"
            )

            self.log(
                self.g_consola,
                (
                    "Existe una ecuación imposible "
                    "del tipo 0 = c, con c distinto "
                    "de cero. Por tanto, el sistema "
                    "no tiene solución."
                ),
                "alerta"
            )

            return

        if clasificacion["tipo"] == "determinado":

            solucion, pasos_sustitucion = (
                modulo_sistemas.sustitucion_hacia_atras(
                    self.gm,
                    self.gn,
                    escalonada
                )
            )

            self.log(
                self.g_consola,
                "\nSUSTITUCIÓN HACIA ATRÁS",
                "paso"
            )

            for i in range(
                len(pasos_sustitucion)
            ):

                self.log(
                    self.g_consola,
                    "\nDespeje "
                    + str(i + 1)
                    + ":",
                    "variable"
                )

                self.log(
                    self.g_consola,
                    pasos_sustitucion[i],
                    "explicacion"
                )

            self.log(
                self.g_consola,
                "\nSOLUCIÓN FINAL:",
                "exito"
            )

            for i in range(len(solucion)):

                self.log(
                    self.g_consola,
                    "x"
                    + a_subindice(i + 1)
                    + " = "
                    + a_fraccion_str(solucion[i]),
                    "exito"
                )

        else:

            self.log(
                self.g_consola,
                (
                    "\nExisten variables libres. "
                    "Reduciremos la matriz a RREF "
                    "para escribir la solución "
                    "paramétrica."
                ),
                "explicacion"
            )

            rref, pivotes_rref, pasos_rref, error = (
                modulo_sistemas.gauss_jordan_rref(
                    self.gm,
                    self.gn,
                    escalonada
                )
            )

            self.registrar_pasos(
                self.g_consola,
                pasos_rref,
                pivotes_rref,
                True
            )

            basicas, libres, solucion = (
                modulo_sistemas.construir_solucion_general(
                    self.gm,
                    self.gn,
                    rref,
                    pivotes_rref
                )
            )

            self.log(
                self.g_consola,
                "\nVARIABLES BÁSICAS:",
                "paso"
            )

            for indice in basicas:

                self.log(
                    self.g_consola,
                    "x" + a_subindice(indice + 1)
                )

            self.log(
                self.g_consola,
                "\nVARIABLES LIBRES:",
                "paso"
            )

            for indice in libres:

                self.log(
                    self.g_consola,
                    "x" + a_subindice(indice + 1)
                )

            self.log(
                self.g_consola,
                "\nSOLUCIÓN GENERAL:",
                "exito"
            )

            for linea in solucion:

                self.log(
                    self.g_consola,
                    linea,
                    "exito"
                )

    # ============================================================
    # 2. GAUSS-JORDAN / RREF
    # ============================================================

    def construir_modulo_rref(
        self,
        parent
    ):

        ttk.Label(
            parent,
            text=(
                "Gauss-Jordan / RREF "
                "con solución detallada"
            ),
            foreground=self.colors["comment"]
        ).pack(pady=5)

        frame = ttk.Frame(parent)
        frame.pack()

        ttk.Label(
            frame,
            text="Ecuaciones (m):"
        ).grid(row=0, column=0)

        self.r_m = self.crear_entry_suave(
            frame
        )

        self.r_m.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            frame,
            text="Variables (n):"
        ).grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        self.r_n = self.crear_entry_suave(
            frame
        )

        self.r_n.grid(
            row=0,
            column=3,
            padx=5
        )

        self.crear_boton_suave(
            frame,
            "Generar",
            self.rref_generar
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.r_frame = tk.Frame(
            parent,
            bg=self.colors["bg_main"]
        )

        self.r_frame.pack(pady=10)

        self.r_entradas = []

        self.r_resolver = (
            self.crear_boton_suave(
                parent,
                "Resolver por Gauss-Jordan",
                self.rref_resolver
            )
        )

        self.r_consola = (
            self.configurar_consola(
                parent
            )
        )

    def rref_generar(self):

        try:

            self.rm = int(self.r_m.get())
            self.rn = int(self.r_n.get())

            if self.rm <= 0 or self.rn <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "m y n deben ser enteros positivos."
            )

            return

        for widget in self.r_frame.winfo_children():
            widget.destroy()

        self.r_entradas = []

        for j in range(self.rn):

            ttk.Label(
                self.r_frame,
                text="x" + a_subindice(j + 1)
            ).grid(
                row=0,
                column=j
            )

        ttk.Label(
            self.r_frame,
            text="b"
        ).grid(
            row=0,
            column=self.rn + 1
        )

        for i in range(self.rm):

            fila = []

            for j in range(self.rn):

                entrada = self.crear_entry_suave(
                    self.r_frame
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                fila.append(entrada)

            tk.Label(
                self.r_frame,
                text="│",
                bg=self.colors["bg_main"],
                fg=self.colors["comment"]
            ).grid(
                row=i + 1,
                column=self.rn
            )

            entrada = self.crear_entry_suave(
                self.r_frame,
                True
            )

            entrada.grid(
                row=i + 1,
                column=self.rn + 1,
                padx=2,
                pady=2
            )

            fila.append(entrada)

            self.r_entradas.append(fila)

        self.r_resolver.pack(pady=5)

    def rref_resolver(self):

        self.r_consola.delete(
            "1.0",
            tk.END
        )

        try:
            Ab = self.leer_matriz(
                self.r_entradas
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.r_consola,
            "GAUSS-JORDAN / RREF"
        )

        self.log(
            self.r_consola,
            "MATRIZ AUMENTADA INICIAL:",
            "paso"
        )

        self.formatear_matriz(
            Ab,
            self.r_consola,
            aumentada=True
        )

        rref, pivotes, pasos, inconsistente = (
            modulo_sistemas.gauss_jordan_rref(
                self.rm,
                self.rn,
                Ab
            )
        )

        self.registrar_pasos(
            self.r_consola,
            pasos,
            pivotes,
            True
        )

        self.log(
            self.r_consola,
            "\nRREF FINAL:",
            "exito"
        )

        self.formatear_matriz(
            rref,
            self.r_consola,
            pivotes,
            True
        )

        if inconsistente:

            self.log(
                self.r_consola,
                "\nCONCLUSIÓN:",
                "paso"
            )

            self.log(
                self.r_consola,
                (
                    "La matriz contiene una "
                    "contradicción. El sistema "
                    "es inconsistente y no tiene "
                    "solución."
                ),
                "alerta"
            )

            return

        basicas, libres, solucion = (
            modulo_sistemas.construir_solucion_general(
                self.rm,
                self.rn,
                rref,
                pivotes
            )
        )

        self.log(
            self.r_consola,
            "\nANÁLISIS DE VARIABLES",
            "paso"
        )

        if len(basicas) > 0:

            texto = ""

            for i in range(len(basicas)):

                if i > 0:
                    texto += ", "

                texto += (
                    "x"
                    + a_subindice(
                        basicas[i] + 1
                    )
                )

            self.log(
                self.r_consola,
                "Variables básicas: " + texto
            )

        if len(libres) > 0:

            texto = ""

            for i in range(len(libres)):

                if i > 0:
                    texto += ", "

                texto += (
                    "x"
                    + a_subindice(
                        libres[i] + 1
                    )
                )

            self.log(
                self.r_consola,
                "Variables libres: " + texto
            )

        else:

            self.log(
                self.r_consola,
                "Variables libres: ninguna"
            )

        self.log(
            self.r_consola,
            "\nSOLUCIÓN:",
            "exito"
        )

        for linea in solucion:

            self.log(
                self.r_consola,
                linea,
                "exito"
            )

        self.log(
            self.r_consola,
            "\nCONCLUSIÓN:",
            "paso"
        )

        if len(libres) == 0:

            self.log(
                self.r_consola,
                (
                    "Existe un pivote para cada "
                    "variable. El sistema tiene "
                    "una única solución."
                ),
                "exito"
            )

        else:

            self.log(
                self.r_consola,
                (
                    "Existen variables libres. "
                    "El sistema tiene infinitas "
                    "soluciones."
                ),
                "exito"
            )

    # ============================================================
    # 3. ECUACIÓN MATRICIAL Ax
    # ============================================================

        # ============================================================
    # 3. ECUACIÓN MATRICIAL Ax = b
    # ============================================================

    def construir_modulo_ax(self, parent):
        """
        Construye el módulo de ecuación matricial.

        Este módulo permite realizar dos procedimientos:

        1. Sistema -> Ax = b
           El usuario introduce la matriz de coeficientes A
           y el vector de términos independientes b.
           El programa identifica automáticamente el vector
           incógnita x y escribe la forma matricial.

        2. Calcular Ax
           El usuario introduce A y un vector numérico x.
           El programa calcula el producto matriz-vector y
           explica su relación con combinación lineal.
        """

        ttk.Label(
            parent,
            text=(
                "Ecuación matricial Ax = b "
                "y producto matriz-vector"
            ),
            foreground=self.colors["comment"]
        ).pack(pady=5)

        # --------------------------------------------------------
        # DIMENSIONES
        # --------------------------------------------------------

        frame_dimensiones = ttk.Frame(parent)
        frame_dimensiones.pack(pady=5)

        ttk.Label(
            frame_dimensiones,
            text="Filas de A:"
        ).grid(
            row=0,
            column=0
        )

        self.ax_m = self.crear_entry_suave(
            frame_dimensiones
        )

        self.ax_m.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            frame_dimensiones,
            text="Columnas de A:"
        ).grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        self.ax_n = self.crear_entry_suave(
            frame_dimensiones
        )

        self.ax_n.grid(
            row=0,
            column=3,
            padx=5
        )

        self.crear_boton_suave(
            frame_dimensiones,
            "Generar",
            self.ax_generar
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        # --------------------------------------------------------
        # ZONA DE ENTRADA
        # --------------------------------------------------------

        self.ax_datos = tk.Frame(
            parent,
            bg=self.colors["bg_main"]
        )

        self.ax_datos.pack(
            pady=10
        )

        # Matriz A
        self.ax_frame_A = tk.Frame(
            self.ax_datos,
            bg=self.colors["bg_main"]
        )

        self.ax_frame_A.grid(
            row=0,
            column=0,
            padx=20
        )

        # Vector x
        self.ax_frame_x = tk.Frame(
            self.ax_datos,
            bg=self.colors["bg_main"]
        )

        self.ax_frame_x.grid(
            row=0,
            column=1,
            padx=20
        )

        # Vector b
        self.ax_frame_b = tk.Frame(
            self.ax_datos,
            bg=self.colors["bg_main"]
        )

        self.ax_frame_b.grid(
            row=0,
            column=2,
            padx=20
        )

        # --------------------------------------------------------
        # BOTONES
        # --------------------------------------------------------

        self.ax_frame_botones = ttk.Frame(
            parent
        )

        self.ax_frame_botones.pack(
            pady=5
        )

        self.ax_boton_forma = (
            self.crear_boton_suave(
                self.ax_frame_botones,
                "Sistema → Ax = b",
                self.ax_mostrar_forma
            )
        )

        self.ax_boton_forma.pack(
            side=tk.LEFT,
            padx=5
        )

        self.ax_boton_calcular = (
            self.crear_boton_suave(
                self.ax_frame_botones,
                "Calcular Ax",
                self.ax_calcular
            )
        )

        self.ax_boton_calcular.pack(
            side=tk.LEFT,
            padx=5
        )

        # --------------------------------------------------------
        # CONSOLA
        # --------------------------------------------------------

        self.ax_consola = (
            self.configurar_consola(
                parent
            )
        )

    # ============================================================
    # GENERAR CAMPOS
    # ============================================================

    def ax_generar(self):
        """
        Genera la matriz A, el vector x y el vector b
        de acuerdo con las dimensiones indicadas.
        """

        try:

            self.axm = int(
                self.ax_m.get()
            )

            self.axn = int(
                self.ax_n.get()
            )

            if (
                self.axm <= 0
                or
                self.axn <= 0
            ):
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                (
                    "Las dimensiones deben ser "
                    "números enteros positivos."
                )
            )

            return

        # Limpiar campos anteriores
        for widget in (
            self.ax_frame_A.winfo_children()
        ):
            widget.destroy()

        for widget in (
            self.ax_frame_x.winfo_children()
        ):
            widget.destroy()

        for widget in (
            self.ax_frame_b.winfo_children()
        ):
            widget.destroy()

        # ========================================================
        # MATRIZ A
        # ========================================================

        ttk.Label(
            self.ax_frame_A,
            text="Matriz A",
            foreground=self.colors["accent"]
        ).grid(
            row=0,
            column=0,
            columnspan=self.axn
        )

        self.ax_entradas_A = []

        for i in range(self.axm):

            fila = []

            for j in range(self.axn):

                entrada = self.crear_entry_suave(
                    self.ax_frame_A
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                fila.append(
                    entrada
                )

            self.ax_entradas_A.append(
                fila
            )

        # ========================================================
        # VECTOR x
        # ========================================================

        ttk.Label(
            self.ax_frame_x,
            text="Vector x",
            foreground=self.colors["warning"]
        ).grid(
            row=0,
            column=0
        )

        self.ax_entradas_x = []

        for i in range(self.axn):

            entrada = self.crear_entry_suave(
                self.ax_frame_x,
                True
            )

            entrada.grid(
                row=i + 1,
                column=0,
                padx=2,
                pady=2
            )

            self.ax_entradas_x.append(
                entrada
            )

        # ========================================================
        # VECTOR b
        # ========================================================

        ttk.Label(
            self.ax_frame_b,
            text="Vector b",
            foreground=self.colors["error"]
        ).grid(
            row=0,
            column=0
        )

        self.ax_entradas_b = []

        for i in range(self.axm):

            entrada = self.crear_entry_suave(
                self.ax_frame_b,
                True
            )

            entrada.grid(
                row=i + 1,
                column=0,
                padx=2,
                pady=2
            )

            self.ax_entradas_b.append(
                entrada
            )

    # ============================================================
    # SISTEMA -> Ax = b
    # ============================================================

    def ax_mostrar_forma(self):
        """
        Convierte la información de un sistema lineal
        a su representación matricial Ax = b.

        El usuario introduce A y b.
        Las variables x₁, x₂, ..., xₙ son generadas
        automáticamente porque representan incógnitas.
        """

        self.ax_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A = self.leer_matriz(
                self.ax_entradas_A
            )

            b = self.leer_vector(
                self.ax_entradas_b
            )

            informacion = (
                modulo_vectores.explicar_forma_matricial(
                    A,
                    b
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        # ========================================================
        # TÍTULO
        # ========================================================

        self.titulo_resultado(
            self.ax_consola,
            "SISTEMA DE ECUACIONES → FORMA MATRICIAL Ax = b"
        )

        self.log(
            self.ax_consola,
            (
                "Para escribir un sistema en forma "
                "matricial debemos identificar tres "
                "elementos:"
            ),
            "explicacion"
        )

        self.log(
            self.ax_consola,
            (
                "\nA = matriz de coeficientes"
                "\nx = vector de incógnitas"
                "\nb = vector de términos independientes"
            ),
            "explicacion"
        )

        # ========================================================
        # PASO 1
        # ========================================================

        self.log(
            self.ax_consola,
            "\nPASO 1. IDENTIFICAR LA MATRIZ DE COEFICIENTES A",
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "Tomamos los coeficientes de las variables "
                "en cada ecuación y los colocamos por filas."
            ),
            "explicacion"
        )

        self.log(
            self.ax_consola,
            "\nA =",
            "variable"
        )

        self.formatear_matriz(
            informacion["A"],
            self.ax_consola
        )

        # ========================================================
        # PASO 2
        # ========================================================

        self.log(
            self.ax_consola,
            "\nPASO 2. IDENTIFICAR EL VECTOR INCÓGNITA x",
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "Como A tiene "
                + str(self.axn)
                + " columnas, el sistema tiene "
                + str(self.axn)
                + " incógnitas."
            ),
            "explicacion"
        )

        self.log(
            self.ax_consola,
            "\nx =",
            "variable"
        )

        for i in range(self.axn):

            self.log(
                self.ax_consola,
                "[ x"
                + a_subindice(i + 1)
                + " ]",
                "matriz"
            )

        # ========================================================
        # PASO 3
        # ========================================================

        self.log(
            self.ax_consola,
            (
                "\nPASO 3. IDENTIFICAR EL VECTOR "
                "DE TÉRMINOS INDEPENDIENTES b"
            ),
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "Los valores situados al lado derecho "
                "de las ecuaciones forman el vector b."
            ),
            "explicacion"
        )

        self.mostrar_vector(
            self.ax_consola,
            informacion["b"],
            "\nb ="
        )

        # ========================================================
        # PASO 4
        # ========================================================

        self.log(
            self.ax_consola,
            "\nPASO 4. ESCRIBIR LA ECUACIÓN MATRICIAL",
            "paso"
        )

        self.log(
            self.ax_consola,
            "\nA x = b",
            "variable"
        )

        self.log(
            self.ax_consola,
            "\nA ="
        )

        self.formatear_matriz(
            informacion["A"],
            self.ax_consola
        )

        self.log(
            self.ax_consola,
            "\nx ="
        )

        for i in range(self.axn):

            self.log(
                self.ax_consola,
                "[ x"
                + a_subindice(i + 1)
                + " ]",
                "matriz"
            )

        self.log(
            self.ax_consola,
            "\nb ="
        )

        self.mostrar_vector(
            self.ax_consola,
            informacion["b"]
        )

        # ========================================================
        # REPRESENTACIÓN EN UNA SOLA ESTRUCTURA
        # ========================================================

        self.log(
            self.ax_consola,
            "\nFORMA MATRICIAL:",
            "exito"
        )

        self._mostrar_ax_igual_b(
            self.ax_consola,
            informacion["A"],
            informacion["b"]
        )

        # ========================================================
        # PASO 5
        # ========================================================

        self.log(
            self.ax_consola,
            (
                "\nPASO 5. COMPROBACIÓN CON "
                "LAS ECUACIONES"
            ),
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "Cada fila de A produce una ecuación "
                "del sistema original:"
            ),
            "explicacion"
        )

        for i in range(
            len(informacion["ecuaciones"])
        ):

            self.log(
                self.ax_consola,
                (
                    "Ecuación "
                    + str(i + 1)
                    + ":  "
                    + informacion["ecuaciones"][i]
                ),
                "matriz"
            )

        # ========================================================
        # CONCLUSIÓN
        # ========================================================

        self.log(
            self.ax_consola,
            "\nCONCLUSIÓN:",
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "El sistema ha sido expresado "
                "correctamente en la forma matricial:\n\n"
                "A x = b"
            ),
            "exito"
        )

    # ============================================================
    # MOSTRAR Ax = b HORIZONTALMENTE
    # ============================================================

    def _mostrar_ax_igual_b(
        self,
        consola,
        A,
        b
    ):
        """
        Presenta visualmente:

                 A          x       b

        [ ... ... ... ]   [x₁]   [b₁]
        [ ... ... ... ] × [x₂] = [b₂]
        [ ... ... ... ]   [x₃]   [b₃]

        No realiza operaciones matemáticas.
        Solo construye una representación legible.
        """

        filas = len(A)
        columnas = len(A[0])

        # Convertir cada fila de A a texto.
        lineas_A = []

        for i in range(filas):

            valores = []

            for j in range(columnas):

                valores.append(
                    "{:^7}".format(
                        a_fraccion_str(
                            A[i][j]
                        )
                    )
                )

            lineas_A.append(
                "[ "
                + " ".join(valores)
                + " ]"
            )

        # Vector incógnita.
        lineas_x = []

        for j in range(columnas):

            lineas_x.append(
                "[ "
                + "x"
                + a_subindice(j + 1)
                + " "
                + "]"
            )

        # Vector b.
        lineas_b = []

        for i in range(len(b)):

            lineas_b.append(
                "[ "
                + a_fraccion_str(b[i])
                + " ]"
            )

        # Normalmente, en Ax=b para un sistema,
        # la cantidad de filas de A y de b coincide.
        # El vector x puede tener otra cantidad de filas,
        # por eso calculamos la mayor altura.
        altura = max(
            len(lineas_A),
            len(lineas_x),
            len(lineas_b)
        )

        centro = altura // 2

        for i in range(altura):

            texto_A = ""

            if i < len(lineas_A):
                texto_A = lineas_A[i]

            texto_x = ""

            if i < len(lineas_x):
                texto_x = lineas_x[i]

            texto_b = ""

            if i < len(lineas_b):
                texto_b = lineas_b[i]

            # Operadores solo en la fila central.
            if i == centro:

                operador_producto = "  ×  "
                operador_igual = "  =  "

            else:

                operador_producto = "     "
                operador_igual = "     "

            linea = (
                "{:<35}".format(texto_A)
                + operador_producto
                + "{:<10}".format(texto_x)
                + operador_igual
                + texto_b
            )

            self.log(
                consola,
                linea,
                "matriz"
            )

    # ============================================================
    # CALCULAR Ax
    # ============================================================

    def ax_calcular(self):
        """
        Calcula el producto de una matriz A por un vector
        numérico x.

        Además muestra que Ax equivale a una combinación
        lineal de las columnas de A.
        """

        self.ax_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A = self.leer_matriz(
                self.ax_entradas_A
            )

            x = self.leer_vector(
                self.ax_entradas_x
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.ax_consola,
            "PRODUCTO MATRIZ-VECTOR Ax"
        )

        # ========================================================
        # PASO 1
        # ========================================================

        self.log(
            self.ax_consola,
            "PASO 1. IDENTIFICAR LA MATRIZ A",
            "paso"
        )

        self.log(
            self.ax_consola,
            "\nA =",
            "variable"
        )

        self.formatear_matriz(
            A,
            self.ax_consola
        )

        # ========================================================
        # PASO 2
        # ========================================================

        self.log(
            self.ax_consola,
            "\nPASO 2. IDENTIFICAR EL VECTOR x",
            "paso"
        )

        self.mostrar_vector(
            self.ax_consola,
            x,
            "\nx ="
        )

        # ========================================================
        # PASO 3
        # ========================================================

        b, detalles = (
            modulo_vectores.producto_ax(
                self.axm,
                self.axn,
                A,
                x
            )
        )

        self.log(
            self.ax_consola,
            (
                "\nPASO 3. MULTIPLICAR CADA "
                "FILA DE A POR x"
            ),
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "Cada componente del resultado se obtiene "
                "haciendo el producto punto entre una fila "
                "de A y el vector x."
            ),
            "explicacion"
        )

        for detalle in detalles:

            self.log(
                self.ax_consola,
                "\n" + detalle,
                "matriz"
            )

        # ========================================================
        # PASO 4
        # ========================================================

        self.log(
            self.ax_consola,
            "\nPASO 4. RESULTADO DEL PRODUCTO",
            "paso"
        )

        self.mostrar_vector(
            self.ax_consola,
            b,
            "\nAx =",
            "exito"
        )

        # ========================================================
        # PASO 5 - COMBINACIÓN LINEAL
        # ========================================================

        (
            columnas,
            resultado,
            explicacion
        ) = modulo_vectores.explicar_ax_combinacion(
            A,
            x
        )

        self.log(
            self.ax_consola,
            (
                "\nPASO 5. INTERPRETAR Ax COMO "
                "COMBINACIÓN LINEAL"
            ),
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "Una multiplicación matriz-vector también "
                "puede interpretarse como una combinación "
                "lineal de las columnas de A."
            ),
            "explicacion"
        )

        for linea in explicacion:

            self.log(
                self.ax_consola,
                linea,
                "explicacion"
            )

        # ========================================================
        # MOSTRAR CADA COLUMNA
        # ========================================================

        self.log(
            self.ax_consola,
            "\nCOLUMNAS DE A:",
            "paso"
        )

        for j in range(len(columnas)):

            self.mostrar_vector(
                self.ax_consola,
                columnas[j],
                (
                    "\na"
                    + a_subindice(j + 1)
                    + " ="
                )
            )

        # ========================================================
        # COMBINACIÓN EXPLÍCITA
        # ========================================================

        self.log(
            self.ax_consola,
            "\nCOMBINACIÓN LINEAL EXPLÍCITA:",
            "paso"
        )

        combinacion = ""

        for j in range(len(x)):

            if j > 0:
                combinacion += " + "

            combinacion += (
                "("
                + a_fraccion_str(x[j])
                + ")a"
                + a_subindice(j + 1)
            )

        self.log(
            self.ax_consola,
            "Ax = " + combinacion,
            "variable"
        )

        # ========================================================
        # MOSTRAR VECTORES ESCALADOS
        # ========================================================

        self.log(
            self.ax_consola,
            (
                "\nMultiplicamos cada columna "
                "por su escalar:"
            ),
            "explicacion"
        )

        vectores_escalados = []

        for j in range(len(columnas)):

            vector_escalado = (
                modulo_vectores.escalar_vector(
                    x[j],
                    columnas[j]
                )
            )

            vectores_escalados.append(
                vector_escalado
            )

            self.mostrar_vector(
                self.ax_consola,
                vector_escalado,
                (
                    "\n("
                    + a_fraccion_str(x[j])
                    + ")a"
                    + a_subindice(j + 1)
                    + " ="
                )
            )

        # ========================================================
        # SUMA DE LOS VECTORES ESCALADOS
        # ========================================================

        if len(vectores_escalados) > 0:

            suma_columnas = (
                vectores_escalados[0][:]
            )

            for j in range(
                1,
                len(vectores_escalados)
            ):

                suma_columnas = (
                    modulo_vectores.sumar_vectores(
                        suma_columnas,
                        vectores_escalados[j]
                    )
                )

            self.log(
                self.ax_consola,
                (
                    "\nSumando los vectores "
                    "anteriores obtenemos:"
                ),
                "explicacion"
            )

            self.mostrar_vector(
                self.ax_consola,
                suma_columnas,
                "\nResultado =",
                "exito"
            )

        # ========================================================
        # CONCLUSIÓN
        # ========================================================

        self.log(
            self.ax_consola,
            "\nCONCLUSIÓN:",
            "paso"
        )

        self.log(
            self.ax_consola,
            (
                "El producto Ax es una combinación "
                "lineal de las columnas de A.\n"
                "Los escalares de la combinación son "
                "exactamente las componentes del vector x."
            ),
            "exito"
        )

    # ============================================================
    # 4. VECTORES Y COMBINACIÓN LINEAL
    # ============================================================

    def construir_modulo_vectores(
        self,
        parent
    ):

        ttk.Label(
            parent,
            text=(
                "Operaciones con vectores, combinación lineal "
                "e independencia lineal"
            ),
            foreground=self.colors["comment"]
        ).pack(pady=5)

        frame = ttk.Frame(parent)
        frame.pack()

        ttk.Label(
            frame,
            text="Dimensión (n):"
        ).grid(row=0, column=0)

        self.v_n = self.crear_entry_suave(
            frame
        )

        self.v_n.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            frame,
            text="Cantidad de vectores (k):"
        ).grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        self.v_k = self.crear_entry_suave(
            frame
        )

        self.v_k.grid(
            row=0,
            column=3,
            padx=5
        )

        self.crear_boton_suave(
            frame,
            "Generar",
            self.vector_generar
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.v_frame = tk.Frame(
            parent,
            bg=self.colors["bg_main"]
        )

        self.v_frame.pack(pady=10)

        frame_botones = ttk.Frame(parent)
        frame_botones.pack(pady=5)

        self.crear_boton_suave(
            frame_botones,
            "u + v",
            self.vector_sumar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            frame_botones,
            "u - v",
            self.vector_restar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            frame_botones,
            "c · u",
            self.vector_escalar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            frame_botones,
            "¿b es combinación lineal?",
            self.vector_combinacion
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            frame_botones,
            "Independencia L.I. / L.D.",
            self.vector_independencia
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            frame_botones,
            "0. Teoremas clave",
            self.vector_teoremas
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.v_consola = (
            self.configurar_consola(
                parent
            )
        )

    def vector_generar(self):

        try:

            self.vn = int(
                self.v_n.get()
            )

            self.vk = int(
                self.v_k.get()
            )

            if self.vn <= 0 or self.vk <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "n y k deben ser enteros positivos."
            )

            return

        for widget in self.v_frame.winfo_children():
            widget.destroy()

        self.v_vectores = []

        for j in range(self.vk):

            ttk.Label(
                self.v_frame,
                text="v" + a_subindice(j + 1)
            ).grid(
                row=0,
                column=j,
                padx=8
            )

            columna = []

            for i in range(self.vn):

                entrada = self.crear_entry_suave(
                    self.v_frame
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                columna.append(entrada)

            self.v_vectores.append(columna)

        ttk.Label(
            self.v_frame,
            text="b",
            foreground=self.colors["error"]
        ).grid(
            row=0,
            column=self.vk,
            padx=10
        )

        self.v_b = []

        for i in range(self.vn):

            entrada = self.crear_entry_suave(
                self.v_frame,
                True
            )

            entrada.grid(
                row=i + 1,
                column=self.vk,
                padx=2,
                pady=2
            )

            self.v_b.append(entrada)

        ttk.Label(
            self.v_frame,
            text="Escalar c"
        ).grid(
            row=0,
            column=self.vk + 1,
            padx=10
        )

        self.v_c = self.crear_entry_suave(
            self.v_frame
        )

        self.v_c.grid(
            row=1,
            column=self.vk + 1,
            padx=5
        )

    def vector_obtener(
        self,
        indice
    ):

        if indice >= len(self.v_vectores):

            raise ValueError(
                "Para esta operación debe generar "
                "al menos dos vectores."
            )

        return self.leer_vector(
            self.v_vectores[indice]
        )

    def vector_sumar(self):

        self.v_consola.delete(
            "1.0",
            tk.END
        )

        try:

            u = self.vector_obtener(0)
            v = self.vector_obtener(1)

            resultado, detalles = (
                modulo_vectores.sumar_vectores_detallado(
                    u,
                    v
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.v_consola,
            "SUMA DE VECTORES u + v"
        )

        self.mostrar_vector(
            self.v_consola,
            u,
            "u ="
        )

        self.log(self.v_consola)

        self.mostrar_vector(
            self.v_consola,
            v,
            "v ="
        )

        self.log(
            self.v_consola,
            "\nSumamos componente a componente:",
            "paso"
        )

        for detalle in detalles:

            self.log(
                self.v_consola,
                detalle,
                "matriz"
            )

        self.log(
            self.v_consola,
            "\nRESULTADO:",
            "exito"
        )

        self.mostrar_vector(
            self.v_consola,
            resultado,
            "u + v =",
            "exito"
        )

    def vector_restar(self):

        self.v_consola.delete(
            "1.0",
            tk.END
        )

        try:

            u = self.vector_obtener(0)
            v = self.vector_obtener(1)

            resultado, detalles = (
                modulo_vectores.restar_vectores_detallado(
                    u,
                    v
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.v_consola,
            "RESTA DE VECTORES u - v"
        )

        self.log(
            self.v_consola,
            "Restamos componente a componente:",
            "paso"
        )

        for detalle in detalles:

            self.log(
                self.v_consola,
                detalle,
                "matriz"
            )

        self.log(
            self.v_consola,
            "\nRESULTADO:",
            "exito"
        )

        self.mostrar_vector(
            self.v_consola,
            resultado,
            "u - v =",
            "exito"
        )

    def vector_escalar(self):

        self.v_consola.delete(
            "1.0",
            tk.END
        )

        try:

            u = self.vector_obtener(0)

            c = parsear_entrada(
                self.v_c.get()
            )

            resultado, detalles = (
                modulo_vectores.escalar_vector_detallado(
                    c,
                    u
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.v_consola,
            "MULTIPLICACIÓN DE VECTOR POR ESCALAR"
        )

        self.log(
            self.v_consola,
            "Escalar c = "
            + a_fraccion_str(c),
            "variable"
        )

        self.mostrar_vector(
            self.v_consola,
            u,
            "\nVector u ="
        )

        self.log(
            self.v_consola,
            "\nMultiplicamos cada componente:",
            "paso"
        )

        for detalle in detalles:

            self.log(
                self.v_consola,
                detalle,
                "matriz"
            )

        self.log(
            self.v_consola,
            "\nRESULTADO:",
            "exito"
        )

        self.mostrar_vector(
            self.v_consola,
            resultado,
            "cu =",
            "exito"
        )

    def vector_combinacion(self):

        self.v_consola.delete(
            "1.0",
            tk.END
        )

        try:

            vectores = []

            for entradas in self.v_vectores:

                vectores.append(
                    self.leer_vector(
                        entradas
                    )
                )

            b = self.leer_vector(
                self.v_b
            )

            (
                es_cl,
                rref,
                pivotes,
                pasos,
                explicacion,
                solucion
            ) = modulo_vectores.explicar_combinacion_lineal(
                vectores,
                b
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.v_consola,
            "COMBINACIÓN LINEAL"
        )

        self.log(
            self.v_consola,
            (
                "Buscamos escalares c₁, c₂, ..., "
                "cₖ tales que:"
            ),
            "paso"
        )

        terminos = ""

        for i in range(self.vk):

            if i > 0:
                terminos += " + "

            terminos += (
                "c"
                + a_subindice(i + 1)
                + "v"
                + a_subindice(i + 1)
            )

        self.log(
            self.v_consola,
            terminos + " = b",
            "variable"
        )

        self.log(
            self.v_consola,
            "\nMATRIZ AUMENTADA:",
            "paso"
        )

        Ab = []

        for i in range(self.vn):

            fila = []

            for j in range(self.vk):

                vector_j = self.leer_vector(
                    self.v_vectores[j]
                )

                fila.append(
                    vector_j[i]
                )

            fila.append(b[i])
            Ab.append(fila)

        self.formatear_matriz(
            Ab,
            self.v_consola,
            aumentada=True
        )

        self.log(
            self.v_consola,
            "\nREDUCCIÓN POR GAUSS-JORDAN:",
            "paso"
        )

        self.registrar_pasos(
            self.v_consola,
            pasos,
            pivotes,
            True
        )

        self.log(
            self.v_consola,
            "\nRREF FINAL:",
            "exito"
        )

        self.formatear_matriz(
            rref,
            self.v_consola,
            pivotes,
            True
        )

        self.log(
            self.v_consola,
            "\nINTERPRETACIÓN:",
            "paso"
        )

        for linea in explicacion:

            self.log(
                self.v_consola,
                linea,
                "explicacion"
            )

        if es_cl:

            self.log(
                self.v_consola,
                "\nESCALARES:",
                "exito"
            )

            for linea in solucion:

                texto = linea

                for i in range(self.vk):

                    texto = texto.replace(
                        "x" + a_subindice(i + 1),
                        "c" + a_subindice(i + 1)
                    )

                self.log(
                    self.v_consola,
                    texto,
                    "exito"
                )

            self.log(
                self.v_consola,
                "\nCONCLUSIÓN:",
                "paso"
            )

            self.log(
                self.v_consola,
                (
                    "El sistema es consistente. "
                    "Por tanto, b SÍ es combinación "
                    "lineal de los vectores dados."
                ),
                "exito"
            )

        else:

            self.log(
                self.v_consola,
                "\nCONCLUSIÓN:",
                "paso"
            )

            self.log(
                self.v_consola,
                (
                    "El sistema es inconsistente. "
                    "Por tanto, b NO es combinación "
                    "lineal de los vectores dados."
                ),
                "alerta"
            )

    def vector_independencia(self):

        self.v_consola.delete(
            "1.0",
            tk.END
        )

        try:

            if not hasattr(self, "v_vectores"):
                raise ValueError(
                    "Primero indique n y k y presione Generar."
                )

            vectores = []

            for entradas in self.v_vectores:
                vectores.append(
                    self.leer_vector(entradas)
                )

            if not vectores:
                raise ValueError(
                    "Debe ingresar al menos un vector."
                )

            # Cada vector v_j se coloca como una columna de A.
            # Si hay k vectores en R^n, A tiene n filas y k columnas.
            A = []

            for i in range(self.vn):
                fila = []

                for j in range(self.vk):
                    fila.append(vectores[j][i])

                A.append(fila)

            # Sistema homogéneo A c = 0.
            Ab = []

            for fila in A:
                Ab.append(fila[:] + [0])

            escalonada, pasos, pivotes = (
                modulo_sistemas.eliminacion_gaussiana(
                    self.vn,
                    self.vk,
                    Ab
                )
            )

            columnas_pivote = []

            for _, columna in pivotes:
                if columna < self.vk and columna not in columnas_pivote:
                    columnas_pivote.append(columna)

            columnas_libres = [
                j
                for j in range(self.vk)
                if j not in columnas_pivote
            ]

            cantidad_pivotes = len(columnas_pivote)
            cantidad_libres = len(columnas_libres)
            es_independiente = cantidad_libres == 0

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.v_consola,
            "INDEPENDENCIA LINEAL"
        )

        self.log(
            self.v_consola,
            (
                "Analizamos "
                + str(self.vk)
                + " vector(es) en R^"
                + str(self.vn)
                + "."
            ),
            "explicacion"
        )

        self.log(
            self.v_consola,
            "\nPASO 1. Planteamos la combinación homogénea:",
            "paso"
        )

        terminos = []

        for j in range(self.vk):
            terminos.append(
                "c"
                + a_subindice(j + 1)
                + "v"
                + a_subindice(j + 1)
            )

        self.log(
            self.v_consola,
            " + ".join(terminos) + " = 0",
            "variable"
        )

        self.log(
            self.v_consola,
            (
                "Buscamos si el sistema homogéneo tiene solamente "
                "la solución trivial o también soluciones no triviales."
            ),
            "explicacion"
        )

        self.log(
            self.v_consola,
            "\nPASO 2. Formamos A colocando los vectores como columnas:",
            "paso"
        )

        self.formatear_matriz(
            A,
            self.v_consola
        )

        self.log(
            self.v_consola,
            "\nPASO 3. Construimos el sistema homogéneo A·c = 0:",
            "paso"
        )

        self.formatear_matriz(
            Ab,
            self.v_consola,
            aumentada=True
        )

        self.log(
            self.v_consola,
            "\nPASO 4. Reducimos la matriz por eliminación gaussiana:",
            "paso"
        )

        self.registrar_pasos(
            self.v_consola,
            pasos,
            pivotes,
            True
        )

        self.log(
            self.v_consola,
            "\nMATRIZ ESCALONADA FINAL:",
            "exito"
        )

        self.formatear_matriz(
            escalonada,
            self.v_consola,
            pivotes,
            True
        )

        self.log(
            self.v_consola,
            "\nPASO 5. Analizamos pivotes y variables libres:",
            "paso"
        )

        self.log(
            self.v_consola,
            "Cantidad de vectores (k): " + str(self.vk),
            "matriz"
        )

        self.log(
            self.v_consola,
            "Cantidad de pivotes: " + str(cantidad_pivotes),
            "matriz"
        )

        if columnas_pivote:
            texto_pivotes = ", ".join(
                "c" + a_subindice(j + 1)
                for j in columnas_pivote
            )
        else:
            texto_pivotes = "Ninguna"

        self.log(
            self.v_consola,
            "Variables con pivote: " + texto_pivotes,
            "variable"
        )

        self.log(
            self.v_consola,
            "Cantidad de variables libres: " + str(cantidad_libres),
            "matriz"
        )

        if columnas_libres:
            texto_libres = ", ".join(
                "c" + a_subindice(j + 1)
                for j in columnas_libres
            )

            self.log(
                self.v_consola,
                "Variables libres: " + texto_libres,
                "alerta"
            )
        else:
            self.log(
                self.v_consola,
                "Variables libres: ninguna.",
                "exito"
            )

        self.log(
            self.v_consola,
            "\nINTERPRETACIÓN TEÓRICA:",
            "paso"
        )

        if es_independiente:

            self.log(
                self.v_consola,
                (
                    "No existen variables libres. Por tanto, el sistema "
                    "homogéneo solo admite la solución trivial:"
                ),
                "explicacion"
            )

            solucion_trivial = []

            for j in range(self.vk):
                solucion_trivial.append(
                    "c" + a_subindice(j + 1) + " = 0"
                )

            self.log(
                self.v_consola,
                ", ".join(solucion_trivial),
                "variable"
            )

            self.log(
                self.v_consola,
                "\nVEREDICTO: LINEALMENTE INDEPENDIENTE (L.I.)",
                "exito"
            )

            self.log(
                self.v_consola,
                (
                    "Como la única combinación que produce el vector cero "
                    "es la combinación trivial, los vectores son L.I."
                ),
                "exito"
            )

        else:

            self.log(
                self.v_consola,
                (
                    "Existe al menos una variable libre. Por tanto, el "
                    "sistema homogéneo admite soluciones no triviales."
                ),
                "explicacion"
            )

            self.log(
                self.v_consola,
                "\nVEREDICTO: LINEALMENTE DEPENDIENTE (L.D.)",
                "alerta"
            )

            self.log(
                self.v_consola,
                (
                    "Existe una combinación de los vectores, con al menos "
                    "un coeficiente distinto de cero, que produce el vector cero."
                ),
                "alerta"
            )

    def vector_teoremas(self):

        self.v_consola.delete(
            "1.0",
            tk.END
        )

        self.titulo_resultado(
            self.v_consola,
            "TEOREMAS CLAVE - VECTORES E INDEPENDENCIA LINEAL"
        )

        lineas = [
            "1. Un conjunto {v₁, v₂, ..., vₖ} es linealmente independiente si y solo si",
            "   la ecuación c₁v₁ + c₂v₂ + ... + cₖvₖ = 0 tiene únicamente la solución trivial.",
            "",
            "2. Solución trivial significa:",
            "   c₁ = c₂ = ... = cₖ = 0.",
            "",
            "3. Si al reducir la matriz aparecen variables libres, existen soluciones no triviales",
            "   y el conjunto es linealmente dependiente (L.D.).",
            "",
            "4. Si cada variable tiene pivote y no existen variables libres, el conjunto es",
            "   linealmente independiente (L.I.).",
            "",
            "5. Para analizar los vectores, se colocan como columnas de A y se estudia",
            "   el sistema homogéneo A·c = 0."
        ]

        for linea in lineas:
            self.log(
                self.v_consola,
                linea,
                "explicacion"
            )

    # ============================================================
    # 5. OPERACIONES MATRICIALES
    # ============================================================

    def construir_modulo_matrices(
        self,
        parent
    ):

        ttk.Label(
            parent,
            text=(
                "Suma, resta, producto por escalar "
                "y multiplicación de matrices"
            ),
            foreground=self.colors["comment"]
        ).pack(pady=5)

        frame = ttk.Frame(parent)
        frame.pack(pady=5)

        ttk.Label(
            frame,
            text="A: filas"
        ).grid(row=0, column=0)

        self.m_am = self.crear_entry_suave(
            frame
        )

        self.m_am.grid(row=0, column=1)

        ttk.Label(
            frame,
            text="columnas"
        ).grid(row=0, column=2)

        self.m_an = self.crear_entry_suave(
            frame
        )

        self.m_an.grid(row=0, column=3)

        ttk.Label(
            frame,
            text="B: filas"
        ).grid(
            row=0,
            column=4,
            padx=(15, 0)
        )

        self.m_bm = self.crear_entry_suave(
            frame
        )

        self.m_bm.grid(row=0, column=5)

        ttk.Label(
            frame,
            text="columnas"
        ).grid(row=0, column=6)

        self.m_bn = self.crear_entry_suave(
            frame
        )

        self.m_bn.grid(row=0, column=7)

        self.crear_boton_suave(
            frame,
            "Generar",
            self.matriz_generar
        ).grid(
            row=0,
            column=8,
            padx=10
        )

        self.m_frame = tk.Frame(
            parent,
            bg=self.colors["bg_main"]
        )

        self.m_frame.pack(pady=10)

        self.m_frame_A = tk.Frame(
            self.m_frame,
            bg=self.colors["bg_main"]
        )

        self.m_frame_A.grid(
            row=0,
            column=0,
            padx=20
        )

        self.m_frame_B = tk.Frame(
            self.m_frame,
            bg=self.colors["bg_main"]
        )

        self.m_frame_B.grid(
            row=0,
            column=1,
            padx=20
        )

        self.m_frame_c = tk.Frame(
            self.m_frame,
            bg=self.colors["bg_main"]
        )

        self.m_frame_c.grid(
            row=0,
            column=2,
            padx=20
        )

        botones = ttk.Frame(parent)
        botones.pack(pady=5)

        self.crear_boton_suave(
            botones,
            "A + B",
            self.matriz_sumar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            botones,
            "A - B",
            self.matriz_restar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            botones,
            "cA",
            self.matriz_escalar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.crear_boton_suave(
            botones,
            "A × B",
            self.matriz_multiplicar
        ).pack(
            side=tk.LEFT,
            padx=3
        )

        self.m_consola = (
            self.configurar_consola(
                parent
            )
        )

    def matriz_generar(self):

        try:

            self.mam = int(self.m_am.get())
            self.man = int(self.m_an.get())
            self.mbm = int(self.m_bm.get())
            self.mbn = int(self.m_bn.get())

            if (
                self.mam <= 0
                or self.man <= 0
                or self.mbm <= 0
                or self.mbn <= 0
            ):
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Todas las dimensiones deben ser positivas."
            )

            return

        for widget in self.m_frame_A.winfo_children():
            widget.destroy()

        for widget in self.m_frame_B.winfo_children():
            widget.destroy()

        for widget in self.m_frame_c.winfo_children():
            widget.destroy()

        ttk.Label(
            self.m_frame_A,
            text="Matriz A",
            foreground=self.colors["accent"]
        ).grid(
            row=0,
            column=0,
            columnspan=self.man
        )

        self.m_A = []

        for i in range(self.mam):

            fila = []

            for j in range(self.man):

                entrada = self.crear_entry_suave(
                    self.m_frame_A
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                fila.append(entrada)

            self.m_A.append(fila)

        ttk.Label(
            self.m_frame_B,
            text="Matriz B",
            foreground=self.colors["warning"]
        ).grid(
            row=0,
            column=0,
            columnspan=self.mbn
        )

        self.m_B = []

        for i in range(self.mbm):

            fila = []

            for j in range(self.mbn):

                entrada = self.crear_entry_suave(
                    self.m_frame_B
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                fila.append(entrada)

            self.m_B.append(fila)

        ttk.Label(
            self.m_frame_c,
            text="Escalar c"
        ).grid(row=0, column=0)

        self.m_c = self.crear_entry_suave(
            self.m_frame_c
        )

        self.m_c.grid(
            row=1,
            column=0,
            pady=5
        )

    def matriz_leer_AB(self):

        A = self.leer_matriz(
            self.m_A
        )

        B = self.leer_matriz(
            self.m_B
        )

        return A, B

    def matriz_sumar(self):

        self.m_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A, B = self.matriz_leer_AB()

            resultado, detalles = (
                modulo_matrices.sumar_matrices_detallado(
                    A,
                    B
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.m_consola,
            "SUMA DE MATRICES A + B"
        )

        self.log(
            self.m_consola,
            "Se suman los elementos que ocupan "
            "la misma posición.",
            "explicacion"
        )

        for detalle in detalles:

            self.log(
                self.m_consola,
                "\n" + detalle,
                "matriz"
            )

        self.log(
            self.m_consola,
            "\nRESULTADO:",
            "exito"
        )

        self.formatear_matriz(
            resultado,
            self.m_consola
        )

    def matriz_restar(self):

        self.m_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A, B = self.matriz_leer_AB()

            resultado, detalles = (
                modulo_matrices.restar_matrices_detallado(
                    A,
                    B
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.m_consola,
            "RESTA DE MATRICES A - B"
        )

        for detalle in detalles:

            self.log(
                self.m_consola,
                "\n" + detalle,
                "matriz"
            )

        self.log(
            self.m_consola,
            "\nRESULTADO:",
            "exito"
        )

        self.formatear_matriz(
            resultado,
            self.m_consola
        )

    def matriz_escalar(self):

        self.m_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A = self.leer_matriz(
                self.m_A
            )

            c = parsear_entrada(
                self.m_c.get()
            )

            resultado, detalles = (
                modulo_matrices.escalar_matriz_detallado(
                    c,
                    A
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.m_consola,
            "MULTIPLICACIÓN DE MATRIZ POR ESCALAR"
        )

        self.log(
            self.m_consola,
            "Escalar c = "
            + a_fraccion_str(c),
            "variable"
        )

        self.log(
            self.m_consola,
            (
                "\nMultiplicamos cada elemento "
                "de A por c:"
            ),
            "paso"
        )

        for detalle in detalles:

            self.log(
                self.m_consola,
                "\n" + detalle,
                "matriz"
            )

        self.log(
            self.m_consola,
            "\nRESULTADO cA:",
            "exito"
        )

        self.formatear_matriz(
            resultado,
            self.m_consola
        )

    def matriz_multiplicar(self):

        self.m_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A, B = self.matriz_leer_AB()

            resultado, detalles = (
                modulo_matrices.multiplicar_matrices(
                    A,
                    B
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.m_consola,
            "MULTIPLICACIÓN DE MATRICES A × B"
        )

        self.log(
            self.m_consola,
            "PASO 1. Matriz A:",
            "paso"
        )

        self.formatear_matriz(
            A,
            self.m_consola
        )

        self.log(
            self.m_consola,
            "\nPASO 2. Matriz B:",
            "paso"
        )

        self.formatear_matriz(
            B,
            self.m_consola
        )

        self.log(
            self.m_consola,
            "\nPASO 3. Verificación de dimensiones:",
            "paso"
        )

        self.log(
            self.m_consola,
            (
                "A es "
                + str(len(A))
                + "×"
                + str(len(A[0]))
                + "\nB es "
                + str(len(B))
                + "×"
                + str(len(B[0]))
            ),
            "explicacion"
        )

        self.log(
            self.m_consola,
            (
                "\nLas columnas de A coinciden "
                "con las filas de B. "
                "La multiplicación está definida."
            ),
            "exito"
        )

        self.log(
            self.m_consola,
            "\nPASO 4. Producto fila por columna:",
            "paso"
        )

        for detalle in detalles:

            self.log(
                self.m_consola,
                "\n" + detalle,
                "matriz"
            )

        self.log(
            self.m_consola,
            "\nRESULTADO A × B:",
            "exito"
        )

        self.formatear_matriz(
            resultado,
            self.m_consola
        )

    # ============================================================
    # 6. PROPIEDADES Ax
    # ============================================================

    def construir_modulo_propiedades(
        self,
        parent
    ):

        ttk.Label(
            parent,
            text=(
                "Verificación paso a paso "
                "de propiedades de Ax"
            ),
            foreground=self.colors["comment"]
        ).pack(pady=5)

        frame = ttk.Frame(parent)
        frame.pack()

        ttk.Label(
            frame,
            text="Filas A:"
        ).grid(row=0, column=0)

        self.p_m = self.crear_entry_suave(
            frame
        )

        self.p_m.grid(
            row=0,
            column=1
        )

        ttk.Label(
            frame,
            text="Columnas A:"
        ).grid(
            row=0,
            column=2,
            padx=(10, 0)
        )

        self.p_n = self.crear_entry_suave(
            frame
        )

        self.p_n.grid(
            row=0,
            column=3
        )

        self.crear_boton_suave(
            frame,
            "Generar",
            self.prop_generar
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        self.p_frame = tk.Frame(
            parent,
            bg=self.colors["bg_main"]
        )

        self.p_frame.pack(pady=10)

        botones = ttk.Frame(parent)
        botones.pack(pady=5)

        self.crear_boton_suave(
            botones,
            "A(u+v) = Au+Av",
            self.prop_suma
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        self.crear_boton_suave(
            botones,
            "A(cu) = c(Au)",
            self.prop_escalar
        ).pack(
            side=tk.LEFT,
            padx=5
        )

        self.p_consola = (
            self.configurar_consola(
                parent
            )
        )

    def prop_generar(self):

        try:

            self.pm = int(self.p_m.get())
            self.pn = int(self.p_n.get())

            if self.pm <= 0 or self.pn <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Las dimensiones deben ser positivas."
            )

            return

        for widget in self.p_frame.winfo_children():
            widget.destroy()

        ttk.Label(
            self.p_frame,
            text="Matriz A",
            foreground=self.colors["accent"]
        ).grid(
            row=0,
            column=0,
            columnspan=self.pn
        )

        self.p_A = []

        for i in range(self.pm):

            fila = []

            for j in range(self.pn):

                entrada = self.crear_entry_suave(
                    self.p_frame
                )

                entrada.grid(
                    row=i + 1,
                    column=j,
                    padx=2,
                    pady=2
                )

                fila.append(entrada)

            self.p_A.append(fila)

        columna_u = self.pn + 1

        ttk.Label(
            self.p_frame,
            text="u",
            foreground=self.colors["warning"]
        ).grid(
            row=0,
            column=columna_u
        )

        self.p_u = []

        for i in range(self.pn):

            entrada = self.crear_entry_suave(
                self.p_frame,
                True
            )

            entrada.grid(
                row=i + 1,
                column=columna_u,
                padx=5
            )

            self.p_u.append(entrada)

        columna_v = self.pn + 2

        ttk.Label(
            self.p_frame,
            text="v",
            foreground=self.colors["success"]
        ).grid(
            row=0,
            column=columna_v
        )

        self.p_v = []

        for i in range(self.pn):

            entrada = self.crear_entry_suave(
                self.p_frame,
                True
            )

            entrada.grid(
                row=i + 1,
                column=columna_v,
                padx=5
            )

            self.p_v.append(entrada)

        columna_c = self.pn + 3

        ttk.Label(
            self.p_frame,
            text="Escalar c",
            foreground=self.colors["error"]
        ).grid(
            row=0,
            column=columna_c,
            padx=10
        )

        self.p_c = self.crear_entry_suave(
            self.p_frame
        )

        self.p_c.grid(
            row=1,
            column=columna_c
        )

    def prop_suma(self):

        self.p_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A = self.leer_matriz(
                self.p_A
            )

            u = self.leer_vector(
                self.p_u
            )

            v = self.leer_vector(
                self.p_v
            )

            resultado = (
                modulo_matrices
                .verificar_propiedad_suma_detallada(
                    A,
                    u,
                    v
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.p_consola,
            "VERIFICAR A(u + v) = Au + Av"
        )

        self.log(
            self.p_consola,
            "DATOS:",
            "paso"
        )

        self.log(
            self.p_consola,
            "\nA =",
            "variable"
        )

        self.formatear_matriz(
            A,
            self.p_consola
        )

        self.mostrar_vector(
            self.p_consola,
            u,
            "\nu ="
        )

        self.mostrar_vector(
            self.p_consola,
            v,
            "\nv ="
        )

        for paso in resultado["pasos"]:

            self.log(
                self.p_consola,
                "\n" + paso["titulo"],
                "paso"
            )

            for detalle in paso["detalles"]:

                self.log(
                    self.p_consola,
                    detalle,
                    "matriz"
                )

            self.mostrar_vector(
                self.p_consola,
                paso["resultado"],
                "\nResultado:"
            )

        self.log(
            self.p_consola,
            "\nCOMPARACIÓN FINAL:",
            "paso"
        )

        self.mostrar_vector(
            self.p_consola,
            resultado["A_u_mas_v"],
            "A(u + v) ="
        )

        self.mostrar_vector(
            self.p_consola,
            resultado["Au_mas_Av"],
            "\nAu + Av ="
        )

        self.log(
            self.p_consola,
            "\nCONCLUSIÓN:",
            "paso"
        )

        if resultado["cumple"]:

            self.log(
                self.p_consola,
                (
                    "Los dos resultados son iguales.\n"
                    "Por tanto:\n\n"
                    "A(u + v) = Au + Av\n\n"
                    "La propiedad se cumple."
                ),
                "exito"
            )

        else:

            self.log(
                self.p_consola,
                "Los resultados no son iguales.",
                "alerta"
            )

    def prop_escalar(self):

        self.p_consola.delete(
            "1.0",
            tk.END
        )

        try:

            A = self.leer_matriz(
                self.p_A
            )

            u = self.leer_vector(
                self.p_u
            )

            c = parsear_entrada(
                self.p_c.get()
            )

            resultado = (
                modulo_matrices
                .verificar_propiedad_escalar_detallada(
                    A,
                    u,
                    c
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            return

        self.titulo_resultado(
            self.p_consola,
            "VERIFICAR A(cu) = c(Au)"
        )

        self.log(
            self.p_consola,
            "DATOS:",
            "paso"
        )

        self.log(
            self.p_consola,
            "\nA =",
            "variable"
        )

        self.formatear_matriz(
            A,
            self.p_consola
        )

        self.mostrar_vector(
            self.p_consola,
            u,
            "\nu ="
        )

        self.log(
            self.p_consola,
            "\nc = " + a_fraccion_str(c),
            "variable"
        )

        for paso in resultado["pasos"]:

            self.log(
                self.p_consola,
                "\n" + paso["titulo"],
                "paso"
            )

            for detalle in paso["detalles"]:

                self.log(
                    self.p_consola,
                    detalle,
                    "matriz"
                )

            self.mostrar_vector(
                self.p_consola,
                paso["resultado"],
                "\nResultado:"
            )

        self.log(
            self.p_consola,
            "\nCOMPARACIÓN FINAL:",
            "paso"
        )

        self.mostrar_vector(
            self.p_consola,
            resultado["A_cu"],
            "A(cu) ="
        )

        self.mostrar_vector(
            self.p_consola,
            resultado["c_Au"],
            "\nc(Au) ="
        )

        self.log(
            self.p_consola,
            "\nCONCLUSIÓN:",
            "paso"
        )

        if resultado["cumple"]:

            self.log(
                self.p_consola,
                (
                    "Los dos resultados son iguales.\n"
                    "Por tanto:\n\n"
                    "A(cu) = c(Au)\n\n"
                    "La propiedad se cumple."
                ),
                "exito"
            )

        else:

            self.log(
                self.p_consola,
                "Los resultados no son iguales.",
                "alerta"
            )