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


def vote(neighbors):
    """Returns dictionary of the proportion of each instance in form
    (instance, distance) tuples."""
    total = 0
    count = dict()
    # Count all instances
    for (instance, distance) in neighbors:
        total += 1
        if (instance in count):
            count[instance] += 1
        else:
            count[instance] = 1
    # Divide each count by total to get proportion
    for instance in count.keys():
        count[instance] = float(count[instance]) / total
    return count

def testVote():
    print "Testing vote()... ",
    neighbors = [
        ('A', 1), ('A', 1), ('A', 1), ('A', 1), ('A', 1), ('A', 1), ('A', 1),
        ('B', 1), ('B', 1), ('B', 1), ('B', 1),
        ('C', 1)
        ]
    votes = vote(neighbors)
    assert(almostEqual(votes['A'], float(7) / 12))
    assert(almostEqual(votes['B'], float(4) / 12))
    assert(almostEqual(votes['C'], float(1) / 12))
    print "Passed!"


def kNN(model, instance, k):
    """Returns a dictionary of vote proportions for the kth nearest neighbors
    of the instance in the model"""
    n = len(instance)
    neighbors = allNeighbors(model, instance, n)
    kNearest = kNearestNeighbors(neighbors, k)
    return vote(kNearest)

def topNClasses(voteProportions, n):
    """Returns a sorted descending list of the top n classes in a vote."""
    votes = []
    for key in voteProportions.keys():              # put votes into a list
        votes.append((key, voteProportions[key]))
    # sort votes by comparing vote proportion (index 1)
    votes = sorted(votes, lambda a, b: cmp(a[1], b[1]))
    votes = votes[::-1]     # reverse to get descending order
    return votes[:n]        # return the n highest

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
    assert(topNClasses(votes, 4) == [('A', 0.6), ('B', 0.3), 
                                    ('C', 0.05), ('D', 0.025)])
    print "Passed!"
















