import numpy as np

def jacobi_method(A, b, x0=None, tol=1e-10, max_iterations=1000):
    """
    Solves the linear system Ax = b using the Jacobi Iterative Method.

    Parameters:
    A (ndarray): Coefficient matrix (n x n).
    b (ndarray): Right-hand side vector (n).
    x0 (ndarray, optional): Initial guess vector (n). Defaults to zeros.
    tol (float, optional): Tolerance for the stopping criterion. Defaults to 1e-10.
    max_iterations (int, optional): Maximum number of iterations. Defaults to 1000.

    Returns:
    x (ndarray): Solution vector.
    iterations (int): Number of iterations performed.
    converged (bool): Whether the method converged within the tolerance.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Initial guess
    x = np.zeros_like(b) if x0 is None else np.array(x0, dtype=float)

    # Decompose A into D, L, and U (D: diagonal part of A)
    D = np.diag(A)
    R = A - np.diagflat(D)

    for iteration in range(max_iterations):
        # Compute the next iteration
        x_new = (b - np.dot(R, x)) / D

        # Compute the error (L2 norm of the difference)
        error = np.linalg.norm(x_new - x, ord=np.inf)

        # Check for convergence
        if error < tol:
            return x_new, iteration + 1, True

        x = x_new

    # Return the last result if convergence wasn't reached
    return x, max_iterations, False


# Example usage:
if __name__ == "__main__":
    A = np.array([[10, -1, 2, 0],
                  [-1, 11, -1, 3],
                  [2, -1, 10, -1],
                  [0, 3, -1, 8]])

    b = np.array([6, 25, -11, 15])
    x0 = np.zeros(len(b))

    solution, iterations, converged = jacobi_method(A, b, x0)

    print("Solution:", solution)
    print("Iterations:", iterations)
    print("Converged:", converged)
