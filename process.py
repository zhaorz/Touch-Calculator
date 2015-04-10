"""
process.py
~~~~~~~~~~~~~~~


"""

import math
import testCanvas
import fileIO


# returns direction d from (x0, y0) to (x1, y1) with 0 <= d < 2pi
def direction((x0, y0), (x1, y1)):
    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
    if (x1 > x0 and y1 >= y0):      # first quadrant
        return math.atan(abs(y1 - y0) / abs(x1 - x0))
    elif (x1 < x0 and y1 >= y0):    # second quadrant
        return math.atan(abs(y1 - y0) / abs(x1 - x0)) + math.pi / 2
    elif (x1 < x0 and y1 < y0):     # third quadrant
        return math.atan(abs(y1 - y0) / abs(x1 - x0)) + math.pi
    elif (x1 > x0 and y1 < y0):     # fourth quadrant
        return math.atan(abs(y1 - y0) / abs(x1 - x0)) + math.pi * 3 / 2
    elif (x1 == x0):                # vertically stacked
        sign = -1 if ((y1 - y0) < 0) else 1
        return sign * math.pi / 2
    else:
        return None # fails?
        










###################### normalize ###########################


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

# returns data of first character in dictionary of most recent file
# for testing
def loadFirstCharacter(directory="data"):
    allData = fileIO.openRecent(directory)
    firstDictionary = allData[0]
    firstKey = sorted(firstDictionary.keys())[0]
    return firstDictionary[firstKey]


# used for testing
def drawPoints(points):
    width = 600
    height = 600
    margin = 50
    window = testCanvas.TestWindow(
        width=width, height=height, margin=margin, points=points)
    window.run()























