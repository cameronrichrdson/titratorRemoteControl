def store(data, current_results):
    """
    Updates the array based on the input data and returns the updated array.

    Args:
        data: A single value (float/int) or an iterable (list/tuple).
        current_results: The current array (passed from LabVIEW).

    Returns:
        The updated array.
    """
    # Ensure current_results is a list
    if not isinstance(current_results, list):
        current_results = []

    # Add new data to the array
    if isinstance(data, (list, tuple)):
        current_results.extend(data)  # Add all elements if iterable
    else:
        current_results.append(data)  # Add single value

    return current_results
