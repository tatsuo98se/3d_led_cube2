# coding: UTF-8
from ..led_cube import *
from ..util.color import Color
import math
import random

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


def skewed(dx0, dy, dz0, t):
    T = 4
    s = math.sin(t * math.pi * T)
    c = math.cos(t * math.pi * T)
    dx = (dx0 * c + dz0 * s) * 0.5
    dz = (-dx0 * s + dz0 * c) * 2
    return dx, dz


def sphere_face():

    while True:
        pos = Xyz_t(random.uniform(-1, 1),
                    random.uniform(-1, 1), random.uniform(-1, 1))
        d2 = pos.x * pos.x + pos.y * pos.y + pos.z * pos.z
        if 0.1 < d2 and d2 < 1:
            d = 0.5
            return Xyz_t(pos.x * d, pos.y * d + 0.1, pos.z * d)


def can_show(p):
    return 0 <= p.x and p.x < LED_WIDTH \
        and 0 <= p.y and p.y < LED_HEIGHT \
        and 0 <= p.z and p.z < LED_DEPTH


class Xyz_t:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __add__(self, other):
        if isinstance(other, Xyz_t):
            return Xyz_t(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Xyz_t(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if isinstance(other, Xyz_t):
            return Xyz_t(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Xyz_t(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if isinstance(other, Xyz_t):
            return Xyz_t(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Xyz_t(self.x * other, self.y * other, self.z * other)


class Xyzc_t:

    def __init__(self, p=Xyz_t(), color=0):
        self.p = p
        self.color = color


def Xyz(x, y, z):
    return Xyz_t(x, y, z)
