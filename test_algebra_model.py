import unittest
from fractions import Fraction

from AlgebraModel import (
    AlgebraModel,
    a_fraccion_str,
    a_subindice,
    parsear_entrada,
)


class TestParsearEntrada(unittest.TestCase):
    def test_acepta_fraccion_escrita(self):
        self.assertEqual(parsear_entrada("1/3"), Fraction(1, 3))

    def test_acepta_decimal_y_coma(self):
        self.assertEqual(parsear_entrada("0.5"), Fraction(1, 2))
        self.assertEqual(parsear_entrada("1,5"), Fraction(3, 2))

    def test_acepta_enteros_y_negativos(self):
        self.assertEqual(parsear_entrada(" 2 "), Fraction(2))
        self.assertEqual(parsear_entrada("-3/4"), Fraction(-3, 4))

    def test_rechaza_vacio_o_basura(self):
        with self.assertRaises(ValueError):
            parsear_entrada("")
        with self.assertRaises(ValueError):
            parsear_entrada("abc")


class TestPivotesYRref(unittest.TestCase):
    def test_gauss_devuelve_posiciones_de_pivote(self):
        Ab = [
            [1, 2, 3, 6],
            [2, 4, 8, 14],
        ]
        Ab_esc, pasos, pivotes = AlgebraModel.eliminacion_gaussiana(2, 3, Ab)
        self.assertEqual(pivotes, [(0, 0), (1, 2)])
        self.assertTrue(pasos)

    def test_completar_rref_normaliza_y_limpia_arriba(self):
        Ab_esc, _, pivotes_esc = AlgebraModel.eliminacion_gaussiana(
            2, 3,
            [[1, 2, 3, 6], [2, 4, 8, 14]],
        )
        Ab_rref, pivotes, pasos = AlgebraModel.completar_rref(2, 3, Ab_esc)
        self.assertEqual(pivotes, [(0, 0), (1, 2)])
        self.assertEqual(Ab_rref[0], [Fraction(1), Fraction(2), Fraction(0), Fraction(3)])
        self.assertEqual(Ab_rref[1], [Fraction(0), Fraction(0), Fraction(1), Fraction(1)])
        self.assertTrue(pasos)


class TestSolucionGeneral(unittest.TestCase):
    def test_solucion_unica_con_subindices_y_fracciones(self):
        Ab = [[Fraction(1), Fraction(0), Fraction(1, 2)], [Fraction(0), Fraction(1), Fraction(1, 3)]]
        pivotes = [(0, 0), (1, 1)]
        basicas, libres, lineas = AlgebraModel.construir_solucion_general(2, 2, Ab, pivotes)
        self.assertEqual(basicas, [0, 1])
        self.assertEqual(libres, [])
        texto = "\n".join(lineas)
        self.assertIn(f"x{a_subindice(1)} = {a_fraccion_str(Fraction(1, 2))}", texto)
        self.assertIn(f"x{a_subindice(2)} = {a_fraccion_str(Fraction(1, 3))}", texto)

    def test_solucion_parametrica_nombra_libres(self):
        Ab = [
            [Fraction(1), Fraction(2), Fraction(0), Fraction(3)],
            [Fraction(0), Fraction(0), Fraction(1), Fraction(1)],
        ]
        pivotes = [(0, 0), (1, 2)]
        basicas, libres, lineas = AlgebraModel.construir_solucion_general(2, 3, Ab, pivotes)
        self.assertEqual(basicas, [0, 2])
        self.assertEqual(libres, [1])
        texto = "\n".join(lineas)
        self.assertIn(f"x{a_subindice(2)}", texto)
        self.assertIn("libre", texto)
        self.assertIn(f"x{a_subindice(1)} =", texto)
        self.assertIn(f"x{a_subindice(3)} = 1", texto)


if __name__ == "__main__":
    unittest.main()
