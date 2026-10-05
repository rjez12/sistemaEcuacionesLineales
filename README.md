# Suite Matemática: calculadora de álgebra lineal

Aplicación de escritorio en Python para explorar y resolver sistemas lineales y operaciones matriciales. Es un proyecto académico de equipo; la descripción del repositorio indica cuatro integrantes.

## Funciones

- Resuelve sistemas Ax=b mediante eliminación gaussiana con pivoteo parcial.
- Reduce matrices a forma escalonada reducida (RREF) y muestra las operaciones realizadas.
- Distingue sistemas inconsistentes, soluciones únicas y soluciones con variables libres.
- Trabaja con fracciones exactas para evitar errores de redondeo en los cálculos.
- Incluye un módulo para operaciones con ecuaciones matriciales Ax.

## Requisitos

- Python 3.10 o posterior.
- Tkinter, incluido en muchas instalaciones de Python. En Linux puede requerir el paquete del sistema `python3-tk`; en macOS, la versión de Python debe incluir Tcl/Tk.
- No requiere paquetes de terceros instalados con pip.

## Ejecutar

Desde la carpeta del proyecto:

```bash
python calculadora.py
```

En algunos sistemas el comando puede llamarse `python3`.

## Estructura principal

| Archivo | Responsabilidad |
| --- | --- |
| `calculadora.py` | Punto de entrada de la aplicación. |
| `InterfasCalculadora.py` | Interfaz Tkinter y sus tres módulos de trabajo. |
| `AlgebraModel.py` | Conversión a fracciones y operaciones de álgebra lineal. |
| `test_algebra_model.py` | Pruebas automatizadas del modelo y del análisis de sistemas. |
| `test_interfaz.py` | Pruebas de interacción de la interfaz; requiere que Tkinter pueda crear una ventana. |

Para ejecutar las pruebas existentes desde la raíz:

```bash
python -m unittest test_algebra_model.py test_interfaz.py
```

## Créditos y alcance

El repositorio presenta el proyecto como un trabajo grupal de cuatro integrantes. La aplicación está pensada como apoyo académico; no reemplaza la verificación manual de ejercicios ni un sistema de cálculo simbólico de propósito general.
