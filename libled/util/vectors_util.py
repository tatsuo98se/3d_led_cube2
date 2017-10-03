# coding: UTF-8
from ..led_cube import *
from ..util.color import Color

# 回心するオブジェクト表示オブジェクト用ユーティリティ
# オブジェクトが中心から外に向かいます

def get_power(ix, N):
    fade = N / 5
    if ix < fade:
        return ix * 255 / fade
    elif ix < (N - fade):
        return 255
    else:
        return (N - ix) * 256 / fade

def max3(a, b, c):
    ab = b if a < b else a
    return c if ab < c else ab

def concentric(canvas, ix, N, proc):
    cx = LED_WIDTH / 2
    cy = LED_HEIGHT / 2
    cz = LED_DEPTH / 2

    power = get_power(ix, N)
    for x in range(LED_WIDTH):
        for y in range(LED_HEIGHT):
            for z in range(LED_DEPTH):
                d = proc(x - cx, y - cy, z - cz, ix * 1.0 / N)
                col0 = int(round(ix - d) % 64)
                col = (col0 % 7 + 1) if (col0 % 6) == 0 else 0
                r = power if (col & 1) else 0
                g = power if (col & 2) else 0
                b = power if (col & 4) else 0
                # rgb = (r << 16) + (g << 8) + b
                # if rgb != 0:
                canvas.set_led(x, y, z, Color(r, g, b))




