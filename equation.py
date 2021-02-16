class Equation:
    """
    A conic equation general form representation.
    Attributes:
        coeff(dict): all equation coefficients 
    """

    def __init__(self, a=1, b=1, c=1, d=0, e=0, f=0):
        self.coeff = dict()
        self.coeff['a'] = float(a)
        self.coeff['b'] = float(b)
        self.coeff['c'] = float(c)
        self.coeff['d'] = float(d)
        self.coeff['e'] = float(e)
        self.coeff['f'] = float(f)


    @classmethod
    def get(cls):
        a = float(input('a: '))
        b = float(input('b: '))
        c = float(input('c: '))
        d = float(input('d: '))
        e = float(input('e: '))
        f = float(input('f: '))
        return Equation(a, b, c, d, e, f)
