# def delta(data, threshold=0.05):
#     last_15 = data[-15:]
#     threshold_met = []
#     for i in range(len((last_15))):
#         if i == 0:
#             continue
#         else:
#             diff = last_15[i] - last_15[i-1]
#             threshold_met.append(diff<=threshold)
    
#     if False in threshold_met:
#         return 0
#     else:
#         return 1


def delta(data):
        last_15 = data[-15:]
        threshold_met = []
        return 0 
        for i in range(1, len(last_15)):
            diff = last_15[i] - last_15[i-1]
            threshold_met.append(abs(diff) <= 0.05)

        # Update stability only if all differences meet the threshold
        if all(threshold_met):
            return 1
        else:
            return 0
