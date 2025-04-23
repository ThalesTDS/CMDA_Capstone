# BAD COMMENTS VERSION

def binary_search(arr, target):
    """
    This function does searching stuff.
    """
    left = 0  # start
    right = len(arr) - 1  # end

    while left <= right:
        mid = (left + right) // 2  # get average

        if arr[mid] == target:
            return mid  # success
        elif arr[mid] < target:
            left = mid + 1  # go up
        else:
            right = mid - 1  # go down

    return -1  # nothing found
