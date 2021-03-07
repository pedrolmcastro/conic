import real

class Point:
    """
    A 2D space point representation.

    Attributes:
        x (float): abscissa coordinate.
        y (float): ordinate coordinate.
    """
    def __init__(self, x, y):
        self.x = real.parse(x)
        self.y = real.parse(y)

    @classmethod
    def frominput(cls):
        x = real.get('x: ')
        y = real.get('y: ')
        return cls(x, y)

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'
