"""
model.py
~~~~~~~~~~~~~~~
Handles data sets used to implement kNN.

Each Model instance keeps track of a set of tuples that relate an instance
type to a feature vector. New instances can be added from raw data files.
Additionally, old models can be loaded into new ones. Models can also be saved.

The main program can call the modelKNN() method to obtain
a dictionary of vote proportions corresponding to the data in the model. kNN
implementation is still handled in knn.py.

Example:

    $ python model.py
    >>> model2 = Model("test_model_2", 3)
    >>>
    >>> model2.load("model/test_model_1")
    >>>
    >>> instance = [ 0.432, 0.192, 0.416 ]
    >>> print model2.modelKNN(instance, 5)
    >>> { 'A': 0.8 , 'B': 0.2 }

"""


# Standard libraries
import os
import knn
import copy

# Packaged libraries
import fileIO
import process


class Model(object):
    """Object that handles a knn character recognition model. 
    
    Args:
        name (str): String used for saving the model.
        dimensions (int): Number of deimensions of feature vectors.
        directory (str, optional): Name of save directory. Defaults to "model"

    Attributes:
        data (list): Elements are tuples (instance, feature) where instance
            is the type/classification and feature is a feature vector.
        sources (list): Elements are str corresponding with the raw data files.

    """
    def __init__(self, name, dimensions=11, directory="model"):
        self.name = name
        self.dimensions = dimensions
        self.directory = directory
        self.data = []
        self.sources = []   # keep track of origin of raw data
        self.initModel()    # attempt to load name

    def initModel(self):
        if (self.name in os.listdir(self.directory)):
            # Try loading existing
            if (self.load(self.directory + os.sep + self.name) != -1):
                print "Load of " + str(self.name) + " successful."
                return
            else:
                print "Load failed."

    def __len__(self):
        """Override default len() function by return length of data list"""
        return len(self.data)

    def __repr__(self):
        count = self.symCount()
        result = ""
        result += 'sym ' + '      count\n'
        result += '____' + '     _______\n\n'
        for sym in sorted(count.keys()):
            result += repr(sym) + ':' + '\t\t' + str(count[sym]) + '\n'
        return result

    def save(self):
        """Creates file if first save, overwrites if file aready exists."""
        saveData = dict()
        saveData["name"] = self.name
        saveData["dimensions"] = self.dimensions
        saveData["data"] = self.data
        saveData["sources"] = self.sources
        fileIO.writeTo(self.directory + os.sep + self.name, saveData)

    def load(self, modelName):
        """Opens modelName, checks that dimensions correspond and updates 
        data"""
        newModelData = fileIO.read(modelName)
        print "Loading model:", newModelData["name"]
        if (newModelData["dimensions"] != self.dimensions):
            print "Error: imput model must have same dimensions"
            return -1
        self.sources.extend(newModelData["sources"])
        self.data.extend(newModelData["data"])

    def loadModelSources(self, modelName):
        newModelData = fileIO.read(modelName)
        print "Loading model sources from", newModelData["name"]
        for source in newModelData["sources"]:
            self.extendData(source)

    def extendData(self, rawDataFile):
        """Processes data in rawDataFile using process.vectorFeature() on each
        element of the raw data. Raw data is a list of dictionaries."""
        processedData = []
        rawData = fileIO.read(rawDataFile)
        processor = process.Feature()
        for d in rawData:
            for key in d.keys():
                # process raw data into a vector feature
                processor.update(d[key])
                feature = processor.feature
                processedData.append((key, feature))
        self.data.extend(processedData)
        self.sources.append(rawDataFile)    # update sources list

    def addNewData(self):
        """Quickly adds the most recent data file in data/ directory."""
        m1.extendData(fileIO.bottomFile("data"))

    def symCount(self):
        count = dict()
        for (sym, v) in self.data:
            if (sym not in count.keys()):
                count[sym] = 1
            else:
                count[sym] += 1
        return count

    def removeSym(self, sym):
        """Remove all data points of sym."""
        temp = []
        for (s, v) in self.data:
            if (s != sym):
                temp.append((s, v))
        del self.data[:]
        self.data = copy.deepcopy(temp)

    def printSymCount(self):
        """Prints a vertical list of all data symbols and their counts."""
        count = self.symCount()
        print 'sym ' + '      count'
        print '____' + '     _______'
        print
        for sym in sorted(count.keys()):
            print repr(sym) + ':' + '\t\t' + str(count[sym])

    def modelKNN(self, instanceFeature, k):
        """Performs a kNN on the model data and returns a dictionary of the vote
        proportions for the k nearest instances."""
        return knn.kNN(self.data, instanceFeature, k)
