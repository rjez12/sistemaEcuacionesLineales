import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

from AlgebraModel import AlgebraModel, a_subindice, a_fraccion_str

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class InterfasCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Suite Matemática - UAM")
        self.root.geometry("1100x850")

        self.colors = {
            "bg_main": "#1e1e2e", "bg_panel": "#252535", "bg_entry": "#313244",
            "fg_text": "#cdd6f4", "accent": "#89b4fa", "accent_hover": "#74c7ec",
            "vector_b": "#312635", "b_text": "#f38ba8", "success": "#a6e3a1",
            "warning": "#f9e2af", "error": "#f38ba8", "comment": "#a6adc8"
        }

        self.root.configure(bg=self.colors["bg_main"])

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.colors["bg_main"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["bg_panel"], foreground=self.colors["fg_text"],
                        font=("Segoe UI", 11, "bold"), padding=[20, 10], borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", self.colors["accent"])], foreground=[("selected", "#11111b")])
        style.configure("TFrame", background=self.colors["bg_main"])
        style.configure("TLabel", background=self.colors["bg_main"], foreground=self.colors["fg_text"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=self.colors["accent"])

        ttk.Label(root, text="Suite de Álgebra Lineal", style="Header.TLabel").pack(pady=(20, 10))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))

        # Pestañas
        self.tab_gauss = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_gauss, text=" 1. Eliminación Principal (Ax=b) ")
        self.construir_modulo_gauss(self.tab_gauss)

        self.tab_rref = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rref, text=" 2. Reducción RREF (Gauss-Jordan) ")
        self.construir_modulo_rref(self.tab_rref)

        self.tab_combinacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_combinacion, text=" 3. Ecuación Matricial (Ax) ")
        self.construir_modulo_combinacion(self.tab_combinacion)

    # --- COMPONENTES AUXILIARES DE UI ---
    def crear_entry_suave(self, parent, is_vector=False):
        bg_color = self.colors["vector_b"] if is_vector else self.colors["bg_entry"]
        fg_color = self.colors["b_text"] if is_vector else self.colors["fg_text"]
        return tk.Entry(parent, width=6, justify="center", font=("Consolas", 12),
                        bg=bg_color, fg=fg_color, relief="flat", insertbackground=self.colors["fg_text"],
                        highlightthickness=1, highlightbackground=self.colors["bg_panel"], highlightcolor=self.colors["accent"])

    def crear_boton_suave(self, parent, texto, comando):
        btn = tk.Button(parent, text=texto, command=comando, bg=self.colors["accent"], fg="#11111b",
                        font=("Segoe UI", 11, "bold"), relief="flat", activebackground=self.colors["accent_hover"],
                        activeforeground="#11111b", padx=20, pady=6, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg=self.colors["accent_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.colors["accent"]))
        return btn

    def configurar_consola(self, frame_padre):
        frame_consola = tk.Frame(frame_padre, bg=self.colors["bg_panel"], highlightthickness=1, highlightbackground=self.colors["comment"])
        frame_consola.pack(fill=tk.BOTH, expand=True, padx=30, pady=(15, 30))
        scroll = ttk.Scrollbar(frame_consola)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        consola = tk.Text(frame_consola, yscrollcommand=scroll.set, font=("Consolas", 11),
                          bg=self.colors["bg_panel"], fg=self.colors["fg_text"], padx=20, pady=20, relief="flat")
        consola.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=consola.yview)

        consola.tag_config("titulo", font=("Consolas", 11, "bold"), foreground=self.colors["accent"])
        consola.tag_config("explicacion", foreground=self.colors["comment"], font=("Consolas", 10, "italic"))
        consola.tag_config("alerta", foreground=self.colors["error"], font=("Consolas", 11, "bold"))
        consola.tag_config("exito", foreground=self.colors["success"], font=("Consolas", 11, "bold"))
        consola.tag_config("matriz", foreground=self.colors["fg_text"], font=("Consolas", 12))
        consola.tag_config("variable", foreground=self.colors["warning"], font=("Consolas", 11, "bold"))
        return consola

    def log(self, consola, mensaje, tipo="normal"):
        consola.insert(tk.END, str(mensaje) + "\n", tipo)
        consola.see(tk.END)

    def formatear_matriz(self, matriz, consola, pivotes=None):
        if pivotes is None: pivotes = []
        for i, fila in enumerate(matriz):
            fila_str = ""
            for j, val in enumerate(fila):
                valor_str = a_fraccion_str(val)
                if j == len(fila) - 1:
                    fila_str += f" │ {valor_str:^8}"
                else:
                    if (i, j) in pivotes:
                        fila_str += f"[{valor_str:^6}]"
                    else:
                        fila_str += f"{valor_str:^8}"
            self.log(consola, f"  [ {fila_str} ]", "matriz")

    # --- MÓDULO 1: ELIMINACIÓN GAUSSIANA ---
    def construir_modulo_gauss(self, parent):
        ttk.Label(parent, text="Método de Eliminación por Filas y Sustitución Hacia Atrás", font=("Segoe UI", 12), foreground=self.colors["comment"]).pack(pady=10)

        frame_dim = ttk.Frame(parent)
        frame_dim.pack()
        ttk.Label(frame_dim, text="Filas (m):").grid(row=0, column=0, padx=5)
        self.m1_entry_m = self.crear_entry_suave(frame_dim)
        self.m1_entry_m.grid(row=0, column=1, padx=5)
        ttk.Label(frame_dim, text="Columnas (n):").grid(row=0, column=2, padx=15)
        self.m1_entry_n = self.crear_entry_suave(frame_dim)
        self.m1_entry_n.grid(row=0, column=3, padx=5)
        self.crear_boton_suave(frame_dim, "Generar Matriz", self.m1_generar).grid(row=0, column=4, padx=25)

        self.m1_frame_matriz = tk.Frame(parent, bg=self.colors["bg_main"], pady=15)
        self.m1_frame_matriz.pack()
        self.m1_entradas = []

        self.m1_frame_boton = tk.Frame(parent, bg=self.colors["bg_main"])
        self.m1_frame_boton.pack()
        self.m1_btn_resolver = self.crear_boton_suave(self.m1_frame_boton, "Resolver Sistema", self.m1_resolver)

        self.m1_consola = self.configurar_consola(parent)

    def m1_generar(self):
        try:
            self.m1_m, self.m1_n = int(self.m1_entry_m.get()), int(self.m1_entry_n.get())
        except ValueError:
            messagebox.showwarning("Error", "Ingresa números enteros.")
            return

        for w in self.m1_frame_matriz.winfo_children(): w.destroy()
        self.m1_entradas = []

        for j in range(self.m1_n):
            tk.Label(self.m1_frame_matriz, text=f"x{a_subindice(j+1)}", font=("Segoe UI", 11, "bold"), bg=self.colors["bg_main"], fg=self.colors["warning"]).grid(row=0, column=j)
        tk.Label(self.m1_frame_matriz, text="b", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["error"]).grid(row=0, column=self.m1_n+1)

        for i in range(self.m1_m):
            fila = []
            for j in range(self.m1_n):
                ent = self.crear_entry_suave(self.m1_frame_matriz)
                ent.grid(row=i+1, column=j, padx=4, pady=4)
                fila.append(ent)
            tk.Label(self.m1_frame_matriz, text="=", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["comment"]).grid(row=i+1, column=self.m1_n)
            ent_b = self.crear_entry_suave(self.m1_frame_matriz, is_vector=True)
            ent_b.grid(row=i+1, column=self.m1_n+1, padx=4, pady=4)
            fila.append(ent_b)
            self.m1_entradas.append(fila)

        self.m1_btn_resolver.pack(pady=10)
        self.m1_consola.delete('1.0', tk.END)

    def m1_resolver(self):
        self.m1_consola.delete('1.0', tk.END)
        Ab = []
        try:
            for i in range(self.m1_m):
                Ab.append([float(self.m1_entradas[i][j].get()) for j in range(self.m1_n + 1)])
        except ValueError:
            messagebox.showerror("Error", "Celdas inválidas.")
            return

        matriz_original = [fila[:] for fila in Ab]

        self.log(self.m1_consola, "=== INICIANDO REDUCCIÓN POR ELIMINACIÓN ===", "titulo")
        self.log(self.m1_consola, "\n[>] Matriz Aumentada Inicial:", "variable")
        self.formatear_matriz(Ab, self.m1_consola)

        Ab_escalonada, pasos = AlgebraModel.eliminacion_gaussiana(self.m1_m, self.m1_n, Ab)

        for tipo, msg, *resto in pasos:
            if tipo == "info":
                self.log(self.m1_consola, f"\n    [i] {msg}", "explicacion")
            elif tipo == "pivoteo":
                self.log(self.m1_consola, f"\n[🔄] {msg}:", "variable")
                self.formatear_matriz(resto[0], self.m1_consola)
            elif tipo == "operacion":
                self.log(self.m1_consola, f"\n[⬇] Operación: {msg}", "variable")
                self.formatear_matriz(resto[0], self.m1_consola)

        self.log(self.m1_consola, "\n[✔] MATRIZ ESCALONADA FINALIZADA:", "exito")
        self.formatear_matriz(Ab_escalonada, self.m1_consola)

        self.log(self.m1_consola, "\n" + "━"*70, "comment")
        self.log(self.m1_consola, "DIAGNÓSTICO DEL SISTEMA MATEMÁTICO:", "titulo")

        inconsistente = False
        for i in range(self.m1_m):
            if all(Ab_escalonada[i][j] == 0 for j in range(self.m1_n)) and Ab_escalonada[i][self.m1_n] != 0:
                inconsistente = True
                self.log(self.m1_consola, f"\n[!] ERROR EN FILA {i+1}: 0 = {a_fraccion_str(Ab_escalonada[i][self.m1_n])}", "alerta")
                break

        if inconsistente:
            self.log(self.m1_consola, "-> ESTADO: Sistema Inconsistente (Sin Solución).", "alerta")
            return

        rango = sum(1 for i in range(self.m1_m) if not all(Ab_escalonada[i][j] == 0 for j in range(self.m1_n)))

        if rango < self.m1_n:
            self.log(self.m1_consola, f"-> ESTADO: Sistema Consistente Indeterminado ({self.m1_n - rango} variables libres).", "variable")
            return

        self.log(self.m1_consola, "-> ESTADO: Sistema Consistente Determinado (Solución Única).", "exito")

        x = AlgebraModel.sustitucion_hacia_atras(self.m1_m, self.m1_n, Ab_escalonada)

        self.log(self.m1_consola, "\n[>] SUSTITUCIÓN HACIA ATRÁS (Vector Solución):", "titulo")
        for i in range(self.m1_n):
            self.log(self.m1_consola, f"    x{a_subindice(i+1)} = {a_fraccion_str(x[i])}", "variable")

        self.log(self.m1_consola, "\n[>] VERIFICACIÓN AUTOMÁTICA:", "titulo")
        verificacion_ok = True
        for i in range(self.m1_m):
            suma_ver = sum(matriz_original[i][j] * float(x[j]) for j in range(self.m1_n))
            val_esp = matriz_original[i][self.m1_n]
            diferencia = abs(suma_ver - val_esp)

            estado = "[OK]" if diferencia < 1e-5 else "[FALLO]"
            color = "success" if diferencia < 1e-5 else "error"
            self.log(self.m1_consola, f"    {estado} Ec. {i+1} -> Calc: {round(suma_ver, 4)} | Esp: {round(val_esp, 4)}", color)
            if diferencia > 1e-5: verificacion_ok = False

        if verificacion_ok:
            self.log(self.m1_consola, "\n[✔] VERIFICACIÓN APROBADA: La solución preserva la igualdad.", "exito")

    # --- MÓDULO 2: RREF AVANZADA (GAUSS-JORDAN) ---
    def construir_modulo_rref(self, parent):
        ttk.Label(parent, text="Forma Escalonada Reducida, Detección de Pivotes y Variables Básicas/Libres", font=("Segoe UI", 12), foreground=self.colors["comment"]).pack(pady=10)

        frame_dim = ttk.Frame(parent)
        frame_dim.pack()
        ttk.Label(frame_dim, text="Filas (m):").grid(row=0, column=0, padx=5)
        self.m2_entry_m = self.crear_entry_suave(frame_dim)
        self.m2_entry_m.grid(row=0, column=1, padx=5)
        ttk.Label(frame_dim, text="Columnas (n):").grid(row=0, column=2, padx=15)
        self.m2_entry_n = self.crear_entry_suave(frame_dim)
        self.m2_entry_n.grid(row=0, column=3, padx=5)
        self.crear_boton_suave(frame_dim, "Generar Matriz", self.m2_generar).grid(row=0, column=4, padx=25)

        self.m2_frame_matriz = tk.Frame(parent, bg=self.colors["bg_main"], pady=15)
        self.m2_frame_matriz.pack()
        self.m2_entradas = []

        self.m2_frame_boton = tk.Frame(parent, bg=self.colors["bg_main"])
        self.m2_frame_boton.pack()
        self.m2_btn_resolver = self.crear_boton_suave(self.m2_frame_boton, "Reducir a RREF", self.m2_resolver)

        self.m2_consola = self.configurar_consola(parent)

    def m2_generar(self):
        try:
            self.m2_m, self.m2_n = int(self.m2_entry_m.get()), int(self.m2_entry_n.get())
        except ValueError:
            return

        for w in self.m2_frame_matriz.winfo_children(): w.destroy()
        self.m2_entradas = []
        for j in range(self.m2_n): 
            tk.Label(self.m2_frame_matriz, text=f"x{a_subindice(j+1)}", font=("Segoe UI", 11, "bold"), bg=self.colors["bg_main"], fg=self.colors["warning"]).grid(row=0, column=j)
        tk.Label(self.m2_frame_matriz, text="b", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["error"]).grid(row=0, column=self.m2_n+1)

        for i in range(self.m2_m):
            fila = []
            for j in range(self.m2_n):
                ent = self.crear_entry_suave(self.m2_frame_matriz)
                ent.grid(row=i+1, column=j, padx=4, pady=4)
                fila.append(ent)
            tk.Label(self.m2_frame_matriz, text="=", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["comment"]).grid(row=i+1, column=self.m2_n)
            ent_b = self.crear_entry_suave(self.m2_frame_matriz, is_vector=True)
            ent_b.grid(row=i+1, column=self.m2_n+1, padx=4, pady=4)
            fila.append(ent_b)
            self.m2_entradas.append(fila)
        self.m2_btn_resolver.pack(pady=10)
        self.m2_consola.delete('1.0', tk.END)

    def m2_resolver(self):
        self.m2_consola.delete('1.0', tk.END)
        Ab = []
        try:
            for i in range(self.m2_m): 
                Ab.append([float(self.m2_entradas[i][j].get()) for j in range(self.m2_n + 1)])
        except ValueError:
            messagebox.showerror("Error", "Celdas inválidas.")
            return

        self.log(self.m2_consola, "=== PROCESAMIENTO: GAUSS-JORDAN (SELECCIÓN DE PIVOTE ÓPTIMO) ===", "titulo")
        
        Ab_rref, pivotes_pos, pasos, es_inconsistente = AlgebraModel.gauss_jordan_rref(self.m2_m, self.m2_n, Ab)

        for tipo, msg, mat in pasos:
            if tipo == "pivoteo":
                self.log(self.m2_consola, f"\n[🔄] {msg}:", "variable")
            elif tipo == "operacion":
                self.log(self.m2_consola, f"\n[⬇] Operación: {msg}", "explicacion")
            self.formatear_matriz(mat, self.m2_consola)

        # 1. Matriz RREF Final
        self.log(self.m2_consola, "\n" + "━"*70, "comment")
        self.log(self.m2_consola, "1. FORMA ESCALONADA REDUCIDA FINAL (RREF):", "exito")
        self.formatear_matriz(Ab_rref, self.m2_consola, pivotes_pos)

        if es_inconsistente:
            self.log(self.m2_consola, "\n" + "━"*70, "comment")
            self.log(self.m2_consola, "DIAGNÓSTICO DEL SISTEMA:", "alerta")
            self.log(self.m2_consola, "-> ESTADO: Sistema Inconsistente (Sin Solución). Existe una fila [ 0 ... 0 │ c ] con c ≠ 0.", "alerta")
            return

        # 2. Detección de Pivotes
        self.log(self.m2_consola, "\n" + "━"*70, "comment")
        cols_pivote_str = ", ".join([str(p[1] + 1) for p in pivotes_pos]) if pivotes_pos else "Ninguna"
        self.log(self.m2_consola, f"2. DETECCIÓN DE PIVOTES:\n   Las columnas pivote son: {cols_pivote_str}", "titulo")

        # 3. Clasificación de Variables
        vars_basicas, vars_libres, lineas_solucion = AlgebraModel.construir_solucion_general(self.m2_m, self.m2_n, Ab_rref, pivotes_pos)
        basicas_str = ", ".join([f"x{a_subindice(j+1)}" for j in vars_basicas]) if vars_basicas else "Ninguna"
        libres_str = ", ".join([f"x{a_subindice(j+1)}" for j in vars_libres]) if vars_libres else "Ninguna"

        self.log(self.m2_consola, "\n3. CLASIFICACIÓN DE VARIABLES:", "titulo")
        self.log(self.m2_consola, f"   • Variables Básicas: {basicas_str}", "exito")
        self.log(self.m2_consola, f"   • Variables Libres:  {libres_str}", "variable")

        # 4. Solución Final
        self.log(self.m2_consola, "\n4. ESTRUCTURA DE LA SOLUCIÓN FINAL:", "titulo")
        for linea in lineas_solucion:
            self.log(self.m2_consola, f"   {linea}", "variable" if "Paramétrica" in linea or "x" in linea else "exito")

    # --- MÓDULO 3: ECUACIÓN MATRICIAL (Ax) ---
    def construir_modulo_combinacion(self, parent):
        ttk.Label(parent, text="Producto Ax y Combinaciones Lineales (Regla Fila-Vector)", font=("Segoe UI", 12), foreground=self.colors["comment"]).pack(pady=10)

        frame_dim = ttk.Frame(parent)
        frame_dim.pack()
        ttk.Label(frame_dim, text="Filas (m):").grid(row=0, column=0, padx=5)
        self.m3_entry_m = self.crear_entry_suave(frame_dim)
        self.m3_entry_m.grid(row=0, column=1, padx=5)
        ttk.Label(frame_dim, text="Columnas (n):").grid(row=0, column=2, padx=15)
        self.m3_entry_n = self.crear_entry_suave(frame_dim)
        self.m3_entry_n.grid(row=0, column=3, padx=5)
        self.crear_boton_suave(frame_dim, "Generar Entorno", self.m3_generar).grid(row=0, column=4, padx=25)

        self.m3_frame_datos = tk.Frame(parent, bg=self.colors["bg_main"], pady=15)
        self.m3_frame_datos.pack()
        self.m3_frame_A = tk.Frame(self.m3_frame_datos, bg=self.colors["bg_main"])
        self.m3_frame_A.grid(row=0, column=0, padx=20)
        ttk.Label(self.m3_frame_datos, text="*", font=("Consolas", 20, "bold"), background=self.colors["bg_main"], foreground=self.colors["comment"]).grid(row=0, column=1)
        self.m3_frame_x = tk.Frame(self.m3_frame_datos, bg=self.colors["bg_main"])
        self.m3_frame_x.grid(row=0, column=2, padx=20)

        self.m3_entradas_A = []
        self.m3_entradas_x = []

        self.m3_frame_boton = tk.Frame(parent, bg=self.colors["bg_main"])
        self.m3_frame_boton.pack()
        self.m3_btn_resolver = self.crear_boton_suave(self.m3_frame_boton, "Calcular Producto Ax", self.m3_calcular)

        self.m3_consola = self.configurar_consola(parent)

    def m3_generar(self):
        try:
            self.m3_m, self.m3_n = int(self.m3_entry_m.get()), int(self.m3_entry_n.get())
        except ValueError:
            return

        for w in self.m3_frame_A.winfo_children(): w.destroy()
        for w in self.m3_frame_x.winfo_children(): w.destroy()
        self.m3_entradas_A, self.m3_entradas_x = [], []

        tk.Label(self.m3_frame_A, text="Matriz A", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["accent"]).grid(row=0, column=0, columnspan=self.m3_n, pady=5)
        for i in range(self.m3_m):
            fila = []
            for j in range(self.m3_n):
                ent = self.crear_entry_suave(self.m3_frame_A)
                ent.grid(row=i+1, column=j, padx=2, pady=2)
                fila.append(ent)
            self.m3_entradas_A.append(fila)

        tk.Label(self.m3_frame_x, text="Vector x", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["warning"]).grid(row=0, column=0, pady=5)
        for j in range(self.m3_n):
            ent = self.crear_entry_suave(self.m3_frame_x, is_vector=True)
            ent.grid(row=j+1, column=0, padx=2, pady=2)
            self.m3_entradas_x.append(ent)

        self.m3_btn_resolver.pack(pady=10)

    def m3_calcular(self):
        self.m3_consola.delete('1.0', tk.END)
        A, x = [], []
        try:
            for i in range(self.m3_m): 
                A.append([float(self.m3_entradas_A[i][j].get()) for j in range(self.m3_n)])
            x = [float(self.m3_entradas_x[j].get()) for j in range(self.m3_n)]
        except ValueError:
            return

        self.log(self.m3_consola, "=== COMBINACIÓN LINEAL ===", "titulo")
        comb_str = ""
        for j in range(self.m3_n):
            peso = a_fraccion_str(x[j])
            columna = [a_fraccion_str(A[i][j]) for i in range(self.m3_m)]
            signo = " + " if j > 0 and x[j] >= 0 else " - " if j > 0 else ""
            val_peso = a_fraccion_str(abs(x[j])) if j > 0 else peso
            comb_str += f"{signo}{val_peso} * {columna}"
        self.log(self.m3_consola, f"Estructura: {comb_str}\n", "variable")

        self.log(self.m3_consola, "=== REGLA FILA-VECTOR ===", "titulo")
        
        b, detalles = AlgebraModel.producto_ax(self.m3_m, self.m3_n, A, x)
        
        for det in detalles:
            self.log(self.m3_consola, det, "matriz")

        self.log(self.m3_consola, "\n[✔] VECTOR RESULTANTE (b):", "exito")
        for val in b: 
            self.log(self.m3_consola, f"  [ {a_fraccion_str(val):^8} ]", "error")