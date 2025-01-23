def delta(data, threshold=0.05):
    if len(data)< 15:
        return False
    last_npts = data[-15:]
    minV=min(last_15pts)
    maxV=max(last_15pts)
    return (maxV-minV)>threshold
