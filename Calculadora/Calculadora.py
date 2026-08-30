# =============================================================================
# UNIVERSIDAD AMERICANA (UAM)
# Facultad de Ingeniería y Arquitectura (FIA)
# Asignatura: Álgebra Lineal (MTM0120)
# Proyecto Integrador: Suite de Álgebra Lineal (Dark Mode Edition)
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

# Habilitar nitidez (DPI Awareness) para pantallas modernas
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass 

class CalculadoraMultitema:
    def __init__(self, root):
        self.root = root
        self.root.title("Suite Matemática - UAM")
        self.root.geometry("1000x850")
        
        # --- PALETA DE COLORES (Dark Theme Moderno) ---
        self.colors = {
            "bg_main": "#1e1e2e",       # Fondo principal oscuro
            "bg_panel": "#252535",      # Fondo de paneles y pestañas
            "bg_entry": "#313244",      # Fondo de las celdas de entrada
            "fg_text": "#cdd6f4",       # Texto principal claro
            "accent": "#89b4fa",        # Azul acento (Botones y Títulos)
            "accent_hover": "#74c7ec",  # Azul claro para hover
            "vector_b": "#312635",      # Fondo rojizo oscuro para el vector b
            "b_text": "#f38ba8",        # Texto rojo pastel para vector b
            "success": "#a6e3a1",       # Verde pastel
            "warning": "#f9e2af",       # Amarillo pastel
            "error": "#f38ba8",         # Rojo pastel
            "comment": "#6c7086"        # Gris para explicaciones
        }
        
        self.root.configure(bg=self.colors["bg_main"])
        
        # --- CONFIGURACIÓN DE ESTILOS TTK FLAT ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Eliminar bordes 3D de las pestañas
        style.configure("TNotebook", background=self.colors["bg_main"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["bg_panel"], foreground=self.colors["fg_text"], 
                        font=("Segoe UI", 11, "bold"), padding=[20, 10], borderwidth=0)
        style.map("TNotebook.Tab", 
                  background=[("selected", self.colors["accent"])], 
                  foreground=[("selected", "#11111b")])
        
        # Estilo global de etiquetas y frames
        style.configure("TFrame", background=self.colors["bg_main"])
        style.configure("TLabel", background=self.colors["bg_main"], foreground=self.colors["fg_text"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=self.colors["accent"])
        
        # --- ENCABEZADO GENERAL ---
        ttk.Label(root, text="Suite de Álgebra Lineal", style="Header.TLabel").pack(pady=(20, 10))
        
        # --- SISTEMA DE PESTAÑAS ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        # Pestaña 1
        self.tab_gauss = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_gauss, text=" Sistemas Ax = b ")
        self.construir_modulo_gauss(self.tab_gauss)
        
        # Pestaña 2
        self.tab_operaciones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_operaciones, text=" Multiplicación de Matrices ")
        self.construir_construccion(self.tab_operaciones, "Suma y Multiplicación")

        # Pestaña 3
        self.tab_determinantes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_determinantes, text=" Determinantes e Inversa ")
        self.construir_construccion(self.tab_determinantes, "Determinantes y Regla de Cramer")

    # =========================================================================
    # COMPONENTES UI PERSONALIZADOS (SMOOTHNESS)
    # =========================================================================
    def crear_entry_suave(self, parent, is_vector_b=False):
        """Crea un campo de texto sin bordes 3D, con colores flat."""
        bg_color = self.colors["vector_b"] if is_vector_b else self.colors["bg_entry"]
        fg_color = self.colors["b_text"] if is_vector_b else self.colors["fg_text"]
        
        ent = tk.Entry(parent, width=7, justify="center", font=("Consolas", 12),
                       bg=bg_color, fg=fg_color, relief="flat", insertbackground=self.colors["fg_text"],
                       highlightthickness=1, highlightbackground=self.colors["bg_panel"], highlightcolor=self.colors["accent"])
        return ent

    def crear_boton_suave(self, parent, texto, comando):
        """Crea un botón con diseño moderno y efecto hover reactivo."""
        btn = tk.Button(parent, text=texto, command=comando, 
                        bg=self.colors["accent"], fg="#11111b", font=("Segoe UI", 11, "bold"), 
                        relief="flat", activebackground=self.colors["accent_hover"], 
                        activeforeground="#11111b", padx=25, pady=8, cursor="hand2")
        # Efecto Hover
        btn.bind("<Enter>", lambda e: btn.config(bg=self.colors["accent_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.colors["accent"]))
        return btn

    # =========================================================================
    # MÓDULO 1: SISTEMAS DE ECUACIONES
    # =========================================================================
    def construir_modulo_gauss(self, parent):
        ttk.Label(parent, text="Eliminación por Filas (Reducción a Forma Escalonada)", font=("Segoe UI", 12), foreground=self.colors["comment"]).pack(pady=15)

        # Controles m y n
        frame_dim = ttk.Frame(parent)
        frame_dim.pack()
        
        ttk.Label(frame_dim, text="Ecuaciones (m):").grid(row=0, column=0, padx=5)
        self.entry_m = self.crear_entry_suave(frame_dim)
        self.entry_m.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_dim, text="Variables (n):").grid(row=0, column=2, padx=15)
        self.entry_n = self.crear_entry_suave(frame_dim)
        self.entry_n.grid(row=0, column=3, padx=5)
        
        btn_generar = self.crear_boton_suave(frame_dim, "Generar Entradas", self.generar_cuadricula)
        btn_generar.grid(row=0, column=4, padx=25)
        
        # Área dinámica de la matriz
        self.frame_matriz = tk.Frame(parent, bg=self.colors["bg_main"], pady=20)
        self.frame_matriz.pack()
        self.entradas_matriz = []
        
        # Contenedor del botón resolver
        self.frame_boton = tk.Frame(parent, bg=self.colors["bg_main"])
        self.frame_boton.pack()
        self.btn_resolver = self.crear_boton_suave(self.frame_boton, "Ejecutar Algoritmo", self.resolver_sistema)
        
        # Consola de Resultados (Terminal Style)
        frame_consola = tk.Frame(parent, bg=self.colors["bg_panel"], highlightthickness=1, highlightbackground=self.colors["comment"])
        frame_consola.pack(fill=tk.BOTH, expand=True, padx=30, pady=(15, 30))
        
        scroll = ttk.Scrollbar(frame_consola)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.consola = tk.Text(frame_consola, yscrollcommand=scroll.set, 
                               font=("Consolas", 11), bg=self.colors["bg_panel"], fg=self.colors["fg_text"], 
                               padx=20, pady=20, relief="flat", insertbackground=self.colors["fg_text"])
        self.consola.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.consola.yview)
        
        # Configuración de Sintaxis de Color para la Terminal
        self.consola.tag_config("titulo", font=("Consolas", 11, "bold"), foreground=self.colors["accent"])
        self.consola.tag_config("explicacion", foreground=self.colors["comment"], font=("Consolas", 10, "italic"))
        self.consola.tag_config("alerta", foreground=self.colors["error"], font=("Consolas", 11, "bold"))
        self.consola.tag_config("exito", foreground=self.colors["success"], font=("Consolas", 11, "bold"))
        self.consola.tag_config("matriz", foreground=self.colors["fg_text"], font=("Consolas", 12))
        self.consola.tag_config("variable", foreground=self.colors["warning"], font=("Consolas", 11, "bold"))

    def log(self, mensaje, tipo="normal"):
        self.consola.insert(tk.END, str(mensaje) + "\n", tipo)
        self.consola.see(tk.END)

    def formatear_matriz(self, matriz):
        for fila in matriz:
            fila_str = ""
            for i, x in enumerate(fila):
                valor = 0.0 if abs(x) < 1e-10 else round(x, 4)
                # Separador visual antes del término b
                if i == len(fila) - 1:
                    fila_str += f" │ {valor:^8g}"
                else:
                    fila_str += f"{valor:^8g}" 
            self.log(f"  [ {fila_str} ]", "matriz")

    def generar_cuadricula(self):
        try:
            self.m = int(self.entry_m.get())
            self.n = int(self.entry_n.get())
        except ValueError:
            messagebox.showwarning("Dato Inválido", "Por favor, ingresa números enteros para m y n.")
            return

        for widget in self.frame_matriz.winfo_children():
            widget.destroy()
            
        self.entradas_matriz = []
        
        for j in range(self.n):
            tk.Label(self.frame_matriz, text=f"x{j+1}", font=("Segoe UI", 11, "bold"), bg=self.colors["bg_main"], fg=self.colors["warning"]).grid(row=0, column=j)
        tk.Label(self.frame_matriz, text="b", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["error"]).grid(row=0, column=self.n+1)

        for i in range(self.m):
            fila_entradas = []
            for j in range(self.n):
                ent = self.crear_entry_suave(self.frame_matriz)
                ent.grid(row=i+1, column=j, padx=4, pady=4)
                fila_entradas.append(ent)
            
            tk.Label(self.frame_matriz, text="=", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_main"], fg=self.colors["comment"]).grid(row=i+1, column=self.n)
            
            ent_b = self.crear_entry_suave(self.frame_matriz, is_vector_b=True)
            ent_b.grid(row=i+1, column=self.n+1, padx=4, pady=4)
            fila_entradas.append(ent_b)
            self.entradas_matriz.append(fila_entradas)

        self.btn_resolver.pack(pady=15)
        self.consola.delete('1.0', tk.END)
        self.log(">> Interfaz generada. Esperando parámetros de entrada...", "explicacion")

    def resolver_sistema(self):
        self.consola.delete('1.0', tk.END)
        Ab = []
        
        try:
            for i in range(self.m):
                fila_valores = []
                for j in range(self.n + 1):
                    fila_valores.append(float(self.entradas_matriz[i][j].get()))
                Ab.append(fila_valores)
        except ValueError:
            messagebox.showerror("Error de Sintaxis", "Hay celdas vacías o con texto. Ingresa solo valores numéricos.")
            return

        matriz_original = [fila[:] for fila in Ab]

        self.log("=== INICIANDO REDUCCIÓN POR ELIMINACIÓN ===", "titulo")
        self.log("\n[>] Matriz Aumentada Inicial:", "variable")
        self.formatear_matriz(Ab)
        
        fila_pivote = 0
        for j in range(self.n):
            if fila_pivote >= self.m: break
                
            max_fila = fila_pivote
            for i in range(fila_pivote + 1, self.m):
                if abs(Ab[i][j]) > abs(Ab[max_fila][j]):
                    max_fila = i
                    
            if abs(Ab[max_fila][j]) < 1e-10:
                self.log(f"\n    [i] Nota: La columna x{j+1} carece de pivote válido (ceros detectados). Saltando variable.", "explicacion")
                continue
                
            if max_fila != fila_pivote:
                Ab[fila_pivote], Ab[max_fila] = Ab[max_fila], Ab[fila_pivote]
                self.log(f"\n[🔄] Pivoteo Parcial Aplicado:", "variable")
                self.log(f"    Se intercambió Fila {fila_pivote+1} con Fila {max_fila+1} para asegurar el mayor pivote posible y evitar errores de redondeo.", "explicacion")
                self.formatear_matriz(Ab)
                
            hubo_cambio = False
            for i in range(fila_pivote + 1, self.m):
                factor = Ab[i][j] / Ab[fila_pivote][j]
                if abs(factor) > 1e-10:
                    for k in range(j, self.n + 1):
                        Ab[i][k] -= factor * Ab[fila_pivote][k]
                    hubo_cambio = True
                    self.log(f"\n[⬇] Operación de Fila (F{i+1} = F{i+1} - ({round(factor,3)}) * F{fila_pivote+1}):", "variable")
                    
            if hubo_cambio:
                self.log("    Estado actual de la matriz tras anular elementos de la columna:", "explicacion")
                self.formatear_matriz(Ab)
                
            fila_pivote += 1

        self.log("\n[✔] MATRIZ ESCALONADA FINALIZADA:", "exito")
        self.formatear_matriz(Ab)
        
        # CLASIFICACIÓN DIAGNÓSTICA
        self.log("\n" + "━"*70, "comment")
        self.log("DIAGNÓSTICO DEL SISTEMA MATEMÁTICO:", "titulo")
        
        inconsistente = False
        for i in range(self.m):
            todo_ceros = all(abs(Ab[i][j]) < 1e-10 for j in range(self.n))
            termino_independiente_no_cero = abs(Ab[i][self.n]) > 1e-10
            if todo_ceros and termino_independiente_no_cero:
                inconsistente = True
                b_val = round(Ab[i][self.n], 2)
                self.log(f"\n[!] ERROR DE LÓGICA ENCONTRADO EN LA FILA {i+1}:", "alerta")
                self.log(f"    Ecuación resultante: 0 = {b_val}", "error")
                break
                
        if inconsistente:
            self.log("\n-> ESTADO: Sistema Inconsistente (Sin Solución).", "alerta")
            self.log("-> INTERPRETACIÓN GEOMÉTRICA: Las ecuaciones representan rectas o planos paralelos que nunca se interceptan en un punto común.", "explicacion")
            return 
            
        rango = sum(1 for i in range(self.m) if not all(abs(Ab[i][j]) < 1e-10 for j in range(self.n)))
                
        if rango < self.n:
            self.log(f"\n-> ESTADO: Sistema Consistente Indeterminado ({self.n - rango} variables libres).", "variable")
            self.log("-> INTERPRETACIÓN GEOMÉTRICA: Existen infinitas soluciones. El sistema describe intersecciones continuas, como planos que se cruzan formando una línea infinita.", "explicacion")
            return
            
        self.log("\n-> ESTADO: Sistema Consistente Determinado (Solución Única).", "exito")
        self.log("-> INTERPRETACIÓN GEOMÉTRICA: Todas las ecuaciones convergen exactamente en un único punto o coordenada espacial.", "explicacion")
        
        # SUSTITUCIÓN HACIA ATRÁS
        x = [0 for _ in range(self.n)]
        for i in range(self.n - 1, -1, -1):
            suma = sum(Ab[i][j] * x[j] for j in range(i + 1, self.n))
            x[i] = (Ab[i][self.n] - suma) / Ab[i][i]
            
        self.log("\n[>] SUSTITUCIÓN HACIA ATRÁS (Vector Solución):", "titulo")
        for i in range(self.n):
            valor_final = 0.0 if abs(x[i]) < 1e-10 else x[i]
            self.log(f"    x{i+1} = {round(valor_final, 4)}", "variable")
            
        # COMPROBACIÓN
        self.log("\n[>] PRUEBA DE ESFUERZO (Verificación Automática):", "titulo")
        verificacion_ok = True
        for i in range(self.m):
            suma_verificacion = sum(matriz_original[i][j] * x[j] for j in range(self.n))
            valor_esperado = matriz_original[i][self.n]
            diferencia = abs(suma_verificacion - valor_esperado)
            
            estado = "[OK]" if diferencia < 1e-5 else "[FALLO]"
            color = "success" if diferencia < 1e-5 else "error"
            self.log(f"    {estado} Ec. {i+1} -> Calculado: {round(suma_verificacion, 4)} | Esperado: {round(valor_esperado, 4)}", color)
            if diferencia > 1e-5: verificacion_ok = False
                
        if verificacion_ok:
            self.log("\n[✔] VERIFICACIÓN APROBADA: La solución encontrada preserva la igualdad en todo el sistema matriz.", "exito")

    # =========================================================================
    # MÓDULOS DE RELLENO (ESTRUCTURA MANTENIDA)
    # =========================================================================
    def construir_construccion(self, parent, titulo):
        ttk.Label(parent, text=f"Módulo: {titulo}", font=("Segoe UI", 16, "bold"), foreground=self.colors["fg_text"]).pack(pady=40)
        ttk.Label(parent, text="[!] Infraestructura lista. Interfaz gráfica en desarrollo para próximas iteraciones.", foreground=self.colors["comment"], font=("Consolas", 12)).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraMultitema(root)
    root.mainloop()