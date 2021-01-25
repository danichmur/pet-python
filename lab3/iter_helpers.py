def transpose(iterable):
    return zip(*iterable)


def scalar_product(a, b):
    try:
        return sum(int(i)*int(j) for i, j in zip(a, b))
    except ValueError:
        return None