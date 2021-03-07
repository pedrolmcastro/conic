import real

class Equation:
    """
    A conic equation general form representation.
    
    Attributes:
        a (float): coefficient of x².
        b (float): coefficient of xy.
        c (float): coefficient of y².
        d (float): coefficient of x.
        e (float): coefficient of y.
        f (float): linear term.
    """
    def __init__(self, a, b, c, d, e, f):
        self.a = real.parse(a)
        self.b = real.parse(b)
        self.c = real.parse(c)
        self.d = real.parse(d)
        self.e = real.parse(e)
        self.f = real.parse(f)

    @classmethod
    def frominput(cls):
        a = real.get('a: ')
        b = real.get('b: ')
        c = real.get('c: ')
        d = real.get('d: ')
        e = real.get('e: ')
        f = real.get('f: ')
        return cls(a, b, c, d, e, f)

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

        string = 'g(x, y) ='
        for coeff, val in self.__dict__.items():
            if val < 0:
                string += f' - {-val}{coeffToVar[coeff]}'
            #if val == 0 the term is not printed
            elif val > 0:
                string += f' + {val}{coeffToVar[coeff]}'
        if string == 'g(x, y) =': #empty equation
            string += ' 0'

        return string
