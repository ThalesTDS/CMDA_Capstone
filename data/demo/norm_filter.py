def normalize_and_filter(data, threshold=0.5):
    """
    Input data, normalize it, then filter values below threshold.
    :param data: List of numerical values to normalize and filter.
    """
    max_val = max(data) if data else 1
    normalized = [x / max_val for x in data]
    filtered = []
    for i, val in enumerate(normalized):
        if val >= threshold:
            filtered.append((i, val))
    return filtered
