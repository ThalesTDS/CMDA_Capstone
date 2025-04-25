def invert_matrix(matrix):
    """
    Inverts a given square matrix using Gauss-Jordan elimination.
    
    Parameters:
    -----------
    matrix : list of list of floats
        A square matrix to be inverted (n x n).
    
    Returns:
    --------
    list of list of floats
        Inverse of the input matrix.
        
    Raises:
    -------
    ValueError
        If the input matrix is not square or is singular (non-invertible).
    """
    n = len(matrix)
    
    # Check if the matrix is square
    if any(len(row) != n for row in matrix):
        raise ValueError("Matrix must be square (n x n)")
    
    # Create the augmented matrix [A | I]
    identity = [[float(i == j) for i in range(n)] for j in range(n)]
    aug_matrix = [row[:] + identity_row[:] for row, identity_row in zip(matrix, identity)]

    # Perform Gauss-Jordan elimination
    for i in range(n):
        # Search for maximum in this column
        max_row = max(range(i, n), key=lambda r: abs(aug_matrix[r][i]))
        if abs(aug_matrix[max_row][i]) < 1e-12:
            raise ValueError("Matrix is singular and cannot be inverted.")
        
        # Swap maximum row with current row
        aug_matrix[i], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[i]
        
        # Normalize pivot row
        pivot = aug_matrix[i][i]
        aug_matrix[i] = [x / pivot for x in aug_matrix[i]]
        
        # Eliminate column entries above and below the pivot
        for j in range(n):
            if j != i:
                factor = aug_matrix[j][i]
                aug_matrix[j] = [a - factor * b for a, b in zip(aug_matrix[j], aug_matrix[i])]
    
    # Extract the inverse matrix from the augmented matrix
    inverse = [row[n:] for row in aug_matrix]
    return inverse


# Example usage:
if __name__ == "__main__":
    A = [
        [4, 7],
        [2, 6]
    ]
    inv_A = invert_matrix(A)
    print("Inverse matrix:")
    for row in inv_A:
        print(row)
