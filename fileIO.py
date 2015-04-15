"""
fileIO.py
~~~~~~~~~~~~~~~


"""


import pickle
import os


# Creates new file and saves contents using pickle to serialize
def writeTo(filename, contents):
    f = open(filename, "w")
    # write contents to file object f
    pickle.dump(contents, f, pickle.HIGHEST_PROTOCOL)
    f.close()

# Deserializes pickled object and returns the original data structure
def read(filename):
    f = open(filename, "r")
    contents = pickle.load(f)
    f.close()
    return contents

# Specialized for the data directory, where filenames are creation times
def openRecent(directory):
    filename = sorted(os.listdir(directory))[-1]
    return read(directory + os.sep + filename)
