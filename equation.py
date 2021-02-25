import real

class Equation:
    """
    A conic equation general form representation.
    
    Attributes:
        coeffs (dict of float): all equation coefficients.
    """
    def __init__(self, a, b, c, d, e, f):
        self.coeffs = dict()
        self.coeffs['a'] = real.parse(a)
        self.coeffs['b'] = real.parse(b)
        self.coeffs['c'] = real.parse(c)
        self.coeffs['d'] = real.parse(d)
        self.coeffs['e'] = real.parse(e)
        self.coeffs['f'] = real.parse(f)

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
                f'({self.coeffs["a"]}, {self.coeffs["b"]}, {self.coeffs["c"]}, {self.coeffs["d"]}, {self.coeffs["e"]}, {self.coeffs["f"]})')

    def __str__(self):
        coeffToVar = {
            'a': 'x²',
            'b': 'xy',
            'c': 'y²',
            'd': 'x',
            'e': 'y',
            'f': '',
        }

        string = 'g(x, y) ='
        for coeff, val in self.coeffs.items():
            if coeff in coeffToVar.keys():
                if val < 0:
                    string += f' - {-val}{coeffToVar[coeff]}'
                elif val > 0:
                    string += f' + {val}{coeffToVar[coeff]}'
                #val == 0 is not printed
        if string == 'g(x, y) =': #all val == 0
            string += ' 0'
        return string
