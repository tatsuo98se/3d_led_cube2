def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step