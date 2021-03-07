from conic import Conic

cnc = Conic.frominput()

#cnc = Conic(1, 0, 1, 0, 0, 1) #nothing
#cnc = Conic(1, 0, 1, 0, 0, 0) #point
#cnc = Conic(1, 0, 1, -2, -2, -2) #circle
#cnc = Conic(2, -1, 2, 0, 0, -30) #ellipse
#cnc = Conic(1, 12, -4, 0, 0, -30) #hyperbola
#cnc = Conic(1, 0, 0, 0, -1, 0) #parabola
#cnc = Conic(0, 0, 1, 0, 0, -1) #parallel lines
#cnc = Conic(1, 0, 0, 0, 0, 0) #coincident lines
#cnc = Conic(1, 0, -1, 0, 0, 0) #intersecting lines

cnc.identify()
print(cnc)
