"""
model.py
~~~~~~~~~~~~~~~

Handles addition of new data points to existing knn models.

Model instances contain data associated to it's raw data sources. Models contain
methods that implement knn.


All models stored in /model

"""

import os
import knn
import fileIO
import process



class Model(object):
    """Object that handles a knn character recognition model. 
    Initialize with a name and the number of dimensions of feature vectors.
    The data model is stored in self.data."""

    def __init__(self, name, dimensions, directory="model"):
        self.name = name
        self.dimensions = dimensions
        self.directory = directory
        self.data = []
        self.sources = []   # keep track of origin of raw data

    def __len__(self):
        """Override default len() function by return length of data list"""
        return len(self.data)

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

    def extendData(self, rawDataFile):
        """Processes data in rawDataFile using process.vectorFeature() on each
        element of the raw data. Raw data is a list of dictionaries."""
        processedData = []
        rawData = fileIO.read(rawDataFile)
        for d in rawData:
            for key in d.keys():
                # process raw data into a vector feature
                feature = process.vectorFeature(d[key], self.dimensions)
                processedData.append((key, feature))
        self.data.extend(processedData)
        self.sources.append(rawDataFile)    # update sources list

    def kNearestNeighborProportions(self, instance, k):
        """Performs a kNN on the model data and returns a dictionary of the vote
        proportions for the k nearest instances. instance should be the same
        type as an element of raw data."""
        instanceFeature = process.vectorFeature(instance, self.dimensions)
        return knn.kNN(self.data, instanceFeature, k)



























