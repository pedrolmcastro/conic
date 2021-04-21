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
        return self._equation.a * self._equation.c - self._equation.b ** 2 / 4

    def isvalid(self):
        return any([getattr(self._equation, coefficient) != 0 for coefficient in ['a', 'b', 'c']])

    def identify(self):
        if not self.isvalid():
            raise ValueError(f'the conic equation {self._equation} is invalid')
        self._findCenter()
        if isinstance(self._center, self._Point) or self._center == math.inf:
            self._translate()
        if self._equation.b != 0:
            self._rotate()
        self._findName()

    def _findCenter(self):
        # ax + by/2 + d/2 = 0
        # bx/2 + cy + e/2 = 0
        # independent system
        if self.determinant != 0:
            if self._equation.a == 0:
                y = - self._equation.d / self._equation.b
                x = - (2 * self._equation.c * y + self._equation.e) / self._equation.b
            else:
                y = (self._equation.b * self._equation.d - 2 * self._equation.a * self._equation.e) / (4 * self.determinant)
                x = - (self._equation.b * y + self._equation.d) / (2 * self._equation.a)
            self._center = self._Point(x, y)
        # dependent system
        elif ((self._equation.a != 0 and
               math.isclose(self._equation.e, (self._equation.b * self._equation.d) / (2 * self._equation.a))) or
              (self._equation.c != 0 and
               math.isclose(self._equation.d, (self._equation.b * self._equation.e) / (2 * self._equation.c)))):
            self._center = math.inf
        # inconsistent system
        else:
            self._center = None

    def _translate(self):
        if isinstance(self._center, self._Point):
            self._equation.f += (self._equation.d * self._center.x + self._equation.e * self._center.y) / 2
            self._equation.d = 0
            self._equation.e = 0
        elif self._center == math.inf:
            if self._equation.a != 0:
                x = - self._equation.d / (2 * self._equation.a)
                y = 0
            else:  # c != 0
                x = 0
                y = - self._equation.e / (2 * self._equation.c)
            self._equation.f += (self._equation.d * x + self._equation.e * y) / 2
            self._equation.d = 0
            self._equation.e = 0

    def _findRotationAngle(self):
        # cot(2θ) = (a-c)/b
        if self._equation.b == 0:
            self._angle = 0
        elif self._equation.a - self._equation.c == 0:
            self._angle = math.pi / 4
        else:
            self._angle = math.atan2(self._equation.b, self._equation.a - self._equation.c) / 2

    def _rotate(self):
        if self._equation.b != 0:
            self._findRotationAngle()
            # d' = dcos(θ) + esin(θ)
            # e' = -dsin(θ) + ecos(θ)
            d = self._equation.d
            e = self._equation.e
            self._equation.d = d * math.cos(self._angle) + e * math.sin(self._angle)
            self._equation.e = - d * math.sin(self._angle) + e * math.cos(self._angle)
            # a' + c' = a + c
            # a' - c' = b√1+((a-c)/b)²
            a = self._equation.a
            c = self._equation.c
            self._equation.a = (a + c + self._equation.b * math.sqrt(1 + ((a - c) / self._equation.b) ** 2)) / 2
            self._equation.c = a + c - self._equation.a
            self._equation.b = 0

    def _findName(self):
        # nothing, point, circle, ellipse, hyperbola or intersecting lines
        if isinstance(self._center, self._Point):
            if self._equation.f == 0:
                # ax² + cy² = 0
                if self._equation.a * self._equation.c < 0:
                    self._name = 'intersecting lines'
                else:
                    self._name = 'point'
            else:
                A = - self._equation.a / self._equation.f
                C = - self._equation.c / self._equation.f
                # Ax² + Cy² = 1
                if A * C < 0:
                    self._name = 'hyperbola'
                elif A < 0 and C < 0:
                    self._name = 'nothing'
                else:
                    if A == C:
                        self._name = 'circle'
                    else:
                        self._name = 'ellipse'
        # nothing, parallel lines or coincident lines
        elif self._center == math.inf:
            # ax² + f = 0 or cy² + f = 0
            if self._equation.f == 0:
                self._name = 'coincident lines'
            elif self._equation.a * self._equation.f < 0 or self._equation.c * self._equation.f < 0:
                self._name = 'parallel lines'
            else:
                self._name = 'nothing'
        # nothing or parabola
        elif self._center == None:
            if self._equation.a != 0 and self._equation.e != 0:
                self._name = 'parabola'
            elif self._equation.c != 0 and self._equation.d != 0:
                self._name = 'parabola'
            else:
                self._name = 'nothing'

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
