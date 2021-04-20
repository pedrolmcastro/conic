import math

class Real:
    '''Functions to get and parse finite floats.'''

    @staticmethod
    def get(message=''):
        '''Require inputs until a finite float is given. Warnings are printed for each invalid input'''
        while True:
            input_string = input(message)
            try:
                number = float(input_string)
            except:
                print(f"cannot convert to float: '{input_string}'. Try again!")
            else:
                if math.isfinite(number):
                    return number
                else:
                    print(f"input must be a finite float, not '{number}'. Try again!")

    @staticmethod
    def parse(value):
        '''Converts the given value to a finite float.'''
        number = float(value)
        if math.isfinite(number):
            return number
        else:
            raise ValueError(f"Real.parse() argument must be finite, not '{number}'")
