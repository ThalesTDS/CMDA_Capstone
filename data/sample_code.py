# GOOD COMMENTS VERSION

def binary_search(arr, target):
    """
    Perform binary search to locate the index of a target value in a sorted list.

    Parameters:
        arr (list of int): A list sorted in ascending order.
        target (int): The value to search for.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    # Initialize the left boundary of the search range
    left = 0
    right = len(arr) - 1  # Initialize the right boundary of the search range
    # Comment not tied to code
    # Blocking comment
    "tesing comment"
    # More comments which should not be picked up
    "Another comment, should be picked up"
    if not arr: return -1

    "Another comment, should not be picked up"

    if not arr: return -1

    "pick me"
    if not arr: return -1



    while left <= right:
        mid = (left + right) // 2  # Find the middle index between left and right

        if arr[mid] == target:
            # Target found at the middle index
            return mid
        elif arr[mid] < target:
            left = mid + 1  # Narrow search to the right half
        else:
            # Narrow search to the left half
            right = mid - 1

    return -1  # Target not found in the list

def binary_search2(arr, target):
    """
    Perform binary search to locate the index of a target value in a sorted list.

    Parameters:
        arr (list of int): A list sorted in ascending order.
        target (int): The value to search for.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    left = 0  # Initialize the left boundary of the search range
    right = len(arr) - 1  # Initialize the right boundary of the search range

    while left <= right:
        mid = (left + right) // 2  # Find the middle index between left and right

        if arr[mid] == target:
            return mid  # Target found at the middle index
        elif arr[mid] < target:
            left = mid + 1  # Narrow search to the right half
        else:
            right = mid - 1  # Narrow search to the left half

    return -1  # Target not found in the list




def binary_search3(arr, target):
    """
    Perform binary search to locate the index of a target value in a sorted list.

    Parameters:
        arr (list of int): A list sorted in ascending order.
        target (int): The value to search for.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    left = 0  # Initialize the left boundary of the search range
    right = len(arr) - 1  # Initialize the right boundary of the search range

    while left <= right:
        mid = (left + right) // 2  # Find the middle index between left and right

        if arr[mid] == target:
            return mid  # Target found at the middle index
        elif arr[mid] < target:
            left = mid + 1  # Narrow search to the right half
        else:
            right = mid - 1  # Narrow search to the left half

    return -1  # Target not found in the list

# GOOD COMMENTS VERSION

def binary_search(arr, target):
    """
    Perform binary search to locate the index of a target value in a sorted list.

    Parameters:
        arr (list of int): A list sorted in ascending order.
        target (int): The value to search for.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    left = 0  # Initialize the left boundary of the search range
    right = len(arr) - 1  # Initialize the right boundary of the search range

    while left <= right:
        mid = (left + right) // 2  # Find the middle index between left and right

        if arr[mid] == target:
            return mid  # Target found at the middle index
        elif arr[mid] < target:
            left = mid + 1  # Narrow search to the right half
        else:
            right = mid - 1  # Narrow search to the left half

    return -1  # Target not found in the list

