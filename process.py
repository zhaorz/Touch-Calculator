"""
process.py
~~~~~~~~~~~~~~~
Handles feature extraction from raw touch data.

The Feature class provides methods for normalization, trimming, stroke
splitting, and vector feature creation.

Example:

    $ python process.py 
    >>> processor = Feature()
    >>> processor.update(rawData)
    >>> print processor.vFeature
    >>> [ 0.991239123, 0.7273723721, 0.0212312309 ]

"""

import math
import testCanvas
import fileIO



class Feature(object):
    """This class handles feature extraction of raw touchpad data.

    Args:
        points (list, optional): Raw data from touchpad in (x, y, timestamp)
            tuples. Defaults to empty list.
        dimensions (int, optional): Number of dimensions used for vector sum.
            Defaults to 3.

    Attributes:
        rawDataPoints (list): Initial raw data.
        vecDimensions (int): Number of dimensions used for vector sum.
        feature (list): Output feature of processing.

    """
    def __init__(self, points=[], vecDimensions=3):
        self.rawDataPoints = points
        self.vecDimensions = 3
        self.dimensions = self.vecDimensions + 1
        self.vecFeature = [0.0 for _ in xrange(self.vecDimensions)]
        self.lenFeature = 0.0
        self.feature = self.vecFeature + [self.lenFeature]
        self.feature = self.normalizeVector(self.feature)
        self.process()

    def process(self):
        """Data processing pipeline.

        Normalization -> primative stroke splitting -> stroke trimming ->
        -> stroke vectorization -> feature creation

        Args: None

        Returns: None

        """
        normalizedPoints = self.normalizePoints(self.rawDataPoints)
        rawStrokes = self.primativeSplit(normalizedPoints)
        trimmedStrokes = [self.trimPoints(stroke) for stroke in rawStrokes]
        vectorStrokes = [self.vector(stroke) for stroke in trimmedStrokes]
        vectorSplit = self.vectorSplitCharacter(vectorStrokes)
        self.vecFeature = self.vectorFeature(vectorSplit)
        self.lenFeature = self.lengthFeature(vectorSplit)
        self.feature = self.vecFeature + [self.lenFeature]
        self.feature = self.normalizeVector(self.feature)

    def update(self, rawData):
        """Reprocesses new data.

        Args:
            rawData (list): Raw data from touchpad in (x, y, timestamp) tuples.

        Returns: None

        """
        self.rawDataPoints = rawData
        self.process()

    def normalizeVector(self, vector):
        """Applies sigmoid function to all components of the vector.

        Args:
            vector (list): Arbitrary-dimension vector.

        Returns:
            list: Return value of sigmoid for each component in vector.

        """
        normalized = []
        for x in vector:
            normalized.append(sigmoid(x))
        return normalized

    def normalizePoints(self, points):
        """Maps points to a 1.0 by 1.0 space.

        Args:
            points (list): Points in the form (x, y, timestamp)

        Returns:
            normalizedPoints (list): The normalized points. Points are still
                in (x, y, timestamp) form.

        """
        if (points == []):
            return points
        ((minX, minY), (maxX, maxY)) = self.findCorners(points)
        width, height = maxX - minX, maxY - minY
        width = 1.0 if width == 0.0 else width      # for vert/horz input
        height = 1.0 if height == 0.0 else height
        normalizedPoints = []
        for (x, y, timestamp) in points:
            x -= minX
            y -= minY
            x *= 1.0 / width
            y *= 1.0 / height
            normalizedPoints.append((x, y, timestamp))
        return normalizedPoints

    def findCorners(self, points):
        """Calculate the bottom left and top right corners of raw data.

        Args:
            points (list): Points in the form (x, y, timestamp)
        
        Returns:
            (float, float), (float, float)  

        """                   
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

    def primativeSplit(self, points):
        """Splits raw data into strokes based on timestamp values.

        Raw data from the multitouch.Trackpad class comes with the system
        allocated timestamp as the third tuples value. Constructs intermediate
        lists and keeps track of time separation between adjacent points.

        Args:
            points (list): A normalized list of (x, y, timestamp) tuples.

        Returns:
            [stroke, ... ] (2D list): Each element is a list of 
                (x, y, timestamp) tuples.

        """
        if (points == []):
            return [[]]
        strokes = []
        newStroke = []
        for i in xrange(len(points)):
            # begin a new stroke
            if (newStroke == []):
                newStroke.append(points[i])
            # previous point belongs to same stroke
            elif (self.isSameStroke(newStroke[-1], points[i]) == True):
                newStroke.append(points[i])      # only include x and y
            # start a new stroke
            else:
                strokes.append(newStroke)
                newStroke = [points[i]]
        if (newStroke != []):   # add last stroke if necessary
            strokes.append(newStroke)
        return strokes

    # True if the two datapoints belong on the same stroke, False otherwise
    def isSameStroke(self, (x1, y1, t1), (x2, y2, t2), epsilon=0.08):
        """Checks if two points belong on the same stroke.

        Uses timestamp data allocated by the system. Timestamp data does not
        seem to correspond with system time. Instead, points placed by the 
        same finger seem to have a timestamp separation of around 0.08.

        Args:
            x1, y1, t1 (float), (float), (float): Data for point 1. x and y
                are positional coordinates. t is the timestamp.
            x2, y2, t2 (float), (float), (float): Data for point 2, see above.
            epsilon (float, optional): Value that determines stroke membership.
                Defaults to 0.08.

        Returns:
            bool: True if the two points belong on the same stroke.
                False otherwise.

        """
        if (abs(t1 - t2) <= epsilon):
            return True
        else:
            return False

    def trimPoints(self, points, epsilon=0.02):
        """Removes points in a stroke that are too close.

        This is meant to improve angle calculation of the vectors that
        arise from points.

        Args:
            points (list): Normalized (x, y, timestamp) points from one stroke.
            epsilon (float, optional): Normalized distance cutoff. 
                Default is 0.02.

        Returns:
            trimmedPoints (list): Points of form (x, y) with timestamp removed
                and any neighbors deemed too close removed.

        """
        if (points == []):
            return []
        trimmedPoints = [points[0]]     # start with first point
        prev = 0                        # keep track of previous point index
        for nxt in xrange(1, len(points)):
            (x0, y0) = points[prev][:2]
            (x1, y1) = points[ nxt][:2]
            # points are sufficiently separated: add point and update prev
            if (magnitude((x0, y0), (x1, y1)) > epsilon):
                trimmedPoints.append(points[nxt][:2])
                prev = nxt
        return trimmedPoints

    def vector(self, points):
        """Vectorizes points as the component-wise distance between neighbors.

        Args:
            points (list): Normalized and trimmed (x, y) tuples.

        Returns:
            List of vectors where each vector is a 2-element list.

            {
                [(x0, y0), (x1, y1), ... , (x(n), y(n))]
                --> [[x1 - x0, y1 - y0], ... , (x(n) - x(n-1), y(n) - y(n-1)]]
            }

        """
        vectors = []
        for i in xrange(len(points) - 1):
            (x0, y0) = points[    i][:2]
            (x1, y1) = points[i + 1][:2]
            vectors.append([x1 - x0, y1 - y0])
        return vectors

    def vectorSplitCharacter(self, strokes):
        """Apply a vector split to each stroke in a list of strokes.

        Args:
            strokes (3D list): Elements are lists of vectors.

        Returns:
            3D list of at least the same number of strokes.

        """
        vectorSplitStrokes = []
        for stroke in strokes:
            vectorSplitStrokes.extend(self.vectorSplit(stroke))
        return vectorSplitStrokes

    def vectorSplit(self, stroke, n=4, epsilon=math.pi/3):
        """Split a stroke at it's greatest angle, if the angle exceeds a cutoff.

        Args:
            stroke (list): Elements are [x, y] vectors.
            n (int, optional): Distance between 2 observation vectors.
            epsilon (float, optional): Angle in radians of cutoff angle.

        Returns:
            [substroke1, substroke2] if the greatest angle surpasses cutoff.

            [stroke] if not.

        """
        theta = []
        for i in xrange(1, len(stroke) - n):
            theta.append(angle(stroke[i], stroke[i + n]))
        maxAngle = max(theta) if theta != [] else 0.0
        if (maxAngle > epsilon):
            # indecies in theta correspond to index + n / 2 in stroke
            splitIndex = theta.index(maxAngle) + n / 2
            return self.splitList(stroke, splitIndex)
        else:
            return [stroke]

    def splitList(self, L, i):
        """Splits a list at index i. Returns a list containing the elements
        after splitting."""
        return [L[:i], L[i:]]

    def addVectorDimension(self, v, origin, k):
        """Adds components of a vector to a given starting index in origin.

        Destructively modifies the origin vector.

        Args:
            v (list): Vector of arbitrary dimensions. [x, y, ... ]
            origin (list): Vector with at least as many dimensions as v.
            k (int): Index in origin at which addition of v's components begins.

        Returns: None

        """
        if (len(v) > len(origin)):
            print "Error: v cannot have greater dimensionality than the origin."
            return -1
        for vIndex in xrange(len(v)):
            originIndex = (vIndex + k) % len(origin)
            origin[originIndex] += v[vIndex]
        return None

    def vectorFeature(self, vectorStrokes):
        """Creates a vector feature from processed strokes.

        Args:
            vectorStrokes (3D list): List elements are strokes. Each stroke
                contains vectors, which are lists.

        Returns:
            origin (list): Vector with length = self.vecDimensions

        """
        if (self.vecDimensions < 2):
            print "Must have at least 2 dimensions"
            return -1
        origin = [0.0 for _ in xrange(self.vecDimensions)]
        k = 0   # starting dimension is x
        for vectorStroke in vectorStrokes:
            for vector in vectorStroke:
                self.addVectorDimension(vector, origin, k)
            # shift to adjacent plane
            k = (k + 1) % self.vecDimensions
        return origin

    def lengthFeature(self, vectorStrokes):
        """Creates a single feature corresponding to total nomralized length.

        Args:
            vectorStrokes (3D list): List elements are strokes. Each stroke
                contains vectors, which are lists.

        Returns:
            float: A scalar normalized length.

        """
        l = 0.0
        for vectorStroke in vectorStrokes:
            for vector in vectorStroke:
                l += length(vector)
        return l


################################
# Misc functions
################################



def magnitude((x0, y0), (x1, y1)):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def length(v):
    """Length of a vector in form [x, y, ... , z]."""
    return (sum(a ** 2 for a in v)) ** 0.5

def dotProduct(v1, v2):
    """Sum product for the components of v1 and v2. v1 and v2 should have 
    same dimensions."""
    if (len(v1) != len(v2)):
        return None
    return sum(a * b for a,b in zip(v1, v2))

def angle(v1, v2):
    """Angle between two vectors of the same dimensions. Return value is between
    0 and pi"""
    try:
        return math.acos(dotProduct(v1, v2) / (length(v1) * length(v2)))
    except:     # if one of the vectors has length 0
        return 0.0

def sigmoid(x):
    """Normalization functions

    Args:
        x (float): Input number. Domain is all real numbers.

    Returns:
        float: Between -1 and 1.

    """
    return 2.0 / (1.0 + math.e ** (-x)) - 1.0
