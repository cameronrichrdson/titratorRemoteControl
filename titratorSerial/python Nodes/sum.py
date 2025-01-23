def delta(self, data):
    last15 = data[-15:]
    thresholdMet = []
    if len(data) < 15:
        return 0
    for i in range(len((last15))):
        if i ==0:
            continue
        else:
            diff = last15[i] - last15[i-1]
            thresholdMet.append(diff<=threshold)

    if False in thresholdMet:
        return 0
    else:
        return 1
