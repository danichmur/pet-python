def get_min_max(s1, s2):
    if (len(s1) < len(s2)):
        return s1, s2
    else:
        return s2, s1

def merge(s1, s2):
    min_s, max_s = get_min_max(s1, s2)
    max_i = iter(max_s)
    create_type = type(s1)
    res = create_type()
    
    e2 = next(max_i, None)
    for e1 in min_s:
        while e2 != None and e2 < e1:
            res += create_type([e2])
            e2 = next(max_i, None)
        res += create_type([e1])
    
    while e2 != None:
        res += create_type([e2])
        e2 = next(max_i, None)
        
    return res