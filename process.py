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

# Raw data -> vector feature
# output type: list [x, y, z, ... ]
def vectorFeature(points, dimensions):
    if (dimensions < 2):
        print "Must have at least 2 dimensions"
        return -1
    vectorStrokes = vectorizeCharacter(normalize(points))
    origin = [0.0 for _ in xrange(dimensions)]
    k = 0   # starting dimension is x
    for vectorStroke in vectorStrokes:
        for vector in vectorStroke:
            addVectorDimension(vector, origin, k)
        # shift to adjacent plane
        k = (k + 1) % dimensions
    return origin

def addVectorDimension(v, origin, k):
    """v and origin are vectors of arbitrary dimensions with origin having at
    least as many dimensions as v. k is the index in origin at which addition
    of v's components begin. A shift of one dimension to the right occurs
    after each addition, for all components of v."""
    if (len(v) > len(origin)):
        print "Error: v cannot have greater dimensionality than the origin."
        return -1
    for vIndex in xrange(len(v)):
        originIndex = (vIndex + k) % len(origin)
        origin[originIndex] += v[vIndex]
    return None

def testAddVectorDimension():
    print "Testing addVectorDimension()... ",
    origin = [0, 0, 0]
    addVectorDimension([1, 1], origin, 0)
    assert(origin == [1, 1, 0])
    addVectorDimension([1, 1], origin, 1)
    assert(origin == [1, 2, 1])
    addVectorDimension([-1, -2], origin, 2)
    assert(origin == [-1, 2, 0])
    assert(addVectorDimension([0, 0, 0, 0], origin, 1) == -1)
    print "Passed!"


def testVectorFeature():
    # output process3D for 7 characters
    # all 7 characters are A's
    print "Testing vectorFeature()... "
    allData = fileIO.read("testData/AAAAAAA.txt")
    data = allData[0]
    for key in data.keys():
        print vectorFeature(data[key], 3)
    print "Passed!"

def testVectorFeatureOnSet():
    # output vectorFeature() for 7 arbitrary characters
    print "Testing vectorFeature()... "
    allData = fileIO.openRecent("data")
    data = allData[0]   # only take first set
    for key in data.keys():
        print str(key) + ": " + str(vectorFeature(data[key], 3))
    print "Passed!"




###################################  vector ####################################


def vector(points):
    """vector([(x0, y0), (x1, y1), ... , (x(n), y(n))]) returns
    [[x1 - x0, y1 - y0], ... , (x(n) - x(n-1), y(n) - y(n-1)]]
    theta is the angle between two adjacent points.
    Input is a list of (x, y, timestamp) tuples."""
    vectors = []
    for i in xrange(len(points) - 1):
        (x0, y0) = points[    i][:2]
        (x1, y1) = points[i + 1][:2]
        vectors.append([x1 - x0, y1 - y0])
    return vectors

def magnitude((x0, y0), (x1, y1)):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def trimPoints(points, epsilon=0.02):
    """Input is a normalized list of points that form one stroke.
    Returns a list with points that are within epsilon distance from their
    preceeding points removed."""
    if (points == []):
        return []
    trimmedPoints = [points[0]]     # start with first point
    prev = 0
    for nxt in xrange(1, len(points)):
        (x0, y0) = points[prev][:2]
        (x1, y1) = points[ nxt][:2]
        # points are sufficiently separated: add point and update prev
        if (magnitude((x0, y0), (x1, y1)) > epsilon):
            trimmedPoints.append(points[nxt][:2])
            prev = nxt
    return trimmedPoints


def testTrimPoints():
    print "Testing trimPoints()... ",
    points = fileIO.read("testData/AAAAAAA.txt")[0]['A']
    trimmed = trimPoints(points)
    print trimmed
    print "Initial length", len(points), "Final length:", len(trimmed)
    testCanvas.TestWindowPoints(trimmed).run()





def length(v):
    """Length of a vector in form [x, y, ... , z]."""
    return (sum(a ** 2 for a in v)) ** 0.5

def testLength():
    print "Testing length()... ",
    assert(almostEqual(length([1,1,1]), (3)**0.5))
    assert(almostEqual(length([2,2,2]), (12)**0.5))
    print "Passed!"

def dotProduct(v1, v2):
    """Sum product for the components of v1 and v2. v1 and v2 should have 
    same dimensions."""
    if (len(v1) != len(v2)):
        return None
    return sum(a * b for a,b in zip(v1, v2))

def testDotProduct():
    print "Testing dotProduct()... ",
    assert(dotProduct([3,4,5],[2,1,2]) == 6 + 4 + 10)
    assert(dotProduct([0,0,0],[2,1,2]) == 0)
    print "Passed!"

def angle(v1, v2):
    """Angle between two vectors of the same dimensions. Return value is between
    0 and pi"""
    try:
        return math.acos(dotProduct(v1, v2) / (length(v1) * length(v2)))
    except:     # if one of the vectors has length 0
        return 0.0

def testAngle():
    print "Testing angle()... ",
    assert(almostEqual(angle([1,0],[0,1]), math.pi / 2))
    assert(almostEqual(angle([1,0],[1,0]), 0.0))
    assert(almostEqual(angle([1,0],[-1,0]), math.pi))
    assert(almostEqual(angle([1,0],[0,0]), 0.0))
    print "Passed!"




def vectorizeCharacter(points):
    strokes = splitToStrokes(points)
    vectors = []
    for stroke in strokes:
        trimmedStroke = trimPoints(stroke)
        vectors.append(vector(trimmedStroke))
    return vectors


def vectorSplitStroke(stroke, n=4, epsilon=math.pi/3):
    """Stroke is a list of [x, y] vector tuples. Returns a list that contains
    the original stroke split at its maximum angle point, if the maximum
    angle exceeds epsilon. Default is 60 degrees. n is the number of vectors
    between 2 observation points."""

    theta = []
    for i in xrange(1, len(stroke) - n):
        theta.append(angle(stroke[i], stroke[i + n]))
    maxAngle = max(theta)
    if (maxAngle > epsilon):
        # indecies in theta correspond to index + n / 2 in stroke
        splitIndex = theta.index(maxAngle) + n / 2
        return splitStroke(stroke, splitIndex)
    else:
        return [stroke]

def splitStroke(stroke, i):
    """Returns a list containing the stroke split at index i."""
    return [stroke[:i], stroke[i:]]

def testSplitStroke():
    print "Testing splitStroke()... ",
    assert(splitStroke([0,1,2,3,4,5], 3) == [[0,1,2],[3,4,5]])
    print "Passed!"


def testVectorSplitStroke():
    allData = fileIO.read("testData/AAAAAAA.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        vectorStrokes = vectorizeCharacter(charData)
        splitStrokes = []
        for stroke in vectorStrokes:
            splitStrokes.extend(vectorSplitStroke(stroke))
        print key, len(splitStrokes)
    





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
    width = 1.0 if width == 0.0 else width
    height = 1.0 if height == 0.0 else height
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























