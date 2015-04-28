"""
mathParser.py
~~~~~~~~~~~~~~~


WolframAlpha AppID: RAJVVX-8GEGHXV5LU

"""


import math


evalCharDictionary = {
    '':'',
    'A':'A', 'B':'B', 'C':'C', 'D':'D', 'E':'E', 'F':'F',
    '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
    '6':'6', '7':'7', '8':'8', '9':'9',

    '*':'*', '+':'+', '/':'/',  '-':'-', '(':'(', ')':')', '^':'**(',
    
    # division      # mult          # pi
    u'\u00f7':'/', u'\u00d7':'*', u'\u03c0':' math.pi ', 'e':' math.e ',
    # sqrt
    u'\u221a':' math.sqrt(', '%':'%', '.':'.',

    'sin':' math.sin(', 'cos':' math.cos(', 'tan':' math.tan(',
    'asin':' math.asin(', 'acos':' math.acos(', 'atan':' math.atan(',

    'ln':' math.log(', 'log':' math.log10('

}

displayCharDictionary = {
    '':'',
    'A':'A', 'B':'B', 'C':'C', 'D':'D', 'E':'E', 'F':'F',
    '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
    '6':'6', '7':'7', '8':'8', '9':'9',
    '*':u'\u00d7', '+':'+', '/':'/',  '-':'-', '(':'(', ')':')', '^':'^(',
    # division      # mult          # pi
    u'\u00f7':u'\u00f7', u'\u00d7':u'\u00d7', u'\u03c0':u'\u03c0', 'e':'e',
    # sqrt
    u'\u221a': u'\u221a(', '%':'%', '.':'.',

    'sin':'sin(', 'cos':'cos(', 'tan':'tan(',
    'asin':'asin(', 'acos':'acos(', 'atan':'atan(',

    'ln':'ln(', 'log':'log('

}


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















