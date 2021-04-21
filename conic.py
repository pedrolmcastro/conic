import math
import copy

import number


class Conic:
    """
    A conic representation.
    
    Attributes:
        _equation (_Equation): general form equation.
        _center (_Point/inf/None/str): number of centers the conic has and its coordinates if unique.
        _name (str): one of ['unknown', 'nothing', 'point', 'intersecting lines', 'parallel lines',
                             'coincident lines', 'circle', 'ellipse', 'hyperbola', 'parabola'].
        _angle (float): angle of the rotation made to identify the conic.
    """

    def __init__(self, a, b, c, d, e, f):
        self._equation = self._Equation(a, b, c, d, e, f)
        self._center = 'unknown'
        self._name = 'unknown'
        self._angle = 0

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
                f'({self._equation.a}, {self._equation.b}, {self._equation.c}, ' +
                f'{self._equation.d}, {self._equation.e}, {self._equation.f})')

    def __str__(self):
        return self._name

    @property
    def equation(self):
        return copy.deepcopy(self._equation)

    @property
    def center(self):
        return copy.deepcopy(self._center)

    @property
    def name(self):
        return self._name

    @property
    def angle(self):
        return self._angle

    @property
    def determinant(self):
        #determinant = ac - b²/4
        return self._equation.a * self._equation.c - self._equation.b ** 2 / 4

    def isvalid(self):
        if self._equation.a != 0 or self._equation.b != 0 or self._equation.c != 0:
            return True
        else:
            return False

    def _findCenter(self):
        #ah + bk/2 + d/2 = 0
        #bh/2 + ck + e/2 = 0
        #independent system
        if self.determinant != 0:
            if self._equation.a == 0:
                k = - self._equation.d / self._equation.b #k = -d/b
                h = - (2 * self._equation.c * k + self._equation.e) / self._equation.b #h = -(2ck + e) / b
            else:
                k = (self._equation.b * self._equation.d - 2 * self._equation.a * self._equation.e) / (4 * self.determinant) #k = (bd - 2ae) / (4*determinant)
                h = - (self._equation.b * k + self._equation.d) / (2 * self._equation.a) #h = -(bk + d) / 2a
            self._center = self._Point(h, k)
        #dependent system:
        elif self._equation.a != 0 and math.isclose(self._equation.e, (self._equation.b * self._equation.d) / (2 * self._equation.a)): #e = bd/2a
            self._center = math.inf
        elif self._equation.c != 0 and math.isclose(self._equation.d, (self._equation.b * self._equation.e) / (2 * self._equation.c)): #d = be/2c
            self._center = math.inf
        #inconsistent system
        else:
            self._center = None

    def _translate(self):
        if isinstance(self._center, self._Point):
            self._equation.f += (self._equation.d * self._center.x + self._equation.e * self._center.y) / 2 #f' = f + dh/2 + ek/2
            self._equation.d = 0
            self._equation.e = 0
        elif self._center == math.inf:
            if self._equation.a != 0:
                k = 0
                h = - self._equation.d / (2 * self._equation.a) #h = -d/2a
            else: #c != 0
                h = 0
                k = - self._equation.e / (2 * self._equation.c) #k = -e/2c
            self._equation.f += (self._equation.d * h + self._equation.e * k) / 2 #f' = f + dh/2 + ek/2
            self._equation.d = 0
            self._equation.e = 0

    def _findRotationAngle(self):
        if self._equation.b == 0:
            self._angle = 0
        #cot(2θ) = (a-c)/b
        elif self._equation.a - self._equation.c == 0:
            self._angle = math.pi / 4 #2θ = pi/2 = acot(0)
        else:
            self._angle = math.atan2(self._equation.b, self._equation.a - self._equation.c) / 2 #2θ = atan(b/(a-c))

    def _rotate(self):
        if self._equation.b != 0:
            self._findRotationAngle()
            #d' = dcos(θ) + esin(θ)
            #e' = -dsin(θ) + ecos(θ)
            d = self._equation.d
            e = self._equation.e
            self._equation.d = d * math.cos(self._angle) + e * math.sin(self._angle) #d' = dcos(θ) + esin(θ)
            self._equation.e = - d * math.sin(self._angle) + e * math.cos(self._angle) #e' = -dsin(θ) + ecos(θ)
            #a' + c' = a + c
            #a' - c' = b√1+((a-c)/b)²
            a = self._equation.a
            c = self._equation.c
            self._equation.a = (a + c + self._equation.b * math.sqrt(1 + ((a - c) / self._equation.b) ** 2)) / 2 #a' = (a + c + b√1+((a-c)/b)²) / 2
            self._equation.c = a + c - self._equation.a #c' = a + c - a'
            self._equation.b = 0

    def _findName(self):
        #nothing, point, circle, ellipse, hyperbola or intersecting lines
        if isinstance(self._center, self._Point):
            if self._equation.f == 0:
                #ax² + cy² = 0
                if self._equation.a * self._equation.c < 0:
                    self._name = 'intersecting lines'
                else:
                    self._name = 'point'
            else:
                A = - self._equation.a / self._equation.f
                C = - self._equation.c / self._equation.f
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
        elif self._center == math.inf:
            #ax² + f = 0 or cy² + f = 0
            if self._equation.f == 0:
                self._name = 'coincident lines'
            elif self._equation.a * self._equation.f < 0 or self._equation.c * self._equation.f < 0:
                self._name = 'parallel lines'
            else:
                self._name = 'nothing'
        #nothing or parabola
        elif self._center == None:
            if self._equation.a != 0 and self._equation.e != 0:
                self._name = 'parabola'
            elif self._equation.c != 0 and self._equation.d != 0:
                self._name = 'parabola'
            else:
                self._name = 'nothing'

    def identify(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self._equation} is invalid')
        self._findCenter()
        if isinstance(self._center, self._Point) or self._center == math.inf:
            self._translate()
        if self._equation.b != 0:
            self._rotate()
        self._findName()

    class _Point:
        '''2D point.'''

        def __init__(self, x, y):
            self.x = number.Real.parse(x)
            self.y = number.Real.parse(y)

        def __repr__(self):
            return f'{self.__class__.__module__}.{self.__class__.__qualname__}({self.x}, {self.y})'

        def __str__(self):
            return f'({self.x}, {self.y})'

    class _Equation:
        '''Conic general form equation.'''

        COEFFICIENT_TO_VARIABLE = {
            'a': 'x²',
            'b': 'xy',
            'c': 'y²',
            'd': 'x',
            'e': 'y',
            'f': '',
        }

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
            return ' + '.join([f'({value}){self.COEFFICIENT_TO_VARIABLE[coefficient]}'
                               for coefficient, value in self.__dict__.items() if value != 0])
