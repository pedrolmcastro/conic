from conic import Conic

#cnc = Conic(0, 0, 1, 0, 0, 2)
#cnc = Conic(1, 0, 0, 0, -1, 0)
cnc = Conic(1, 0, 1, -2, -2, -2)

cnc.identify()
print(cnc.center)
print(cnc.equation)
