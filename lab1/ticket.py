def sum_eq(n):
    j, i = 0, 0
    s = str(n)
    for k in range(len(s)):
        if k % 2 == 0:
            j += int(s[k])
        else:
            i += int(s[k])
    return j == i

def get_nearest_lucky_ticket(n):
    c = n
    k = 0
    while not sum_eq(c):
        k += 1
        c_next, c_prev = c + k, c - k
        if sum_eq(c_next):
            return c_next
        else:
            if sum_eq(c_prev):
                return c_prev
       
    return current_ticket