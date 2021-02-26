import math

from conic import Conic

#cnc = Conic(0, 0, 1, 0, 0, 2) #parallel lines
#cnc = Conic(1, 0, 0, 0, -1, 0) #parabola
#cnc = Conic(1, 0, 1, -2, -2, -2) #circle
#cnc = Conic(2, -1, 2, 0, 0, -30) #ellipse
cnc = Conic(1, 12, -4, 0, 0, -30) #hyperbola

cnc.identify()
print(math.degrees(cnc.angle))
print(cnc.equation)
