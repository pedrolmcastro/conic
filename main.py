from conic import Conic

cnc = Conic.get()
while not cnc.isvalid():
    print(f'\'a\', \'b\' and \'c\' cannot all equal to 0. Try again!')
    cnc.getNewEquation()

print(cnc.eqt)
