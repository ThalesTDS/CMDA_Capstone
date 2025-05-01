
def bubble_sort_iterative(collection: list[Any]) -> list[Any]:
    """
        Sorts list by swapping every element in the list. This
        is done via comparisions.
    """
    length = len(collection)
    for i in reversed(range(length)):
        swapped = False
        for j in range(i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break
    return collection 

def binary_search(arr, target):
    """
    Searches iteratively through an array for a value. Nothing happens when the
    value does not exist
    """
    left = 0 
    right = len(arr) - 1

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
        Given an array, this can calculate unknown values with in it using
        system solvers.
    """

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    
    for i in range(num_rows):
        
        max_row = i
        for k in range(i + 1, num_rows):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k

        
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        
        if abs(matrix[i][i]) < 1e-12:
            raise ValueError("No unique solution exists.")

        
        for k in range(i + 1, num_rows):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, num_cols):
                matrix[k][j] -= factor * matrix[i][j]

    
    solution = [0] * num_rows
    for i in range(num_rows - 1, -1, -1):
        sum_ax = sum(matrix[i][j] * solution[j] for j in range(i + 1, num_rows))
        solution[i] = (matrix[i][-1] - sum_ax) / matrix[i][i]

    return solution





