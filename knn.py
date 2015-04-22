"""
knn.py
~~~~~~~~~~~~~~~

Kth Nearest Neighbors.

Call kNN(model, instance, k) on an existing model of training data to classify
a new instance based on the k nearest neighbors.

"""


def kNN(model, instance, k):
    """Returns a dictionary of vote proportions for the kth nearest neighbors
    of the instance in the model.
    This is the main function called by other files."""
    n = len(instance)
    neighbors = allNeighbors(model, instance, n)
    kNearest = kNearestNeighbors(neighbors, k)
    return vote(kNearest)

def euclideanDistance(a, b, n):
    """Computes length of line segment connecting 2 n-dimensional points. 
    Each point is a list of at least length n."""
    d = sum((a[i] - b[i]) ** 2 for i in xrange(n))
    return d ** 0.5

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

def topNClasses(voteProportions, n):
    """Returns a sorted descending list of the top n classes in a vote."""
    votes = []
    for key in voteProportions.keys():              # put votes into a list
        votes.append((key, voteProportions[key]))
    # sort votes by comparing vote proportion (index 1)
    votes = sorted(votes, lambda a, b: cmp(a[1], b[1]))
    votes = votes[::-1]     # reverse to get descending order
    return votes[:n]        # return the n highest
