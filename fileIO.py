"""
fileIO.py
~~~~~~~~~~~~~~~


"""


import pickle
import os
from time import localtime, strftime


# Creates new file and saves contents using pickle to serialize
def writeTo(filename, contents):
    with open(filename, "wt") as f:
        # write contents to file object f
        pickle.dump(contents, f, pickle.HIGHEST_PROTOCOL)

# Deserializes pickled object and returns the original data structure
def read(filename):
    with open(filename, "rt") as f:
        contents = pickle.load(f)
        return contents

# Specialized for the data directory, where filenames are creation times
def openRecent(directory):
    filename = bottomFile(directory)
    return read(directory + os.sep + filename)

# Returns last filename in a sorted list of all filenames in a directory
def bottomFile(directory):
    return directory + os.sep + sorted(os.listdir(directory))[-1]

# Takes a list of dictionaries, returns list of (key, value) tuples
def processDictList(a):
    tuples = []
    for d in a:
        for key in d.keys():
            tuples.append((key, d[key]))
    return tuples

# Takes a file of a list of dictionaries, returns list of (key, value) tuples
def processDictListFile(filename):
    lst = read(filename)
    return processDictList(lst)

# returns string in MMDDYY_HHMMSS format (month/day/year_hour/min/sec)
def timeStr():
    return strftime("%m%d%y_%H%M%S", localtime())
