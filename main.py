from conic import Conic

cnc = Conic(1, 2, 3, 4, 5, 6)
print(cnc.equation)

while True:
    cnc = Conic.get()
    if cnc.isvalid():
        break
    print('\'a\', \'b\' and \'c\' cannot all equal to 0. Try again!')
print(cnc.equation)
