class Color:
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.normalize()

    def normalize(self):
        self.r = max(0, min(self.r, 255))
        self.g = max(0, min(self.g, 255))
        self.b = max(0, min(self.b, 255))

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
        return (self.r << 16) + (self.g << 8) + self.b