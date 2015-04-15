"""
process.py
~~~~~~~~~~~~~~~


"""

import math
import testCanvas
import fileIO


#############################  feature creation ################################
"""
Raw data --> strokes --> vector strokes --> 3D vector addition --> [x, y, z]
Raw data enters as a list of (x, y, timestamp) elements
Output is a list of 3 elements, the endpoint of the vector sum of the character.
Dimensions are handled by shifting 1 dimension for each stroke, and adding the
x and y data to those two dimensions in the 3D output.
"""

def process3D(points):
    vectorStrokes = vectorizeCharacter(normalize(points))
    origin = [0.0, 0.0, 0.0]
    numDimensions = 3       # x, y, and z
    d1, d2 = 0, 1           # start at x and y
    for vectorStroke in vectorStrokes:
        for vector in vectorStroke:
            dx, dy = vector
            origin[d1] += dx
            origin[d2] += dy
        # shift to adjacent plane
        d1 = (d1 + 1) % numDimensions
        d2 = (d2 + 1) % numDimensions
    return origin

def testProcess3D():
    # output process3D for 7 characters
    # all 7 characters are A's
    print "Testing process3D()... "
    allData = fileIO.read("testData/christian.txt")
    data = allData[0]
    for key in data.keys():
        print process3D(data[key])
    print "Passed!"

def testProcess3DOnSet():
    # output process3D for 7 arbitrary characters
    print "Testing process3D()... "
    allData = fileIO.openRecent("data")
    data = allData[0]   # only take first set
    for key in data.keys():
        print str(key) + ": " + str(process3D(data[key]))
    print "Passed!"




###################################  vector ####################################


# Converts list of points to list of distances between consecutive points
# input is a list of (x, y, timestamp) tuples
# i.e.  [(x0, y0), (x1, y1), ... , (x(n), y(n))] --> 
#       [(x1 - x0, y1 - y0), ... , (x(n) - x(n-1), y(n) - y(n-1))]
def vector(points):
    vectors = []
    for i in xrange(len(points) - 1):
        (x0, y0) = points[    i][:2]
        (x1, y1) = points[i + 1][:2]
        vectors.append((x1 - x0, y1 - y0))
    return vectors

def vectorizeCharacter(points):
    strokes = splitToStrokes(points)
    vectors = []
    for stroke in strokes:
        vectors += [vector(stroke)]
    return vectors

# 2D sum of a list of vectors
def vectorSum(origin, vectors):
    for (x, y) in vectors:
        origin[0] += x
        origin[1] += y
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
        assert(almostEqual(vectorEndPoint[0], strokeEndPoint[0], 0.000001))
        assert(almostEqual(vectorEndPoint[1], strokeEndPoint[1], 0.000001))
    print "Passed!"


############################## stroke separation ###############################


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

# from 15-112 hw1 starter code
# https://www.cs.cmu.edu/~112/notes/hw1.html
def almostEqual(d1, d2, epsilon=10**-3):
    return abs(d1 - d2) < epsilon


################################## normalize ##################################


# takes array of points and maps it to a 1.0 by 1.0 space
def normalize(points):
    if (points == []):
        return points
    ((minX, minY), (maxX, maxY)) = findCorners(points)
    width = maxX - minX
    height = maxY - minY
    normalizedPoints = []
    for i in xrange(len(points)):
        (x, y, time) = points[i]
        x -= minX
        y -= minY
        x *= 1.0 / width
        y *= 1.0 / height
        normalizedPoints.append((x, y, time))
    return normalizedPoints

# finds bottom left and top right corners of a list of points
def findCorners(points):
    minX = minY = maxX = maxY = None
    for (x, y, time) in points:
        if (minX == None or x < minX):
            minX = x
        if (maxX == None or x > maxX):
            maxX = x
        if (minY == None or y < minY):
            minY = y
        if (maxY == None or y > maxY):
            maxY = y
    return ((minX, minY), (maxX, maxY))

# returns data of the given character in dictionary of most recent file
# for testing
def loadCharacter(char=None, directory="data"):
    allData = fileIO.openRecent(directory)
    firstDictionary = allData[0]
    if (char == None):      # no key given, just return first element
        firstKey = sorted(firstDictionary.keys())[0]
        return firstDictionary[firstKey]
    elif (char in firstDictionary.keys()):        # data exists
        return firstDictionary[char]


# used for testing
def drawPoints(points):
    width = 600
    height = 600
    margin = 50
    window = testCanvas.TestWindow(
        width=width, height=height, margin=margin, points=points)
    window.run()























