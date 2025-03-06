def delta(data):
    if len(data) < 5:
        return 0
    
    last5 = data[-5:]
    thresholdMet = []
    
    for i in range(len(last5)):
        if i ==0:
            continue
        else:
            diff = last5[i] - last5[i-1]
            thresholdMet.append(abs(diff)<=0.05)
    if all(thresholdMet):
        return 1
    else:
        return 0 
    
