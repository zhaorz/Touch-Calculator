"""
evaluate.py
~~~~~~~~~~~~~~~
Handles behavior of math string input and evaluation.

Contains two dictionaries. Each maps a result char (from an input source) to
either a display or eval string. This dictionaries are global, but they are only
accessed by displayChar() and evalChar().

The primary function is evaluate(), which attempts to evaluate a list of
legal evalChars, and returns a list corresponding to the result. If exceptions
are raised during evaluation, strings describing the error are returned.

"""


# Standard libraries
import math


# from 15-112 hw1 starter code
# https://www.cs.cmu.edu/~112/notes/hw1.html
def almostEqual(d1, d2, epsilon=10**-3):
    return abs(d1 - d2) < epsilon


# Maps raw input to evaluable strings
evalCharDictionary = {
    '':'',
    'A':'A', 'B':'B', 'C':'C', 'D':'D', 'E':'E', 'F':'F',
    '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
    '6':'6', '7':'7', '8':'8', '9':'9',

    '*':' * ', '+':' + ', '/':' / ',  '-':' - ', '(':' ( ', ')':' ) ',
    '^':' **( ',
    
    # division      # mult          # pi
    u'\u00f7':' / ', u'\u00d7':' * ', u'\u03c0':' math.pi ', 'e':' math.e ',
    # sqrt
    u'\u221a':' math.sqrt( ', '%':' % ', '.':'.',

    'sin':' math.sin( ', 'cos':' math.cos( ', 'tan':' math.tan( ',
    'asin':' math.asin( ', 'acos':' math.acos( ', 'atan':' math.atan( ',

    'ln':' math.log( ', 'log':' math.log10( '

}

# Maps raw input to visual display strings
displayCharDictionary = {
    '':'',
    'A':'A', 'B':'B', 'C':'C', 'D':'D', 'E':'E', 'F':'F',
    '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
    '6':'6', '7':'7', '8':'8', '9':'9',
    '*':u'\u00d7', '+':'+', '/':'/',  '-':'-', '(':'(', ')':')', '^':'^(',
    # division              # mult              # pi
    u'\u00f7':u'\u00f7', u'\u00d7':u'\u00d7', u'\u03c0':u'\u03c0', 'e':'e',
    # sqrt
    u'\u221a': u'\u221a(', '%':'%', '.':'.',

    'sin':'sin(', 'cos':'cos(', 'tan':'tan(',
    'asin':'asin(', 'acos':'acos(', 'atan':'atan(',

    'ln':'ln(', 'log':'log('

}


def evaluate(evalList):
    """Evaluates a list of evalChars.

    Args:
        evalList (list): A list of legal evalChars.

    Returns:
        str: the value that evalList evaluates to.

    """
    evalString = "".join(evalList)
    terms = evalString.split(' ')
    floatList = toFloat(terms)
    try:
        result = str(eval("".join(floatList)))
    except ZeroDivisionError:
        return "Divide by Zero Error"
    except ValueError:
        return "Value Error"
    except SyntaxError:
        return "Syntax Error"
    except:
        return "Error"
    # Convert to int if the float is whole
    if (almostEqual(eval(result), round(eval(result)), 0.000001)):
        result = str(int(round(eval(result))))
    if len(result) > 14:
        result = "Overflow Error"
    return result

def testEvaluate():
    print "Testing evaluate()... ",
    assert(evaluate(['1',' + ','1']) == '2')
    assert(evaluate(['1',' / ','2']) == str(1.0 / 2))
    assert(evaluate(['5','8',' / ','4']) == str(58.0/4))
    print "Passed!"

def toFloat(evalList):
    """Convert numerical string elements of input list to float strings.

    Args:
        evalList (list): A list of legal string evalChars.

    Returns:
        list: The same list of strings with any integers now as floats.

    """
    result = []
    for char in evalList:
        if (char.isdigit()):
            result.append(char + '.0')
        else:
            result.append(char)
    return result

def testToFloat():
    print "Testing toFloat()... ",
    assert(toFloat([]) == [])
    assert(toFloat(['123']) == ['123.0'])
    assert(toFloat(['123','456']) == ['123.0', '456.0'])
    assert(toFloat([' math.pi ',' ln(','1']) == [' math.pi ',' ln(','1.0'])
    print "Passed!"


def evalChar(value):
    """Converts raw strings to evaluable ones.

    Args:
        value (str, unicode): The raw representation.

    Returns:
        str: The str that evaluates to the desired value or method.

    """
    return evalCharDictionary[value]

def displayChar(value):
    """Converts raw input string to display string.

    Args:
        value (str, unicode): The raw representation.

    Returns:
        str: The appropriate display string.

    """
    return displayCharDictionary[value]


