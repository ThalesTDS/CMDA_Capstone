

def add(x: int, y: int):
    """
    Adds two integers and returns the sum
    
    """
    
    return x+y 

def binary_search(arr, target):
    """
    Searches for a target value in a sorted array that is in ascending order. Each iteration
    checks if the value is in the middle of the array. If the median value is less than
    our target value, we divide the array in halves, and choose the right half as our new array. Otherwise,
    we use the left half. If the target is not found, we return -1, otherwise the index of the target value is returned.
    """
    
    left = 0
    right = len(arr) - 1
    
    
    if not arr: return -1

    
    
    if not arr: return -1

    
    if not arr: return -1

    while left <= right:
        mid = (left + right) // 2  

        if arr[mid] == target:
            
            return mid
        elif arr[mid] < target:
            left = mid + 1  
        else:
            
            right = mid - 1

    return -1 

def gaussian_elimination(matrix):
    """
    Solves a system of linear equations using Gaussian elimination.

    Select the pivot element with the largest absolute value from the column. 
    Swap rows to move this element into the pivot position.
    For each row below the pivot, subtract a multiple of the pivot row to eliminate the entries below the pivot. 
    Iterate for each column and row
    
    Finally, use backsubsitution to iteratively solve from the  variables x_n to x_1. Then return the list of x variables
    
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





