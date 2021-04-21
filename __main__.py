from conic import Conic


# conic = Conic(1, 0, 1, 0, 0, 1)      # nothing
# conic = Conic(1, 0, 1, 0, 0, 0)      # point
# conic = Conic(1, 0, 1, -2, -2, -2)   # circle
# conic = Conic(2, -1, 2, 0, 0, -30)   # ellipse
# conic = Conic(1, 12, -4, 0, 0, -30)  # hyperbola
# conic = Conic(1, 0, 0, 0, -1, 0)     # parabola
# conic = Conic(0, 0, 1, 0, 0, -1)     # parallel lines
# conic = Conic(1, 0, 0, 0, 0, 0)      # coincident lines
# conic = Conic(1, 0, -1, 0, 0, 0)     # intersecting lines
conic = Conic.frominput()

conic.identify()
print(conic)
