from functools import wraps
import time

def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time.time()
        result = func(*args, **kargs)
        elapsed = time.time() - start
        print(func.__name__ + " rap time: " + str(elapsed) )
        return result
    return wrapper