def profile(fn):
    def wrapped():
        start_time = default_timer()
        r = fn()
        elapsed = default_timer() - start_time
        print(elapsed)
        return r
    return wrapped


class timer:
    def __enter__(self):
        self.start_time = default_timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(default_timer() - self.start_time)