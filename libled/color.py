class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __int__(self):
        return Color.to_i(self.r ,self.g, self.b)

    @staticmethod
    def to_i(r, g, b):
        return r << 16 + g << 8 + b
