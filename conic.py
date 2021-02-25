import real
from equation import Equation

class Conic:
    """
    A conic representation.
    
    Attributes:
        equation (Equation): general form equation.
        center (Point/inf/None/str): number of centers the conic has and its coordinates if unique.
        name (str): one of ['unknown', 'empty', 'point', 'intersecting lines', 'parallel lines',
                            'coincident lines', 'circumference', 'ellipse', 'hyperbole', 'parable'].
    """
    def __init__(self, a, b, c, d, e, f):
        self.equation = Equation(a, b, c, d, e, f)
        self.center = 'unknown'
        self.name = 'unknown'

    @classmethod
    def get(cls):
        a = real.get('a: ')
        b = real.get('b: ')
        c = real.get('c: ')
        d = real.get('d: ')
        e = real.get('e: ')
        f = real.get('f: ')
        return cls(a, b, c, d, e, f)
    
    def isvalid(self):
        if self.equation.coeffs.keys() == {'a', 'b', 'c', 'd', 'e', 'f'}:
            if self.equation.coeffs['a'] != 0 or self.equation.coeffs['b'] != 0 or self.equation.coeffs['c'] != 0:
                return True
        return False
