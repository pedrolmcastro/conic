import math

def get(msg=''):
    """
    Reads a finite real number from input. If the input is not a number or is not finite, a message
    will be printed and another input will be required.

    Args:
        msg (str, optional): input message display.
    
    Returns:
        float: finite number.
    """
    while True:
        inp = str(input(msg)).strip().replace(',', '.')
        try:
            inp = float(inp)
        except ValueError:
            print(f'cannot convert string to real: \'{inp}\'. Try again!')
        else:
            if math.isfinite(inp):
                return inp
            else:
                print(f'input must be a finite number, not \'{inp}\'. Try again!')


def parse(val):
    """
    Converts the given value to a finite real number.

    Args:
        val (int/float/str): value to be converted.
    
    Returns:
        float: converted finite number.
    
    Raises:
        ValueError: if the string cannot be converted or the argument is not finite.
        TypeError: if the argument is not an int, float or str.
    """
    try:
        val = float(val)
    except ValueError:
        raise ValueError(f'could not convert string to real: \'{val}\'')
    except TypeError:
        raise TypeError(f'real.parse() argument must be a string or a number, not {type(val)}')
    else:
        if math.isfinite(val):
            return val
        else:
            raise ValueError(f'real.parse() argument must be a finite number, not \'{val}\'')
