import math
import copy

import number

class _Point:
    """
    A 2D space point representation.

    Attributes:
        x (float): abscissa coordinate.
        y (float): ordinate coordinate.
    """
    def __init__(self, x, y):
        self.x = number.Real.parse(x)
        self.y = number.Real.parse(y)

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'


class _Equation:
    """
    A conic general form equation representation.
    
    Attributes:
        a (float): coefficient of x².
        b (float): coefficient of xy.
        c (float): coefficient of y².
        d (float): coefficient of x.
        e (float): coefficient of y.
        f (float): linear term.
    """
    def __init__(self, a, b, c, d, e, f):
        self.a = number.Real.parse(a)
        self.b = number.Real.parse(b)
        self.c = number.Real.parse(c)
        self.d = number.Real.parse(d)
        self.e = number.Real.parse(e)
        self.f = number.Real.parse(f)

    def __repr__(self):
        return (f'{self.__class__.__module__}.{self.__class__.__qualname__}' + 
                f'({self.a}, {self.b}, {self.c}, {self.d}, {self.e}, {self.f})')

    def __str__(self):
        coeffToVar = {
            'a': 'x²',
            'b': 'xy',
            'c': 'y²',
            'd': 'x',
            'e': 'y',
            'f': '',
        }
        eqt = 'g(x, y) ='
        for coeff, val in self.__dict__.items():
            if val < 0:
                eqt += f' - {-val}{coeffToVar[coeff]}'
            elif val > 0:
                eqt += f' + {val}{coeffToVar[coeff]}'
        if eqt == 'g(x, y) =': #empty equation
            eqt += ' 0'
        return eqt


class Conic:
    """
    A conic representation.
    
    Attributes:
        _eqt (_Equation): general form equation.
        _ctr (_Point/inf/None/str): number of centers the conic has and its coordinates if unique.
        _name (str): one of ['unknown', 'nothing', 'point', 'intersecting lines', 'parallel lines',
                             'coincident lines', 'circle', 'ellipse', 'hyperbola', 'parabola'].
        _ang (float): angle of the rotation made to identify the conic.
    """
    def __init__(self, a, b, c, d, e, f):
        self._eqt = _Equation(a, b, c, d, e, f)
        self._ctr = 'unknown'
        self._name = 'unknown'
        self._ang = 0

    @classmethod
    def frominput(cls):
        a = number.Real.get('a: ')
        b = number.Real.get('b: ')
        c = number.Real.get('c: ')
        d = number.Real.get('d: ')
        e = number.Real.get('e: ')
        f = number.Real.get('f: ')
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
    def name(self):
        return self._name

    @property
    def angle(self):
        return self._ang

    @property
    def det(self):
        return self._eqt.a*self._eqt.c - self._eqt.b**2/4 #det = ac - b²/4

    def isvalid(self):
        if self._eqt.a != 0 or self._eqt.b != 0 or self._eqt.c != 0:
            return True
        else:
            return False

    def _findCenter(self):
        #ah + bk/2 + d/2 = 0
        #bh/2 + ck + e/2 = 0
        #independent system
        if self.det != 0:
            if self._eqt.a == 0:
                k = - self._eqt.d / self._eqt.b #k = -d/b
                h = - (2*self._eqt.c*k + self._eqt.e) / self._eqt.b #h = -(2ck + e) / b
            else:
                k = (self._eqt.b*self._eqt.d - 2*self._eqt.a*self._eqt.e) / (4*self.det) #k = (bd - 2ae) / (4*det)
                h = - (self._eqt.b*k + self._eqt.d) / (2*self._eqt.a) #h = -(bk + d) / 2a
            self._ctr = _Point(h, k)
        #dependent system:
        elif self._eqt.a != 0 and math.isclose(self._eqt.e, (self._eqt.b*self._eqt.d) / (2*self._eqt.a)): #e = bd/2a
            self._ctr = math.inf
        elif self._eqt.c != 0 and math.isclose(self._eqt.d, (self._eqt.b*self._eqt.e) / (2*self._eqt.c)): #d = be/2c
            self._ctr = math.inf
        #inconsistent system
        else:
            self._ctr = None

    def _translate(self):
        if isinstance(self._ctr, _Point):
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
        if self._eqt.b == 0:
            self._ang = 0
        #cot(2θ) = (a-c)/b
        elif self._eqt.a - self._eqt.c == 0:
            self._ang = math.pi / 4 #2θ = pi/2 = acot(0)
        else:
            self._ang = math.atan2(self._eqt.b, self._eqt.a-self._eqt.c) / 2 #2θ = atan(b/(a-c))

    def _rotate(self):
        if self._eqt.b != 0:
            self._findRotationAngle()
            #d' = dcos(θ) + esin(θ)
            #e' = -dsin(θ) + ecos(θ)
            d = self._eqt.d
            e = self._eqt.e
            self._eqt.d = d*math.cos(self._ang) + e*math.sin(self._ang) #d' = dcos(θ) + esin(θ)
            self._eqt.e = - d*math.sin(self._ang) + e*math.cos(self._ang) #e' = -dsin(θ) + ecos(θ)
            #a' + c' = a + c
            #a' - c' = b√1+((a-c)/b)²
            a = self._eqt.a
            c = self._eqt.c
            self._eqt.a = (a + c + self._eqt.b*math.sqrt(1 + ((a-c)/self._eqt.b)**2)) / 2 #a' = (a + c + b√1+((a-c)/b)²) / 2
            self._eqt.c = a + c - self._eqt.a #c' = a + c - a'
            self._eqt.b = 0

    def _findName(self):
        #nothing, point, circle, ellipse, hyperbola or intersecting lines
        if isinstance(self._ctr, _Point):
            if self._eqt.f == 0:
                #ax² + cy² = 0
                if self._eqt.a * self._eqt.c < 0:
                    self._name = 'intersecting lines'
                else:
                    self._name = 'point'
            else:
                A = - self._eqt.a / self._eqt.f
                C = - self._eqt.c / self._eqt.f
                #Ax² + Cy² = 1
                if A * C < 0:
                    self._name = 'hyperbola'
                elif A < 0 and C < 0:
                    self._name = 'nothing'
                else:
                    if A == C:
                        self._name = 'circle'
                    else:
                        self._name = 'ellipse'
        #nothing, parallel lines or coincident lines
        elif self._ctr == math.inf:
            #ax² + f = 0 or cy² + f = 0
            if self._eqt.f == 0:
                self._name = 'coincident lines'
            elif self._eqt.a*self._eqt.f < 0 or self._eqt.c*self._eqt.f < 0:
                self._name = 'parallel lines'
            else:
                self._name = 'nothing'
        #nothing or parabola
        elif self._ctr == None:
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
        if isinstance(self._ctr, _Point) or self._ctr == math.inf:
            self._translate()
        if self._eqt.b != 0:
            self._rotate()
        self._findName()
