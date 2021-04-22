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
equation = conic.Equation.from_input()

determinant = conic.Conic.determinant(equation)
center = conic.Conic._get_center(equation, determinant)
if not center is None:
    equation = conic.Conic._translate(equation, center)
rotation_angle = conic.Conic._get_rotation_angle(equation)
if equation.b != 0:
    equation = conic.Conic._rotate(equation, rotation_angle)
print(conic.Conic._get_name(equation, center))
