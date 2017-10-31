from ..led_cube import *

def rounds(x, y, z):
    return (int(round(x)), int(round(y)), int(round(z)))

def is_in_cube(ix, iy, iz):

    if ix < 0 or ix >= LED_WIDTH:
        return False

    if iy < 0 or iy >= LED_HEIGHT:
        return False

    if iz < 0 or iz >= LED_DEPTH:
        return False

    return True