from conic import Conic

cnc = Conic(1, 0, 1, -2, -2, -2)

cnc.findCenter()
print(cnc.center)

cnc.translate()
print(cnc.equation)
