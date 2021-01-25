#3
class BoundedMeta(type):

    def __new__(mcs, name, bases, attrs, **kwargs):
        mcs.max_instance_count = kwargs.get('max_instance_count', 1)
        mcs.instance_count = 0
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls):
        cls.instance_count += 1
        if cls.max_instance_count is None:
            return super().__call__()
        elif cls.instance_count > cls.max_instance_count:
            raise TypeError
        else:
            return super().__call__()


#4



#5
def smart_function():
    c = 1

    def new_smart_function():
        nonlocal c
        c += 1
        return c

    global smart_function
    smart_function = new_smart_function
    return c
