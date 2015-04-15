"""
knn.py
~~~~~~~~~~~~~~~

Kth Nearest Neighbors

"""


def euclideanDistance(a, b, n):
    """Computes length of line segment connecting 2 n-dimensional points. 
    Each point is a list of at least length n."""
    d = sum((a[i] - b[i]) ** 2 for i in xrange(n))
    return d ** 0.5

def testEuclideanDistance():
    print "Testing euclideanDistance()... ",
    a = [0, 0, 0]
    b = [1, 1, 1]
    n = 3
    assert(almostEqual(euclideanDistance(a, b, n), (1 + 1 + 1) ** 0.5))
    print "Passed!"

# from 15-112 hw1 starter code
# https://www.cs.cmu.edu/~112/notes/hw1.html
def almostEqual(d1, d2, epsilon=10**-3):
    return abs(d1 - d2) < epsilon


def allNeighbors(model, instance, n):
    """Returns a list of (sym, distance) tuples of the model set, where
    n is the dimenstionality of the instance used to calculate distance and
    sym is the classification of the model data.
    The model should be a list of tuples (sym, data)."""
    neighbors = []
    for (sym, data) in model:
        distance = euclideanDistance(instance, data, n)
        neighbors.append((sym, distance))
    return neighbors

def kNearestNeighbors(neighbors, k):
    """Returns a list of the k neighbors with the least distance. Each element
    in neighbors is a (sym, distance) tuple."""

    # sort by comparing each tuple's distance (index = 1)
    sortedNeighbors = sorted(neighbors, lambda a, b: cmp(a[1], b[1]))
    return sortedNeighbors[:k]


def testKNearestNeighbors():
    print "Testing kNearestNeighbors()... ",
    neighbors = [('A', 1.5), ('B', 6.0), ('C', 5.0), ('D', 3.3)]
    assert(kNearestNeighbors(neighbors, 2) == [('A', 1.5), ('D', 3.3)])
    print "Passed!"






















