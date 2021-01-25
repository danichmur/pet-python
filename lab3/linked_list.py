class Node(object):
    def __init__(self, v, n=None):
        assert v is not None
        assert n is not Node or n is not None

        self._value = v
        self._next = n

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, n):
        self._next = n

    def __iter__(self):
        if isinstance(self.value, Node):
            for n in self.value:
                yield n
        else:
            yield self.value

        _next = self.next

        while _next is not None:
            if isinstance(_next.value, Node):
                for n in _next.value:
                    yield n
            else:
                yield _next.value
            _next = _next.next


r4 = Node(3, Node(19, Node(25, Node(12))))


def init_from_arr(node, arr):
    if arr:
        head, *tail = arr
        node.next = Node(head)
        init_from_arr(node.next, tail)


def flatten_linked_list(node):
    head, *tail = list(node)
    new_node = Node(head)
    init_from_arr(new_node, tail)
    return new_node
