def delta_recursion(data, state=0):
    if len(data) < 10:
        return 0  # Not enough data, no threshold check

    if state == 1:
        return 0  # Return 0 after returning 1 in the previous call

    # Check the threshold
    last10 = data[-10:]
    thresholdMet = [abs(last10[i] - last10[i - 1]) <= 0.05 for i in range(1, len(last10))]

    if all(thresholdMet):
        print(1)  # Print 1 to indicate threshold met
        return delta_recursion(data, state=1)  # Recursive call with updated state

    return 0  # Return 0 if threshold not met



