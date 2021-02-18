from equation import Equation

class Conic:
    """
    A conic representation.
    
    Attributes:
        eqt (Equation): general form equation.
        center (Point/inf/None/str): number of centers the conic has and its coordinates if unique.
        name (str): one of ['unknown', 'Empty', 'Point', 'Intersecting lines', 'Parallel lines',
                            'Coincident lines', 'Circumference', 'Ellipse', 'Hyperbole', 'Parable'].
    """
    def __init__(self, eqt=None):
        if eqt is None:
            self.eqt = Equation()
        elif isinstance(eqt, Equation):
            self.eqt = eqt
        else:
            raise TypeError(f'equation must be of class Equation or None, not {type(eqt)}')
        self.center = 'unknown'
        self.name = 'unknown'

    @classmethod
    def get(cls):
        eqt = Equation.get()
        return cls(eqt)

    def getNewEquation(self):
        self.eqt = Equation.get()
        self.center = 'unknown'
        self.name = 'unknown'
    
    def isvalid(self):
        if self.eqt.coeffs.keys() == {'a', 'b', 'c', 'd', 'e', 'f'}:
            if self.eqt.coeffs['a'] != 0 or self.eqt.coeffs['b'] != 0 or self.eqt.coeffs['c'] != 0:
                return True
        return False
