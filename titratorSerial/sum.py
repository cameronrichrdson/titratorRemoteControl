def delta(data):
    if len(data) < 15:
        return 0
    
    last15 = data[-15:]
    thresholdMet = []
    
    for i in range(len(last15)):
        if i ==0:
            continue
        else:
            diff = last15[i] - last15[i-1]
            thresholdMet.append(abs(diff)<=0.05)
    if all(thresholdMet):
        return 1
    else:
        return 0 
    
