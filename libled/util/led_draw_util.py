import math
import loop_util
import numpy as np
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

def get_scled_image(src , wscale, hscale):
    image = Image.fromarray(src, 'RGBA')
    nw = int(round(image.width * wscale))
    nh = int(round(image.height * hscale))
    scaled = image.resize((nw, nh))
    scaled = scaled.rotate(Image.ROTATE_90)
    return np.asarray(scaled)

def get_scled_rgb_image(src , wscale, hscale):
    image = Image.fromarray(src, 'RGB')
    nw = int(round(image.width * wscale))
    nh = int(round(image.height * hscale))
    scaled = image.resize((nw, nh))
    scaled = scaled.rotate(Image.ROTATE_90)
    return np.asarray(scaled)

def resize2(src, new_size, pos, fill):
    dx, dy, sx, sy, w, h = get_copy_positions(new_size, src.shape, pos)

    new_src = src
    pad = None
    if dx > sx:
        pad = np.array([[fill * h] * dx])
        new_src = np.vstack([pad[0,:,:,:], new_src])

    if new_size[0] > dx + w:
        pad = np.array([[fill * h] * (new_size[0] - dx - w ) ])
        new_src = np.vstack([new_src, pad[0,:,:,:]])

    if dy > sy:
        pad = np.array([[fill * dy] * new_size[0]])
        new_src = np.hstack([pad[0,:,:,:], new_src])

    if new_size[1] > dy + h:
        pad = np.array([[fill * (new_size[1] - dy - h)] * new_size[0]])
        new_src = np.hstack([new_src, pad[0,:,:,:]])

    if src.shape[0] > new_size[0]:
        new_src =  new_src[sx:sx+w, :]

    if src.shape[1] > new_size[1]:
        new_src =  new_src[:, sy:sy+h]

    return new_src


def get_copy_positions(src_size, dst_size, pos):
    dw = dst_size[0]
    dh = dst_size[1]
    sw = src_size[0]
    sh = src_size[1]

    w = min(dw, sw)
    h = min(dh, sh)

    dx = pos[0]
    dy = pos[1]
    sx = sy = 0

    if pos[0] < 0:
        dx = 0
        sx = -pos[0]

    if  pos[1] < 0:
        dy = 0
        sy = -pos[1]

    return (dx, dy, sx, sy, w, h)
