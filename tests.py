"""
process.py
~~~~~~~~~~~~~~~

Contains test code for other files, along with non-critical code.

"""


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




