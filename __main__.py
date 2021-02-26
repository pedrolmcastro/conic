from conic import Conic
from equation import Equation

#cnc = Conic(0, 0, 1, 0, 0, 2)
#cnc = Conic(1, 0, 0, 0, -1, 0)
#cnc = Conic(1, 0, 1, -2, -2, -2)

eqt = Equation.frominput()
cnc = Conic.fromequation(eqt)

cnc.identify()
print(cnc.center)
print(cnc.equation)
