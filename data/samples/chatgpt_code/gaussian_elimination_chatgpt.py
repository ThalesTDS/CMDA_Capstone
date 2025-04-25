def gaussian_elimination(matrix):
    """
    Solves a system of linear equations using Gaussian elimination.

    Parameters:
    matrix (list of list of floats): The augmented matrix of the system,
                                      where each row represents an equation and the last column is the constants.

    Returns:
    list of floats: The solution to the system, if one exists.
                    Raises ValueError if the system has no unique solution.
    """

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Forward Elimination
    for i in range(num_rows):
        # Find the pivot for column i
        max_row = i
        for k in range(i + 1, num_rows):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k

        # Swap the max row with the current row
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Check for zero pivot (no unique solution)
        if abs(matrix[i][i]) < 1e-12:
            raise ValueError("No unique solution exists.")

        # Eliminate entries below the pivot
        for k in range(i + 1, num_rows):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, num_cols):
                matrix[k][j] -= factor * matrix[i][j]

    # Back Substitution
    solution = [0] * num_rows
    for i in range(num_rows - 1, -1, -1):
        sum_ax = sum(matrix[i][j] * solution[j] for j in range(i + 1, num_rows))
        solution[i] = (matrix[i][-1] - sum_ax) / matrix[i][i]

    return solution

# Example usage:
if __name__ == "__main__":
    # System: 2x + y - z = 8
    #         -3x - y + 2z = -11
    #         -2x + y + 2z = -3
    augmented_matrix = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]

    try:
        solution = gaussian_elimination(augmented_matrix)
        print("Solution:", solution)
    except ValueError as e:
        print("Error:", e)
