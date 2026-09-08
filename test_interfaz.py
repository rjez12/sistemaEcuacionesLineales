import unittest
import tkinter as tk

from InterfasCalculadora import InterfasCalculadora


class TestInterfazCalculadora(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = InterfasCalculadora(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def _llenar(self, entradas, filas):
        for i, fila in enumerate(filas):
            for j, valor in enumerate(fila):
                entradas[i][j].delete(0, tk.END)
                entradas[i][j].insert(0, valor)

    def test_pestaña1_acepta_fracciones_y_da_solucion_unica(self):
        self.app.m1_entry_m.delete(0, tk.END)
        self.app.m1_entry_n.delete(0, tk.END)
        self.app.m1_entry_m.insert(0, "2")
        self.app.m1_entry_n.insert(0, "2")
        self.app.m1_generar()
        self._llenar(self.app.m1_entradas, [["2", "0", "1"], ["0", "3", "1"]])
        self.app.m1_resolver()
        texto = self.app.m1_consola.get("1.0", tk.END)
        self.assertIn("RREF", texto)
        self.assertIn("1/2", texto)
        self.assertIn("1/3", texto)
        self.assertIn("Variables Básicas", texto)
        self.assertIn("Variables Libres:  Ninguna", texto)

    def test_pestaña1_solucion_general_con_libre_y_entrada_1_sobre_3(self):
        self.app.m1_entry_m.delete(0, tk.END)
        self.app.m1_entry_n.delete(0, tk.END)
        self.app.m1_entry_m.insert(0, "2")
        self.app.m1_entry_n.insert(0, "3")
        self.app.m1_generar()
        self._llenar(self.app.m1_entradas, [["1", "2", "3", "6"], ["2", "4", "8", "1/3"]])
        self.app.m1_resolver()
        texto = self.app.m1_consola.get("1.0", tk.END)
        self.assertNotIn("Celdas vacías", texto)
        self.assertIn("columnas pivote", texto.lower())
        self.assertIn("Variables Libres", texto)
        self.assertIn("libre", texto.lower())

    def test_pestaña1_sistema_inconsistente(self):
        self.app.m1_entry_m.delete(0, tk.END)
        self.app.m1_entry_n.delete(0, tk.END)
        self.app.m1_entry_m.insert(0, "2")
        self.app.m1_entry_n.insert(0, "2")
        self.app.m1_generar()
        self._llenar(self.app.m1_entradas, [["1", "1", "1"], ["2", "2", "3"]])
        self.app.m1_resolver()
        texto = self.app.m1_consola.get("1.0", tk.END)
        self.assertIn("Inconsistente", texto)

    def test_pestaña2_acepta_fraccion_en_celda(self):
        self.app.m2_entry_m.delete(0, tk.END)
        self.app.m2_entry_n.delete(0, tk.END)
        self.app.m2_entry_m.insert(0, "1")
        self.app.m2_entry_n.insert(0, "1")
        self.app.m2_generar()
        self._llenar(self.app.m2_entradas, [["1/2", "1/4"]])
        self.app.m2_resolver()
        texto = self.app.m2_consola.get("1.0", tk.END)
        self.assertIn("1/2", texto)
        self.assertIn("Solución Única", texto)

    def test_pestaña3_acepta_fraccion_en_celda(self):
        self.app.m3_entry_m.delete(0, tk.END)
        self.app.m3_entry_n.delete(0, tk.END)
        self.app.m3_entry_m.insert(0, "1")
        self.app.m3_entry_n.insert(0, "1")
        self.app.m3_generar()
        self.app.m3_entradas_A[0][0].delete(0, tk.END)
        self.app.m3_entradas_A[0][0].insert(0, "1/2")
        self.app.m3_entradas_x[0].delete(0, tk.END)
        self.app.m3_entradas_x[0].insert(0, "1/3")
        self.app.m3_calcular()
        texto = self.app.m3_consola.get("1.0", tk.END)
        self.assertIn("1/6", texto)


if __name__ == "__main__":
    unittest.main()
