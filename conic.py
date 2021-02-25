import math

import real
from point import Point
from equation import Equation

class Conic:
    """
    A conic representation.
    
    Attributes:
        equation (Equation): general form equation.
        center (Point/inf/None/str): number of centers the conic has and its coordinates if unique.
        name (str): one of ['unknown', 'nothing', 'point', 'intersecting lines', 'parallel lines',
                            'coincident lines', 'circle', 'ellipse', 'hyperbola', 'parabola'].
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

    def __repr__(self):
        return (f'{self.__class__.__module__}.{self.__class__.__qualname__}' +
                f'({self.equation.coeffs["a"]}, {self.equation.coeffs["b"]}, {self.equation.coeffs["c"]}, ' +
                f'{self.equation.coeffs["d"]}, {self.equation.coeffs["e"]}, {self.equation.coeffs["f"]})')
    
    def __str__(self):
        return self.name
    
    def isvalid(self):
        if self.equation.coeffs.keys() == {'a', 'b', 'c', 'd', 'e', 'f'}:
            if self.equation.coeffs['a'] != 0 or self.equation.coeffs['b'] != 0 or self.equation.coeffs['c'] != 0:
                return True
        return False

    @property
    def det(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self.equation} is invalid')
        return self.equation.coeffs['a']*self.equation.coeffs['c'] - self.equation.coeffs['b']**2/4 #a*c - b²/4

    def __isDependentSystem(self):
        if (self.equation.coeffs['a'] != 0 and
           math.isclose(self.equation.coeffs['e'], (self.equation.coeffs['b']*self.equation.coeffs['d']) / (2*self.equation.coeffs['a']))):
            return True
        elif (self.equation.coeffs['c'] != 0 and
             math.isclose(self.equation.coeffs['d'], (self.equation.coeffs['b']*self.equation.coeffs['e']) / (2*self.equation.coeffs['c']))):
            return True
        else:
            return False

    def findCenter(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self.equation} is invalid')
        #ah + bk/2 + d/2 = 0
        #bh/2 + ck + e/2 = 0
        if self.equation.coeffs['d'] == 0 and self.equation.coeffs['e'] == 0:
            self.center = Point(0, 0)
        if self.det != 0: #independent system
            if self.equation.coeffs['a'] == 0:
                k = - self.equation.coeffs['d'] / self.equation.coeffs['b'] #k = -d/b
                h = - (2*self.equation.coeffs['c']*k + self.equation.coeffs['e']) / self.equation.coeffs['b'] #h = -2ck/b - e/b
            else:
                k = (self.equation.coeffs['b']*self.equation.coeffs['d'] - 2*self.equation.coeffs['a']*self.equation.coeffs['e']) / (4*self.det) #k = (b*d - 2*a*e) / (4*det)
                h = - (self.equation.coeffs['b']*k + self.equation.coeffs['d']) / (2*self.equation.coeffs['a']) #h = -(bk + d) / 2a
            self.center = Point(h, k)
        elif self.__isDependentSystem():
            self.center = math.inf
        else: #inconsistent system
            self.center = None

    def translate(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self.equation} is invalid')
        self.findCenter()
        if isinstance(self.center, Point):
            self.equation.coeffs['f'] += (self.equation.coeffs['d']*self.center.coords['x'] + self.equation.coeffs['e']*self.center.coords['y']) / 2 #f = f + dh/2 + ek/2
            self.equation.coeffs['d'] = 0
            self.equation.coeffs['e'] = 0
        elif self.center == math.inf:
            if self.equation.coeffs['a'] != 0:
                k = 0
                h = - self.equation.coeffs['d'] / (2*self.equation.coeffs['a']) #h = -d/2a
            else: #c != 0
                h = 0
                k = - self.equation.coeffs['e'] / (2*self.equation.coeffs['c']) #k = -e/2c
            self.equation.coeffs['f'] += (self.equation.coeffs['d']*h + self.equation.coeffs['e']*k) / 2 #f = f + dh/2 + ek/2
            self.equation.coeffs['d'] = 0
            self.equation.coeffs['e'] = 0
