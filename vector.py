"""
vector.py
~~~~~~~~~~~~~~~


"""

import math
import testCanvas
import fileIO




# 2D vector sum, origin is a list [x, y]
def vectorSum(origin, vectors):
    for (magnitude, direction) in vectors:
        dx = magnitude * math.cos(direction)
        dy = magnitude * math.sin(direction)
        origin[0] += dx
        origin[1] += dy
    return origin

# Data consists of single strokes
# test that the vector sum is the same as endpoint - startpoint
def testVectorSum():
    print "Testing vectorSum()... ",
    allData = fileIO.read("testData/vectorSumTestData.txt")
    data = allData[0]   # first dictionary
    for key in data.keys():
        strokes = splitToStrokes(data[key])
        vectorStrokes = vectorizeCharacter(data[key])
        # only use one stroke
        stroke = strokes[0]
        vector = vectorStrokes[0]
        start = stroke[0]
        end = stroke[-1]
        vectorEndPoint = vectorSum([0.0, 0.0], vector)
        strokeEndPoint = [end[0] - start[0], end[1] - start[1]]
        print vectorEndPoint, strokeEndPoint
    print "Passed!"



def vectorizeCharacter(points):
    strokes = splitToStrokes(points)
    vectors = []
    for stroke in strokes:
        vectors += [vector(stroke)]
    return vectors

# input is a list of (x, y, timestamp) tuples
def vector(points):
    vectors = []
    for i in xrange(len(points) - 1):
        (x0, y0) = points[    i][:2]
        (x1, y1) = points[i + 1][:2]
        vectors.append((distance((x0, y0), (x1, y1)),
                       direction((x0, y0), (x1, y1))))
    return vectors

def distance((x0, y0), (x1, y1)):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

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

# Take an array containing raw data of touch points and split
# into individual strokes (in order). Returns a 2D array consiting
# of the strokes, where each stroke contains touch points.
# points is a tuple (x, y, timestamp)
def splitToStrokes(points):
    if (points == []):
        return [[]]
    strokes = []
    newStroke = []
    for i in xrange(len(points)):
        # begin a new stroke
        if (newStroke == []):
            newStroke.append(points[i])
        # previous point belongs to same stroke
        elif (isSameStroke(newStroke[-1], points[i]) == True):
            newStroke.append(points[i])      # only include x and y
        # start a new stroke
        else:
            strokes.append(newStroke)
            newStroke = [points[i]]
    if (newStroke != []):   # add last stroke if necessary
        strokes.append(newStroke)
    return strokes

# True if the two datapoints belong on the same stroke, False otherwise
def isSameStroke((x1, y1, timestamp1), (x2, y2, timestamp2)):
    epsilon = 0.08
    if (abs(timestamp1 - timestamp2) > epsilon):
        return False
    else:
        return True


def testSplitToStrokes():
    print "Testing splitToStrokes()... ",
    # This file only contains one dictionary with 7 keys
    allData = fileIO.read("testData/ABCDEF7.txt")
    firstDictionary = allData[0]
    strokes = {"A": 2, "B": 2, "C": 1, "D": 2, "E": 4, "F": 3, "7": 1}
    for char in strokes.keys():
        charData = firstDictionary[char]
        strokeData = splitToStrokes(charData)
        assert(len(strokeData) == strokes[char])
    print "Passed!"

