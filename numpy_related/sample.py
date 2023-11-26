# Manera estándar de importar NumPy:
import numpy as np

"""
Crear un arreglo 2-D, establecer cada segundo elemento en
algunas columnas y fijar max por fila::
"""

x = np.arange(15, dtype=np.int64).reshape(3, 5)
x[1:, ::2] = -99
x
# array([[  0,   1,   2,   3,   4],
#        [-99,   6, -99,   8, -99],
#        [-99,  11, -99,  13, -99]])

x.max(axis=1)
# array([ 4,  8, 13])

# Generar números aleatorios normalmente distribuidos:
rng = np.random.default_rng()
samples = rng.normal(size=2500)
