from equation import Equation

test = Equation.get()
print(test)

test.coeff['j'] = 32
for i in test.coeff.keys():
    print(i, end=' ')
print()
print(test)
