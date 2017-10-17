import math
import loop_util
from ..led_cube import *
from ..util.color import Color
from PIL import Image, ImageDraw

class LedDirection(object):
    DIRECTION_FRONT = 1
    DIRECTION_UP = 2
    DIRECTION_SIDE = 3

def circle(canvas, x, y, z, color, r, direction = LedDirection.DIRECTION_FRONT):
    dth = (2.0 * math.pi)/(4 * r*math.pi)
    for th in loop_util.frange(0, 2.0 * math.pi, dth):
        c1=r * math.cos(th)
        c2=r * math.sin(th)

        ambigous1 = abs(c1 - round(c1))
        ambigous2 = abs(c2 - round(c2))
        ambigous = (ambigous1 + ambigous2) # / 2

        xadd = yadd = zadd = 0
       
        if direction == LedDirection.DIRECTION_FRONT:
            xadd = c1
            yadd = c2
        elif direction == LedDirection.DIRECTION_UP:
            xadd = c1
            zadd = c2
        elif direction == LedDirection.DIRECTION_SIDE:
            yadd = c1
            zadd = c2
        else:
            pass

        canvas.set_led(x + xadd, y + yadd, z + zadd,
                    Color(color.r, color.g, color.b, color.a * ambigous))

def circle2(canvas, x, y, z, color, r, direction = LedDirection.DIRECTION_FRONT):
    image = Image.new('RGBA', (LED_WIDTH, LED_HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.ellipse((int(x-r), int(y-r), int(x+r), int(y+r)), outline=(color.to_rgba255()))

    for x in range(LED_WIDTH):
        for y in range(LED_HEIGHT):
            rgba = image.getpixel((x,y))

            canvas.set_led(x, y, z, Color.rgbatapple255_to_color(rgba))
