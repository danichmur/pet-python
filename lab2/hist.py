def distribute(a, k):
    l = [0] * k
    min_a = min(a)
    max_a = max(a)
    h = (max_a - min_a) / k
    
    for e in a:
        if e == max_a:
            position = k - 1
        else:                   
            position = int((e - min_a) // h)
        l[position] += 1
        
    return l