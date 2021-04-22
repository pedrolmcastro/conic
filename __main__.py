import conic


# equation = conic.Equation(1, 0, 1, 0, 0, 1)      # nothing
# equation = conic.Equation(1, 0, 1, 0, 0, 0)      # point
# equation = conic.Equation(1, 0, 1, -2, -2, -2)   # circle
# equation = conic.Equation(2, -1, 2, 0, 0, -30)   # ellipse
# equation = conic.Equation(1, 12, -4, 0, 0, -30)  # hyperbola
# equation = conic.Equation(1, 0, 0, 0, -1, 0)     # parabola
# equation = conic.Equation(0, 0, 1, 0, 0, -1)     # parallel lines
# equation = conic.Equation(1, 0, 0, 0, 0, 0)      # coincident lines
# equation = conic.Equation(1, 0, -1, 0, 0, 0)     # intersecting lines
equation = conic.Equation.frominput()

name, center, rotation_angle, translated_equation, rotated_equation = conic.Conic.identify(equation)

print(name)
print(center)
print(rotation_angle)
print(translated_equation)
print(rotated_equation)
