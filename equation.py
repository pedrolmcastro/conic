import real

class Equation:
    """
    A conic equation general form representation.
    
    Attributes:
        coeff (dict of float): all equation coefficients
    """

    def __init__(self, a=1, b=1, c=1, d=0, e=0, f=0):
        self.coeff = dict()
        self.coeff['a'] = real.parse(a)
        self.coeff['b'] = real.parse(b)
        self.coeff['c'] = real.parse(c)
        self.coeff['d'] = real.parse(d)
        self.coeff['e'] = real.parse(e)
        self.coeff['f'] = real.parse(f)


    @classmethod
    def get(cls):
        a = real.get('a: ')
        b = real.get('b: ')
        c = real.get('c: ')
        d = real.get('d: ')
        e = real.get('e: ')
        f = real.get('f: ')
        return Equation(a, b, c, d, e, f)
