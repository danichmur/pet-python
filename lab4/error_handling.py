import functools
import sys
import time

from contextlib import contextmanager

def no_trace_except_handler(t, value, _):
    print(': '.join([str(t.__name__), str(value)]))
        
#1
def handle_error(re_raise=True, log_traceback=True, exc_type=Exception, tries=1, delay=0, backoff=1):
    assert tries > 0
    
    @contextmanager
    def except_handler(exc_handler):
        sys.excepthook = exc_handler
        yield
        sys.excepthook = sys.__excepthook__


    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(tries):
                try:
                    if log_traceback:
                        result = f(*args, **kwargs)
                    else:
                        with except_handler(no_trace_except_handler):
                            result = f(*args, **kwargs)
                except exc_type:
                    if attempt == tries - 1 and re_raise:
                        raise
                    current_delay *= backoff
                    time.sleep(current_delay)
                else:
                    return result
        return wrapper
    return decorator


#2
class handle_error_context(object):
    def __init__(self, re_raise=True, log_traceback=True, exc_type=Exception):
        self.re_raise = re_raise
        self.log_traceback = log_traceback
        self.exc_type = exc_type

    def __enter__(self):
        return self

    def is_handled(self, t):
        if isinstance(self.exc_type, tuple):
            return t in self.exc_type
        else:
            return self.exc_type == t

    def __exit__(self, t, value, traceback):
        if t:
            if self.re_raise:
                if self.is_handled(t):
                    if not self.log_traceback:
                        sys.excepthook = no_trace_except_handler
                    return False
                return False
            return True
        return True