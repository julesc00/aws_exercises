import numpy as np

# Crear dos matrices 3x3
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

# Multiplicación de matrices (Dot Product)
C = np.dot(A, B)
print("Matrix multiplication of A and B:\n", C)

# Multiplicación por elementos
D = A * B
print("\nElement-wise multiplication of A and B:\n", D)

# Suma de todos los elementos en D
sum_d = np.sum(D)
print("\nSum of all elements in the element-wise multiplied matrix:\n", sum_d)
