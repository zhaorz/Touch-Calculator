"""
vector.py
~~~~~~~~~~~~~~~


"""

import math
import testCanvas
import fileIO




# returns direction d from (x0, y0) to (x1, y1) with 0 <= d < 2pi
def direction((x0, y0), (x1, y1)):
    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
    if (x1 > x0 and y1 >= y0):      # first quadrant
        return math.atan((y1 - y0) / (x1 - x0))
    elif (x1 < x0 and y1 >= y0):    # second quadrant
        return math.pi - abs(math.atan((y1 - y0) / (x1 - x0)))
    elif (x1 < x0 and y1 < y0):     # third quadrant
        return math.pi + abs(math.atan((y1 - y0) / (x1 - x0)))
    elif (x1 > x0 and y1 < y0):     # fourth quadrant
        return math.pi * 2 - abs(math.atan((y1 - y0) / (x1 - x0)))
    elif (x1 == x0):                # vertically stacked
        sign = -1 if ((y1 - y0) < 0) else 1
        return sign * math.pi / 2
    else:
        return None # fail
        
def testDirection():
    print "Testing direction()... ",
    theta = 0
    while (theta < math.pi * 2):
        x0 = y0 = 0.0
        x1 = math.cos(theta)
        y1 = math.sin(theta)
        assert(almostEqual(direction((x0, y0), (x1, y1)), theta))
        theta += 0.1
    print "Passed!"


# from 15-112 hw1 starter code
# https://www.cs.cmu.edu/~112/notes/hw1.html
def almostEqual(d1, d2, epsilon=10**-3):
    return abs(d1 - d2) < epsilon

