import math
import typing


class Conic:
    """Conic of equation ax² + bxy + cy² + dx + ey + f = 0"""

    def __init__(self, a: float, b: float, c: float, d: float, e: float, f:float) -> None:
        # Validate
        self.equations = [self._equation(a, b, c, d, e, f)]

        # Translate
        self.center = self._center(self.equations[0])
        self.equations.append(self._translate(self.equations[0], self.center))

        # Rotate
        self.angle = self._angle(self.equations[1])
        self.equations.append(self._rotate(self.equations[1], self.angle))

        # Classify
        self.name = self._name(self.equations[2], self.center)
    
    def __str__(self):
        return (
            f"Name:                {self.name}        \n"
            f"Center:              {self.center}      \n"
            f"Rotation Angle:      {self.angle}       \n"
            f"Initial Equation:    {self.equations[0]}\n"
            f"Translated Equation: {self.equations[1]}\n"
            f"Rotated Equation:    {self.equations[2]}"
        )
    
    @staticmethod
    def _determinant(equation: dict[str, float]) -> float:
        # | a   b/2 | = ac - b²/4
        # | b/2 c   |
        return equation['a'] * equation['c'] - equation['b'] ** 2 / 4

    @staticmethod
    def _equation(a: float, b: float, c: float, d: float, e: float, f:float) -> dict[str, float]:
        equation = locals().copy()
        
        if not all(type(coefficient) in (int, float) and math.isfinite(coefficient) for coefficient in equation.values()):
            raise TypeError("All coefficients must be finite integers or floats")
        elif not any(equation[coefficient] != 0 for coefficient in ['a', 'b', 'c']):
            raise ValueError("Coefficients 'a', 'b' and 'c' can not all be 0")
        
        return equation
    
    @classmethod
    def _center(cls, equation: dict[str, float]) -> tuple[float, float] | float | None:
        # ax + by/2 + d/2 = 0
        # bx/2 + cy + e/2 = 0
        determinant = cls._determinant(equation)
                
        # Independent system
        if determinant != 0:
            if equation['a'] == 0:
                y = - equation['d'] / equation['b']
                x = - (2 * equation['c'] * y + equation['e']) / equation['b']
            else:
                y = (equation['b'] * equation['d'] - 2 * equation['a'] * equation['e']) / (4 * determinant)
                x = - (equation['b'] * y + equation['d']) / (2 * equation['a'])
            return x, y
        
        # Dependent system
        if (equation['a'] != 0 and math.isclose(equation['e'], equation['b'] * equation['d'] / (2 * equation['a'])) or
            equation['c'] != 0 and math.isclose(equation['d'], equation['b'] * equation['e'] / (2 * equation['c']))):
            return math.inf
        
        # Inconsistent system
        return None
    
    @staticmethod
    def _translate(equation: dict[str, float], center: tuple[float, float] | float | None) -> dict[str, float]:
        translated = equation.copy()

        # Unique center
        if type(center) is tuple:
            center = typing.cast(tuple[float, float], center)
            translated['f'] += (equation['d'] * center[0] + equation['e'] * center[1]) / 2
            translated['d'] = translated['e'] = 0
        
        # Infinite centers
        elif center == math.inf:
            if equation['a'] != 0:
                x = - equation['d'] / (2 * equation['a'])
                y = 0.
            else:
                x = 0.
                y = - equation['e'] / (2 * equation['c'])
            translated['f'] += (equation['d'] * x + equation['e'] * y) / 2
            translated['d'] = translated['e'] = 0
        
        return translated
    
    @staticmethod
    def _angle(equation: dict[str, float]) -> float:
        # cot(2θ) = (a - c)/b
        if equation['b'] == 0:
            return 0
        elif equation['a'] - equation['c'] == 0:
            return math.pi / 4
        return math.atan2(equation['b'], equation['a'] - equation['c']) / 2
    
    @staticmethod
    def _rotate(translated: dict[str, float], angle: float) -> dict[str, float]:
        rotated = translated.copy()

        if translated['b'] != 0:
            rotated['b'] = 0
            # a' + c' = a + c
            # a' - c' = b √1 + ((a - c)/b)²
            rotated['a'] = (translated['a'] + translated['c'] + translated['b'] * math.sqrt(1 + ((translated['a'] - translated['c']) / translated['b']) ** 2)) / 2
            rotated['c'] = translated['a'] + translated['c'] - rotated['a']
            # d' = d cos(θ) + e sin(θ)
            # e' = - d sin(θ) + e cos(θ)
            rotated['d'] = translated['d'] * math.cos(angle) + translated['e'] * math.sin(angle)
            rotated['e'] = - translated['d'] * math.sin(angle) + translated['e'] * math.cos(angle)
        
        return rotated
    
    @staticmethod
    def _name(rotated: dict[str, float], center: tuple[float, float] | float | None) -> str:
        # Unique center
        if type(center) is tuple:
            if rotated['f'] == 0:
                # ax² + cy² = 0
                return "Intersecting lines" if rotated['a'] * rotated['c'] < 0 else "Point"
            # ax²/f + cy²/f = Ax² + Cy² = 1
            A = - rotated['a'] / rotated['f']
            C = - rotated['c'] / rotated['f']
            if A < 0 and C < 0:
                return "Nothing"
            if A * C < 0:
                return "Hyperbola"
            if A == C:
                return "Circle"
            return "Ellipse"
        
        # Infinite centers
        if center == math.inf:
            # ax² + f = 0 or cy² + f = 0
            if rotated['f'] == 0:
                return "Coincident lines"
            if rotated['a'] * rotated['f'] < 0 or rotated['c'] * rotated['f'] < 0:
                return "Parallel lines"
            return "Nothing"
        
        # No center
        return "Parabola" if rotated['a'] != 0 and rotated['e'] != 0 or rotated['c'] != 0 and rotated['d'] != 0 else "Nothing"
