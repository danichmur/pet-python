def compress(a):
    d = {}
    for e in a:
        d[e] = d.get(e, 0) + 1
    return d.items()