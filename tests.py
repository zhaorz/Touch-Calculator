"""
tests.py
~~~~~~~~~~~~~~~
Contains test code for other files, along with non-critical code.

"""


# Packaged libraries
import fileIO


###################################
# knn.py
###################################


import knn


# from 15-112 hw1 starter code
# https://www.cs.cmu.edu/~112/notes/hw1.html
def almostEqual(d1, d2, epsilon=10**-3):
    return abs(d1 - d2) < epsilon

def testEuclideanDistance():
    print "Testing euclideanDistance()... ",
    a = [0, 0, 0]
    b = [1, 1, 1]
    n = 3
    assert(almostEqual(knn.euclideanDistance(a, b, n), (1 + 1 + 1) ** 0.5))
    print "Passed!"

def testKNearestNeighbors():
    print "Testing kNearestNeighbors()... ",
    neighbors = [('A', 1.5), ('B', 6.0), ('C', 5.0), ('D', 3.3)]
    assert(knn.kNearestNeighbors(neighbors, 2) == [('A', 1.5), ('D', 3.3)])
    print "Passed!"

def testVote():
    print "Testing vote()... ",
    neighbors = [
        ('A', 1), ('A', 1), ('A', 1), ('A', 1), ('A', 1), ('A', 1), ('A', 1),
        ('B', 1), ('B', 1), ('B', 1), ('B', 1),
        ('C', 1)
        ]
    votes = knn.vote(neighbors)
    assert(almostEqual(votes['A'], float(7) / 12))
    assert(almostEqual(votes['B'], float(4) / 12))
    assert(almostEqual(votes['C'], float(1) / 12))
    print "Passed!"

def testTopNClasses():
    print "Testing topNClasses()... ",
    votes = {
        'A': 0.6,
        'B': 0.3,
        'C': 0.05,
        'D': 0.025,
        'E': 0.015,
        'F': 0.007,
        'G': 0.003
        }
    assert(knn.topNClasses(votes, 4) == [('A', 0.6), ('B', 0.3), 
                                    ('C', 0.05), ('D', 0.025)])
    print "Passed!"


def testKNN():
    print "Testing knn.py... "
    testEuclideanDistance()
    testKNearestNeighbors()
    testVote()
    testTopNClasses()
    print "Passed!"



###################################
# process.py
###################################


import process


def testFeature():
    print "Testing Feature()... "
    processor = Feature()
    print "Testing 7 A's..."
    allData = fileIO.read("testData/AAAAAAA.txt")
    data = allData[0]
    for key in data.keys():
        processor.update(data[key])
        print processor.vFeature
    print "Testing most recent data..."
    allData = fileIO.openRecent("data")
    data = allData[0]   # only take first set
    for key in data.keys():
        processor.update(data[key])
        print str(key) + ": " + str(processor.vFeature)
    print "Passed!"

def testAddVectorDimension():
    print "Testing addVectorDimension()... ",
    processor = Feature()
    origin = [0, 0, 0]
    processor.addVectorDimension([1, 1], origin, 0)
    assert(origin == [1, 1, 0])
    processor.addVectorDimension([1, 1], origin, 1)
    assert(origin == [1, 2, 1])
    processor.addVectorDimension([-1, -2], origin, 2)
    assert(origin == [-1, 2, 0])
    assert(processor.addVectorDimension([0, 0, 0, 0], origin, 1) == -1)
    print "Passed!"

def testTrimPoints():
    print "Testing trimPoints()... "
    processor = Feature()
    points = fileIO.read("testData/AAAAAAA.txt")[0]['A']
    trimmed = processor.trimPoints(points)
    print "Initial length", len(points), "Final length:", len(trimmed)
    #testCanvas.TestWindowPoints(trimmed).run()

def testSplitList():
    print "Testing splitList()... ",
    processor = Feature()
    assert(processor.splitList([0,1,2,3,4,5], 3) == [[0,1,2],[3,4,5]])
    assert(processor.splitList([],1) == [[],[]])
    print "Passed!"


def testVectorSplitStroke():
    processor = Feature()
    allData = fileIO.read("testData/AAAAAAA.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalize(charData)
        rawStrokes = processor.primativeSplit(normalizedPoints)
        trimmedStrokes = [processor.trimPoints(stroke) for stroke in rawStrokes]
        vectorStrokes = [processor.vector(stroke) for stroke in trimmedStrokes]
        vectorSplit = processor.vectorSplitCharacter(vectorStrokes)
        print key + ": " + str(len(vectorSplit))


def testLength():
    print "Testing length()... ",
    assert(almostEqual(process.length([1,1,1]), (3)**0.5))
    assert(almostEqual(process.length([2,2,2]), (12)**0.5))
    print "Passed!"

def testDotProduct():
    print "Testing dotProduct()... ",
    assert(process.dotProduct([3,4,5],[2,1,2]) == 6 + 4 + 10)
    assert(process.dotProduct([0,0,0],[2,1,2]) == 0)
    print "Passed!"

def testAngle():
    print "Testing angle()... ",
    assert(almostEqual(process.angle([1,0],[0,1]), math.pi / 2))
    assert(almostEqual(process.angle([1,0],[1,0]), 0.0))
    assert(almostEqual(process.angle([1,0],[-1,0]), math.pi))
    assert(almostEqual(process.angle([1,0],[0,0]), 0.0))
    print "Passed!"

def testCurvatureFeature():
    print "Testing curvatureFeature()... "
    processor = process.Feature()
    print "Testing straight lines..."
    allData = fileIO.read("testData/straightLines.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        rawStrokes = processor.primativeSplit(normalizedPoints)
        trimmedStrokes = [processor.trimPoints(stroke) for stroke in rawStrokes]
        vectorStrokes = [processor.vector(stroke) for stroke in trimmedStrokes]
        vectorSplit = processor.vectorSplitCharacter(vectorStrokes)
        print "    " + key + ": " + str(processor.curvatureFeature(vectorSplit))
    print "Testing ABCDEF7..."
    allData = fileIO.read("testData/ABCDEF7.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        rawStrokes = processor.primativeSplit(normalizedPoints)
        trimmedStrokes = [processor.trimPoints(stroke) for stroke in rawStrokes]
        vectorStrokes = [processor.vector(stroke) for stroke in trimmedStrokes]
        vectorSplit = processor.vectorSplitCharacter(vectorStrokes)
        print "    " + key + ": " + str(processor.curvatureFeature(vectorSplit))
    print "Testing 0U32896..."
    allData = fileIO.read("testData/0U32896.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        rawStrokes = processor.primativeSplit(normalizedPoints)
        trimmedStrokes = [processor.trimPoints(stroke) for stroke in rawStrokes]
        vectorStrokes = [processor.vector(stroke) for stroke in trimmedStrokes]
        vectorSplit = processor.vectorSplitCharacter(vectorStrokes)
        print "    " + key + ": " + str(processor.curvatureFeature(vectorSplit))

def testStartEndPoint():
    print "Testing startPointFeature() and endPointFeature()... "
    processor = process.Feature()
    print "Testing straight lines... "
    allData = fileIO.read("testData/straightLines.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        startPointFeature = processor.findStartPoint(normalizedPoints)
        endPointFeature = processor.findEndPoint(normalizedPoints)
        print ("    "  + key + " - Start: " + str(startPointFeature) + 
                                 " End: " + str(endPointFeature))
    print "Testing ABCDEF7..."
    allData = fileIO.read("testData/ABCDEF7.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        startPointFeature = processor.findStartPoint(normalizedPoints)
        endPointFeature = processor.findEndPoint(normalizedPoints)
        print ("    "  + key + " - Start: " + str(startPointFeature) + 
                                 " End: " + str(endPointFeature))

def testNumStrokesFeature():
    print "Testing numStrokes()... "
    processor = process.Feature()
    print "Testing lines..."
    allData = fileIO.read("testData/straightLines.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        rawStrokes = processor.primativeSplit(normalizedPoints)
        numStrokes = processor.numStrokes(rawStrokes)
        print "    " + key + " numStrokes: " + str(numStrokes)
    print "Testing ABCDEF7..."
    allData = fileIO.read("testData/ABCDEF7.txt")
    d = allData[0]
    for key in d.keys():
        charData = d[key]
        normalizedPoints = processor.normalizePoints(charData)
        rawStrokes = processor.primativeSplit(normalizedPoints)
        numStrokes = processor.numStrokes(rawStrokes)
        print "    " + key + " numStrokes: " + str(numStrokes)
