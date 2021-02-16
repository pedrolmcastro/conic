from equation import Equation

test = Equation('inf', '-inf', 'test', f='nan')
for i in test.coeff.values():
    print(i, end=' ')
print()

test = Equation.get()
for i in test.coeff.values():
    print(i, end=' ')
print()
