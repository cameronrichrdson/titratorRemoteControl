def delta():
    threshold_met_flag = False
    return_state = None  # Tracks if we should return 1, then 0

    def inner(data):
        nonlocal threshold_met_flag, return_state

        if return_state == 1:
            return_state = 0  # After returning 1, set up to return 0 next
            return 1
        elif return_state == 0:
            return_state = None  # Reset state after returning 0
            return 0

        if len(data) < 10:
            return 0

        last10 = data[-10:]
        thresholdMet = [abs(last10[i] - last10[i-1]) <= 0.05 for i in range(1, len(last10))]

        if all(thresholdMet):
            return_state = 1  # Start the sequence to return 1 then 0
            threshold_met_flag = True

        return 0

    return inner

delta_function = delta()

# Example usage:
  # Returns 0
print(delta_function([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))  # Returns 1
