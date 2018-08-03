import numpy as np

class Color:
    def __init__(self, r=0, g=0, b=0, a=1.0):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.a = float(a)
        self.normalize()

    @staticmethod
    def int_to_rgbtapple255(rgb):
        return (((rgb&0xff0000) >> 16 ),
                      ((rgb&0x00ff00) >> 8 ) ,
                      (rgb&0x0000ff) )

    @staticmethod
    def rgbtapple255_to_int(rgb):
        return (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]

    @staticmethod
    def int_to_color(rgb):
        return Color( ((rgb&0xff0000) >> 16 ) / 255.0,
                      ((rgb&0x00ff00) >> 8 ) / 255.0,
                      (rgb&0x0000ff) / 255.0)

    @staticmethod
    def rgbtapple_to_color(rgb, a=1.0):
        return Color(rgb[0],
                    rgb[1],
                    rgb[2],
                    a)

    @staticmethod
    def rgbatapple_to_color(rgba):
        return Color(rgba[0],
                    rgba[1],
                    rgba[2],
                    rgba[3])
    @staticmethod
    def rgbtapple255_to_color(rgb, a=1.0):
        return Color(rgb[0] / 255.0,
                    rgb[1] / 255.0,
                    rgb[2] / 255.0,
                    a)

    @staticmethod
    def rgbatapple255_to_color(rgba):
        return Color(rgba[0] / 255.0,
                    rgba[1] / 255.0,
                    rgba[2] / 255.0,
                    rgba[3])
    @staticmethod
    def object_to_color(color):
        if  isinstance(color, Color):
            return color
        elif  isinstance(color, int):
            return Color.int_to_color(color)
        elif  isinstance(color, float):
            return Color.int_to_color(int(color))
        elif isinstance(color, tuple):
            if len(color) == 3:
                return Color.rgbtapple_to_color(color)
            else:
                return Color.rgbatapple_to_color(color)
        elif isinstance(color, np.ndarray):
            if len(color) == 3:
                return Color.rgbtapple255_to_color(color)
            else:
                return Color.rgbatapple255_to_color(color)
        else:
            print("Unknown Type:" + str(type(color)))
            raise TypeError

    def normalize(self):
        self.r = max(0.0, min(self.r, 1.0))
        self.g = max(0.0, min(self.g, 1.0))
        self.b = max(0.0, min(self.b, 1.0))
        self.a = max(0.0, min(self.a, 1.0))

    def __mul__(self, other):
        return Color(
            self.r * other,
            self.g * other,
            self.b * other)

    def __div__(self, other):
        return Color(
            self.r / other,
            self.g / other,
            self.b / other)

    def __or__(self, other):
        return Color.rgbtapple255_to_color(
            (
            int(self.r * 255) | int(other.r * 255),
            int(self.g * 255) | int(other.g* 255),
            int(self.b * 255) | int(other.b* 255))
            )

    def __and__(self, other):
        return Color.rgbtapple255_to_color(
            (
            int(self.r * 255) & int(other.r * 255),
            int(self.g * 255) & int(other.g* 255),
            int(self.b * 255) & int(other.b* 255))
            )


    def __sub__(self, other):
        if(isinstance(other, Color)):
            return Color(
                self.r - other.r,
                self.g - other.g,
                self.b - other.b)
        else:
            return Color(
                self.r - other,
                self.g - other,
                self.b - other)

    def __int__(self):
        return (int(round(self.r * self.a * 255)) << 16) + \
               (int(round(self.g * self.a * 255)) << 8) + \
               int(round(self.b * self.a * 255))

    def is_black(self):
        if self.a == 0:
            return True
        return self.r == 0.0 and self.g == 0.0 and self.b == 0.0

    def to_rgba255(self):
        return (int(round(self.r * 255)),
                int(round(self.g * 255)),
                int(round(self.b * 255)),
                int(round(self.a * 255)))

    def to_rgb255(self):
        return (int(round(self.r * 255)),
                int(round(self.g * 255)),
                int(round(self.b * 255)))
