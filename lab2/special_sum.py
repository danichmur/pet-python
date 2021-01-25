from functools import reduce

def calculate_special_sum(n):
    return reduce(lambda x, y: x + y * (y - 1) ** 2, range(n + 1))