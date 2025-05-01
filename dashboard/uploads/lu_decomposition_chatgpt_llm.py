import numpy as np

def lu_decomposition(A):
    """
    Performs LU Decomposition of a square matrix A using Doolittle's method.
    
    Parameters:
    A (numpy.ndarray): The square matrix to decompose (n x n)
    
    Returns:
    L (numpy.ndarray): Lower triangular matrix (with 1s on the diagonal)
    U (numpy.ndarray): Upper triangular matrix

    Raises:
    ValueError: If the matrix is not square or has a zero pivot (non-invertible)
    """

    # Ensure A is a square matrix
    n, m = A.shape
    if n != m:
        raise ValueError("Matrix must be square for LU decomposition.")

    # Create zero matrices for L and U
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    # Perform Doolittle's LU Decomposition
    for i in range(n):
        # Compute U[i][j]
        for j in range(i, n):
            sum_u = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_u

        # Compute L[j][i]
        for j in range(i, n):
            if i == j:
                L[i][i] = 1  # Diagonal as 1
            else:
                sum_l = sum(L[j][k] * U[k][i] for k in range(i))
                if U[i][i] == 0:
                    raise ValueError("Zero pivot encountered. LU decomposition not possible without pivoting.")
                L[j][i] = (A[j][i] - sum_l) / U[i][i]

    return L, U


# Example usage:
if __name__ == "__main__":
    A = np.array([[4, 3],
                  [6, 3]], dtype=float)

    L, U = lu_decomposition(A)

    print("Matrix A:")
    print(A)
    print("\nLower Triangular Matrix L:")
    print(L)
    print("\nUpper Triangular Matrix U:")
    print(U)

    # Verify the decomposition
    print("\nReconstructed A (L @ U):")
    print(np.dot(L, U))
