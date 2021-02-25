from conic import Conic

cnc = Conic(1, 2, 3, 4, 5, 6)

print(repr(cnc))
print(str(cnc))

#cnc.equation.coeffs['g'] = 7
print(cnc.equation)
