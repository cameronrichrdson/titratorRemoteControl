def delta(data):
    if len(data) < 10:
        return 0
    
    last10 = data[-10:]
    thresholdMet = []
    
    for i in range(len(last10)):
        if i ==0:
            continue
        else:
            diff = last10[i] - last10[i-1]
            thresholdMet.append(abs(diff)<=0.05)
    if all(thresholdMet):
        print(1)
        print()
        print()
        return(0)
    else:
        return 0 
    

data = [0.1, 0.1,0.1,0.1,0.1,0.1,0.1,0.1, 0.1,0.1]
print(delta(data))    # Output: 1