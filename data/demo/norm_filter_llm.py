def normalize_and_filter(data, threshold=0.5):
    """
    Normalize a list of numerical values and filter out values below a threshold.

    Parameters:
        data (list of float): The input list of numerical values.
        threshold (float, optional): The minimum normalized value to retain. Defaults to 0.5.

    Returns:
        list of tuple: A list of (index, normalized_value) tuples where the normalized
                       value is greater than or equal to the threshold.

    Notes:
        - If `data` is empty, normalization is done with a max value of 1 to avoid division by zero.
        - Normalization is done by dividing each element by the maximum value in `data`.
    """
    max_val = max(data) if data else 1
    normalized = [x / max_val for x in data]
    filtered = []
    for i, val in enumerate(normalized):
        if val >= threshold:
            filtered.append((i, val))
    return filtered
