import real

class Point:
    """
    A 2D space point representation.

    Attributes:
        coords (dict of float): point coordinates.
    """
    def __init__(self, x=0, y=0):
        self.coords = dict()
        self.coords['x'] = real.parse(x)
        self.coords['y'] = real.parse(y)

    @classmethod
    def get(cls):
        x = real.get('x: ')
        y = real.get('y: ')
        return cls(x, y)

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}({self.coords["x"]}, {self.coords["y"]})'

    def __str__(self):
        return f'({self.coords["x"]}, {self.coords["y"]})'
