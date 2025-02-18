def calculate_average(numbers: List[float]) -> float:
    """
    Calculate the average of a list of numbers.

    @param numbers: A list of floating-point numbers.
    @return: The calculated average value.
    """
    if not numbers:
        return 0.0  # Avoid division by zero
    
    total_sum = sum(numbers)  # Sum all numbers
    count = len(numbers)  # Count how many numbers are in the list
    average = total_sum / count  # Compute the average
    
    return average
