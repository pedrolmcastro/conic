from __future__ import annotations

import math
import copy
from typing import Union, NamedTuple

import number


class Point:
    '''2D point.'''

    def __init__(self, x, y) -> None:
        self.x = number.Real.parse(x)
        self.y = number.Real.parse(y)

    def __repr__(self) -> str:
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}({self.x}, {self.y})'

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'


class Equation:
    '''Conic general form equation.'''

    COEFFICIENT_TO_VARIABLE = {
        'a': 'x²',
        'b': 'xy',
        'c': 'y²',
        'd': 'x',
        'e': 'y',
        'f': '',
    }

    def __init__(self, a, b, c, d, e, f) -> None:
        self.a = number.Real.parse(a)
        self.b = number.Real.parse(b)
        self.c = number.Real.parse(c)
        self.d = number.Real.parse(d)
        self.e = number.Real.parse(e)
        self.f = number.Real.parse(f)

    @classmethod
    def frominput(cls):
        a = number.Real.get('a: ')
        b = number.Real.get('b: ')
        c = number.Real.get('c: ')
        d = number.Real.get('d: ')
        e = number.Real.get('e: ')
        f = number.Real.get('f: ')
        return cls(a, b, c, d, e, f)

    def __repr__(self) -> str:
        return (f'{self.__class__.__module__}.{self.__class__.__qualname__}' + 
                f'({self.a}, {self.b}, {self.c}, {self.d}, {self.e}, {self.f})')

    def __str__(self) -> str:
        return ' + '.join([f'({value}){self.COEFFICIENT_TO_VARIABLE[coefficient]}'
                           for coefficient, value in self.__dict__.items() if value != 0])


class Conic(NamedTuple):
    '''Conic data and functions.'''
    name: str
    center: Union[Point, float, None]
    rotation_angle: float
    translated_equation: Equation
    rotated_equation: Equation

    @staticmethod
    def determinant(equation: Equation) -> float:
        return equation.a * equation.c - equation.b ** 2 / 4

    @staticmethod
    def isconic(equation: Equation) -> bool:
        return any([getattr(equation, coefficient) != 0 for coefficient in ['a', 'b', 'c']])

    @classmethod
    def identify(cls, equation: Equation) -> Conic:
        if not cls.isconic(equation):
            raise ValueError(f'the equation {equation} is not a conic')
        center = cls._get_center(equation, cls.determinant(equation))
        translated_equation = cls._translate(equation, center)
        rotation_angle = cls._get_rotation_angle(equation)
        rotated_equation = cls._rotate(equation, rotation_angle)
        name = cls._get_name(rotated_equation, center)
        return cls(name, center, rotation_angle, translated_equation, rotated_equation)

    @staticmethod
    def _get_center(equation: Equation, determinant: float) -> Union[Point, float, None]:
        # ax + by/2 + d/2 = 0
        # bx/2 + cy + e/2 = 0
        # independent system
        if determinant != 0:
            if equation.a == 0:
                y = - equation.d / equation.b
                x = - (2 * equation.c * y + equation.e) / equation.b
            else:
                y = (equation.b * equation.d - 2 * equation.a * equation.e) / (4 * determinant)
                x = - (equation.b * y + equation.d) / (2 * equation.a)
            return Point(x, y)
        # dependent system
        elif ((equation.a != 0 and math.isclose(equation.e, (equation.b * equation.d) / (2 * equation.a))) or
              (equation.c != 0 and math.isclose(equation.d, (equation.b * equation.e) / (2 * equation.c)))):
            return math.inf
        # inconsistent system
        else:
            return None

    @staticmethod
    def _translate(equation: Equation, center: Union[Point, float, None]) -> Equation:
        if isinstance(center, Point):
            f = equation.f + (equation.d * center.x + equation.e * center.y) / 2
            return Equation(equation.a, equation.b, equation.c, 0, 0, f)
        elif center == math.inf:
            if equation.a != 0:
                x = - equation.d / (2 * equation.a)
                y = 0.0
            elif equation.c != 0:
                x = 0.0
                y = - equation.e / (2 * equation.c)
            f = equation.f + (equation.d * x + equation.e * y) / 2
            return Equation(equation.a, equation.b, equation.c, 0, 0, f)
        else:
            return copy.deepcopy(equation)

    @staticmethod
    def _get_rotation_angle(equation: Equation) -> float:
        # cot(2θ) = (a-c)/b
        if equation.b == 0:
            return 0.0
        elif equation.a - equation.c == 0:
            return math.pi / 4
        else:
            return math.atan2(equation.b, equation.a - equation.c) / 2

    @staticmethod
    def _rotate(equation: Equation, rotation_angle: float) -> Equation:
        if equation.b != 0:
            # a' + c' = a + c
            # a' - c' = b√1+((a-c)/b)²
            a = (equation.a + equation.c + equation.b * math.sqrt(1 + ((equation.a - equation.c) / equation.b) ** 2)) / 2
            c = equation.a + equation.c - a
            # d' = dcos(θ) + esin(θ)
            # e' = -dsin(θ) + ecos(θ)
            d = equation.d * math.cos(rotation_angle) + equation.e * math.sin(rotation_angle)
            e = - equation.d * math.sin(rotation_angle) + equation.e * math.cos(rotation_angle)
            return Equation(a, 0, c, d, e, equation.f)
        else:
            return copy.deepcopy(equation)

    @staticmethod
    def _get_name(equation: Equation, center: Union[Point, float, None]) -> str:
        if isinstance(center, Point):
            if equation.f == 0:
                # ax² + cy² = 0
                if equation.a * equation.c < 0:
                    return 'intersecting lines'
                else:
                    return 'point'
            else:
                A = - equation.a / equation.f
                C = - equation.c / equation.f
                # Ax² + Cy² = 1
                if A * C < 0:
                    return 'hyperbola'
                elif A < 0 and C < 0:
                    return 'nothing'
                elif A == C:
                    return 'circle'
                else:
                    return 'ellipse'
        elif center == math.inf:
            # ax² + f = 0 or cy² + f = 0
            if equation.f == 0:
                return 'coincident lines'
            elif equation.a * equation.f < 0 or equation.c * equation.f < 0:
                return 'parallel lines'
            else:
                return 'nothing'
        elif center == None:
            if (equation.a != 0 and equation.e != 0) or (equation.c != 0 and equation.d != 0):
                return 'parabola'
            else:
                return 'nothing'
        else:
            return 'unknown'
