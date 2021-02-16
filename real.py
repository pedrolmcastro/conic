import math

def get(msg=''):
    """
    Read a finite real number from input. If the input is not a number or not finite, an error message
    will be printed and another input will be required.

    Args:
        msg (str, optional): input message display.
    
    Returns:
        float: a valid finite number.
    """

    while True:
        inp = str(input(msg)).strip().replace(',', '.')
        try:
            inp = float(inp)
        except ValueError:
            print(f'[ERROR] \'{inp}\' is not a number! Try Again!')
        else:
            if math.isfinite(inp):
                return inp
            else:
                print(f'[ERROR] \'{inp}\' is not finite! Try again!')


def parse(arg):
    """
    Converts the given argument to a finite real number. If the argument is not a number or not finite, an
    error message will be printed and 0 will be returned.

    Args:
        arg (): Argument passed to be converted.
    
    Returns:
        float: the converted finite number or 0.0 if the argument is not valid or infinite.
    """

    try:
        arg = float(arg)
    except ValueError:
        print(f'[ERROR] \'{arg}\' is not a number! Using 0 instead!')
        return 0.0
    else:
        if math.isfinite(arg):
            return arg
        else:
            print(f'[ERROR] \'{arg}\' is not finite! Using 0 instead!')
            return 0.0
