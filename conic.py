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
        _ang (float): angle of the rotation made to identify the conic.
    """
    def __init__(self, a, b, c, d, e, f):
        self._eqt = Equation(a, b, c, d, e, f)
        self._ctr = 'unknown'
        self._name = 'unknown'
        self._ang = 0

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
        a = eqt.a
        b = eqt.b
        c = eqt.c
        d = eqt.d
        e = eqt.e
        f = eqt.f
        return cls(a, b, c, d, e, f)

    def __repr__(self):
        return (f'{self.__class__.__module__}.{self.__class__.__qualname__}' +
                f'({self._eqt.a}, {self._eqt.b}, {self._eqt.c}, {self._eqt.d}, {self._eqt.e}, {self._eqt.f})')

    def __str__(self):
        return self._name

    @property
    def equation(self):
        return copy.deepcopy(self._eqt)

    @property
    def center(self):
        return copy.deepcopy(self._ctr)

    @property
    def angle(self):
        return self._ang

    @property
    def name(self):
        return self._name

    @property
    def det(self):
        return self._eqt.a*self._eqt.c - self._eqt.b**2/4 #det = ac - b²/4

    def isvalid(self):
        if self._eqt.a != 0 or self._eqt.b != 0 or self._eqt.c != 0:
            return True
        else:
            return False

    def _isDependentSystem(self):
        if self._eqt.a != 0 and math.isclose(self._eqt.e, (self._eqt.b*self._eqt.d) / (2*self._eqt.a)): #e = bd/2a
            return True
        elif self._eqt.c != 0 and math.isclose(self._eqt.d, (self._eqt.b*self._eqt.e) / (2*self._eqt.c)): #d = be/2c
            return True
        else:
            return False

    def _findCenter(self):
        #ah + bk/2 + d/2 = 0
        #bh/2 + ck + e/2 = 0
        if self.det != 0: #independent system
            if self._eqt.a == 0:
                k = - self._eqt.d / self._eqt.b #k = -d/b
                h = - (2*self._eqt.c*k + self._eqt.e) / self._eqt.b #h = -(2ck + e) / b
            else:
                k = (self._eqt.b*self._eqt.d - 2*self._eqt.a*self._eqt.e) / (4*self.det) #k = (bd - 2ae) / (4*det)
                h = - (self._eqt.b*k + self._eqt.d) / (2*self._eqt.a) #h = -(bk + d) / 2a
            self._ctr = Point(h, k)
        elif self._isDependentSystem():
            self._ctr = math.inf
        else: #inconsistent system
            self._ctr = None

    def _translate(self):
        if isinstance(self._ctr, Point):
            self._eqt.f += (self._eqt.d*self._ctr.x + self._eqt.e*self._ctr.y) / 2 #f' = f + dh/2 + ek/2
            self._eqt.d = 0
            self._eqt.e = 0
        elif self._ctr == math.inf:
            if self._eqt.a != 0:
                k = 0
                h = - self._eqt.d / (2*self._eqt.a) #h = -d/2a
            else: #c != 0
                h = 0
                k = - self._eqt.e / (2*self._eqt.c) #k = -e/2c
            self._eqt.f += (self._eqt.d*h + self._eqt.e*k) / 2 #f' = f + dh/2 + ek/2
            self._eqt.d = 0
            self._eqt.e = 0

    def _findRotationAngle(self):
        #Trigonometric functions values of 2*ang
        doubleAngCotg = (self._eqt.a - self._eqt.c) / self._eqt.b #cotg(2θ) = (a-c)/b
        doubleAngSin = 1 / math.sqrt(1 + doubleAngCotg**2) #sin(2θ) = 1/√1+cotg(2θ)²
        doubleAngCos = doubleAngSin * doubleAngCotg #cos(2θ) = sin(2θ) * cotg(2θ)
        #Trigonometric functions values of ang
        angSin = math.sqrt((1 - doubleAngCos) / 2) #sin(θ) = √1-cos(2θ)
        angCos = math.sqrt((1 + doubleAngCos) / 2) #cos(θ) = √1+cos(2θ)
        self._ang = math.asin(angSin)
        return angSin, angCos

    def _rotate(self):
        #d' = dcos(θ) + esin(θ)
        #e' = -dsin(θ) + ecos(θ)
        angSin, angCos = self._findRotationAngle()
        d = self._eqt.d
        e = self._eqt.e
        self._eqt.d = d*angCos + e*angSin #d' = dcos(θ) + esin(θ)
        self._eqt.e = - d*angSin + e*angCos #e' = -dsin(θ) + ecos(θ)
        #a' + c' = a + c
        #a' - c' = b√1+((a-c)/b)²
        a = self._eqt.a
        c = self._eqt.c
        self._eqt.a = (a + c + self._eqt.b*math.sqrt(1 + ((a-c)/self._eqt.b)**2)) / 2 #a' = a + c + b√1+((a-c)/b)²
        self._eqt.c = a + c - self._eqt.a #c' = a + c - a'
        self._eqt.b = 0

    def _findName(self):
        if isinstance(self._ctr, Point):
            #nothing, point, circle, ellipse, hyperbola or intersecting lines
            if self._eqt.f == 0:
                if self._eqt.a * self._eqt.c < 0:
                    self._name = 'intersecting lines'
                else: #self._eqt.a * self._eqt.c > 0
                    self._name = 'point'
            else:
                A = - self._eqt.a / self._eqt.f
                C = - self._eqt.c / self._eqt.f
                if A * C < 0:
                    self._name = 'hyperbola'
                elif A < 0 and C < 0:
                    self._name = 'nothing'
                else:
                    if A == C:
                        self._name = 'circle'
                    else:
                        self._name = 'ellipse'
        elif self._ctr == math.inf:
            #nothing, parallel lines or coincident lines
            if self._eqt.a*self._eqt.f < 0 or self._eqt.c*self._eqt.f < 0:
                self._name = 'parallel lines'
            elif self._eqt.f == 0:
                self._name = 'coincident lines'
            else: #self._eqt.a*self._eqt.f > 0 or self._eqt.c*self._eqt.f > 0
                self._name = 'nothing'
        elif self._ctr == None:
            #nothing or parabola
            if self._eqt.a != 0 and self._eqt.e != 0:
                self._name = 'parabola'
            elif self._eqt.c != 0 and self._eqt.d != 0:
                self._name = 'parabola'
            else:
                self._name = 'nothing'

    def identify(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self._eqt} is invalid')
        self._findCenter()
        if isinstance(self._ctr, Point) or self._ctr == math.inf:
            self._translate()
        if self._eqt.b != 0:
            self._rotate()
        self._findName()
