import math
import copy

import real
from point import Point
from equation import Equation

class Conic:
    """
    A conic representation.
    
    Attributes:
        _eqt (Equation): general form equation.
        _ctr (Point/inf/None/str): number of centers the conic has and its coordinates if unique.
        _name (str): one of ['unknown', 'nothing', 'point', 'intersecting lines', 'parallel lines',
                             'coincident lines', 'circle', 'ellipse', 'hyperbola', 'parabola'].
    """
    def __init__(self, a, b, c, d, e, f):
        self._eqt = Equation(a, b, c, d, e, f)
        self._ctr = 'unknown'
        self._name = 'unknown'

    @classmethod
    def frominput(cls):
        a = real.get('a: ')
        b = real.get('b: ')
        c = real.get('c: ')
        d = real.get('d: ')
        e = real.get('e: ')
        f = real.get('f: ')
        return cls(a, b, c, d, e, f)

    @classmethod
    def fromequation(cls, eqt):
        if not isinstance(eqt, Equation):
            raise TypeError(f'equation must be of class Equation, not {type(eqt)}')
        a = eqt.coeffs['a']
        b = eqt.coeffs['b']
        c = eqt.coeffs['c']
        d = eqt.coeffs['d']
        e = eqt.coeffs['e']
        f = eqt.coeffs['f']
        return cls(a, b, c, d, e, f)

    def __repr__(self):
        return (f'{self.__class__.__module__}.{self.__class__.__qualname__}' +
                f'({self._eqt.coeffs["a"]}, {self._eqt.coeffs["b"]}, {self._eqt.coeffs["c"]}, ' +
                f'{self._eqt.coeffs["d"]}, {self._eqt.coeffs["e"]}, {self._eqt.coeffs["f"]})')

    def __str__(self):
        return self._name

    @property
    def equation(self):
        return copy.deepcopy(self._eqt)

    @property
    def center(self):
        return copy.deepcopy(self._ctr)

    @property
    def name(self):
        return self._name

    @property
    def det(self):
        return self._eqt.coeffs['a']*self._eqt.coeffs['c'] - self._eqt.coeffs['b']**2/4 #a*c - b²/4

    def isvalid(self):
        if self._eqt.coeffs['a'] != 0 or self._eqt.coeffs['b'] != 0 or self._eqt.coeffs['c'] != 0:
            return True
        else:
            return False

    def _isDependentSystem(self):
        if (self._eqt.coeffs['a'] != 0 and
           math.isclose(self._eqt.coeffs['e'], (self._eqt.coeffs['b']*self._eqt.coeffs['d']) / (2*self._eqt.coeffs['a']))): #e = bd/2a
            return True
        elif (self._eqt.coeffs['c'] != 0 and
             math.isclose(self._eqt.coeffs['d'], (self._eqt.coeffs['b']*self._eqt.coeffs['e']) / (2*self._eqt.coeffs['c']))): #d = be/2c
            return True
        else:
            return False

    def _findCenter(self):
        #ah + bk/2 + d/2 = 0
        #bh/2 + ck + e/2 = 0
        if self.det != 0: #independent system
            if self._eqt.coeffs['a'] == 0:
                k = - self._eqt.coeffs['d'] / self._eqt.coeffs['b'] #k = -d/b
                h = - (2*self._eqt.coeffs['c']*k + self._eqt.coeffs['e']) / self._eqt.coeffs['b'] #h = -(2ck + e) / b
            else:
                k = (self._eqt.coeffs['b']*self._eqt.coeffs['d'] - 2*self._eqt.coeffs['a']*self._eqt.coeffs['e']) / (4*self.det) #k = (b*d - 2*a*e) / (4*det)
                h = - (self._eqt.coeffs['b']*k + self._eqt.coeffs['d']) / (2*self._eqt.coeffs['a']) #h = -(bk + d) / 2a
            self._ctr = Point(h, k)
        elif self._isDependentSystem():
            self._ctr = math.inf
        else: #inconsistent system
            self._ctr = None

    def _translate(self):
        if isinstance(self._ctr, Point):
            self._eqt.coeffs['f'] += (self._eqt.coeffs['d']*self._ctr.coords['x'] + self._eqt.coeffs['e']*self._ctr.coords['y']) / 2 #f = f + dh/2 + ek/2
            self._eqt.coeffs['d'] = 0
            self._eqt.coeffs['e'] = 0
        elif self._ctr == math.inf:
            if self._eqt.coeffs['a'] != 0:
                k = 0
                h = - self._eqt.coeffs['d'] / (2*self._eqt.coeffs['a']) #h = -d/2a
            else: #c != 0
                h = 0
                k = - self._eqt.coeffs['e'] / (2*self._eqt.coeffs['c']) #k = -e/2c
            self._eqt.coeffs['f'] += (self._eqt.coeffs['d']*h + self._eqt.coeffs['e']*k) / 2 #f = f + dh/2 + ek/2
            self._eqt.coeffs['d'] = 0
            self._eqt.coeffs['e'] = 0

    def identify(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self._eqt} is invalid')
        self._findCenter()
        if isinstance(self._ctr, Point) or self._ctr == math.inf:
            self._translate()
