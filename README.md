# Suite Matemática - Calculadora de Matrices (UAM)

Calculadora de álgebra lineal con interfaz gráfica: eliminación gaussiana, RREF y producto matricial `Ax`.

## Requisitos

| Dependencia | Tipo | Instalación |
|-------------|------|-------------|
| Python 3.10+ | Sistema | [python.org](https://www.python.org/) o `brew install python@3.13` |
| tkinter | Sistema | Ver abajo según tu SO |
| ctypes | Estándar | Incluido con Python |

No hay paquetes de pip. El archivo `requirements.txt` documenta esto explícitamente.

### macOS (Homebrew)

```bash
brew install python@3.13 python-tk@3.13
```

> **Nota:** `tkinter` no se instala con `pip`. El comando `pip install tkinter` fallará siempre.

### Ubuntu / Debian

```bash
sudo apt install python3 python3-tk
```

### Windows

Instala Python desde [python.org](https://www.python.org/downloads/). Marca la opción **tcl/tk and IDLE** durante la instalación.

## Ejecución

```bash
python3 calculadora.py
```

## Entorno virtual (opcional)

Aunque no hay dependencias de pip, puedes usar un venv para aislar el proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
python calculadora.py
```
