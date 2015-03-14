"""
featureDetection.py
~~~~~~~~~~~~~~~


"""

import math


################################################################################


# stroke is a list of tuples (x, y, timestamp)
# returns a list where the first element is the stroke origin (x0, y0)
# and the rest of the list consists of tuples (magnitude, direction)
# where direction is in radians
def vectorizeStroke(stroke):
    if (stroke == []):
        return []
    vectors = [stroke[0][:2]]   # Only take first 2 values (x0, y0)
    for i in xrange(1, len(stroke)):
        mag = magnitude(stroke[i - 1][:2], stroke[i][:2])
        dirc = direction(stroke[i - 1][:2], stroke[i][:2])
        vectors.append((mag, dirc))
    return vectors

def magnitude((x0, y0), (x1, y1)):
    return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

def direction((x0, y0), (x1, y1)):
    dx = x1 - x0
    dy = y1 - y0
    if (dx == 0.0):
        sign = -1 if ((y1 - y0) < 0) else 1
        return sign * math.pi / 2
    else:
        return math.atan(dy / dx)


################################################################################


# Take an array containing raw data of touch points and split
# into individual strokes (in order). Returns a 2D array consiting
# of the strokes, where each stroke contains touch points.
# touchData is a tuple (x, y, timestamp)
def splitToStrokes(touchData):
    n = len(touchData)
    if (n == 0):
        return [[]]
    strokes = []
    newStroke = []
    for i in xrange(n):
        # Begin stroke
        if (newStroke == []):
            newStroke.append(touchData[i])
        # Test if same stroke
        elif (isSameStroke(newStroke[-1], touchData[i]) == True):
            newStroke.append(touchData[i])
        # New stroke started
        else:
            strokes.append(newStroke)
            newStroke = [touchData[i]]
    if (newStroke != []):
        strokes.append(newStroke)
    finalStrokes = removeTimestamp(strokes)
    return strokes


# True if the two datapoints belong on the same stroke, False otherwise
def isSameStroke((x1, y1, timestamp1), (x2, y2, timestamp2)):
    epsilon = 0.1
    if (abs(timestamp1 - timestamp2) > epsilon):
        return False
    else:
        return True

def removeTimestamp(strokes):
    newStrokes = []
    for stroke in strokes:
        newStroke = []
        for (x, y, timestamp) in stroke:
            newStroke.append((x, y))
        newStrokes.append(newStroke)
    return newStrokes


################################################################################













