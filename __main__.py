from conic import Conic, Equation


# equation = Equation(1, 0, 1, 0, 0, 1)      # nothing
# equation = Equation(1, 0, 1, 0, 0, 0)      # point
# equation = Equation(1, 0, 1, -2, -2, -2)   # circle
# equation = Equation(2, -1, 2, 0, 0, -30)   # ellipse
# equation = Equation(1, 12, -4, 0, 0, -30)  # hyperbola
# equation = Equation(1, 0, 0, 0, -1, 0)     # parabola
# equation = Equation(0, 0, 1, 0, 0, -1)     # parallel lines
# equation = Equation(1, 0, 0, 0, 0, 0)      # coincident lines
# equation = Equation(1, 0, -1, 0, 0, 0)     # intersecting lines
equation = Equation.frominput()

conic = Conic.identify(equation)

print(conic.name)
print(conic.center)
print(conic.rotation_angle)
print(conic.translated_equation)
print(conic.rotated_equation)
