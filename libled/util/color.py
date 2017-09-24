class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = float(r)
        self.g = float(g)
        self.b = float(b)
        self.a = float(a)
        self.normalize()

    @staticmethod
    def rgbtapple_to_color(rgb, a=1.0):
        return Color(int(rgb[0]),
                    int(rgb[1]),
                    int(rgb[2]),
                    a)

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
