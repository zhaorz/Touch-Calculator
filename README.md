# TypeCrypt
## Trackpad Character Recognition using kNN

### Abstract
In this work we explore a novel way of recognizing online character input from traditional laptop trackpads. We present a simple yet effective algorithm to extract features efficiently from data in real time. Our method does not need an extremely high dimensional space that current recognition methods require to implement a K-Nearest-Neighbors algorithm. By performing vector operations on input data, we are able to obtain adequate class separation without high dimensionality while maintaining computational efficiency.

### Introduction

Traditionally, optical and online character recognition pipelines use a variety of normalization, decomposition, thinning operations, and pixel analysis in order to extract features. In terms of implementing a kNN algorithm, most approaches use bitmap pixel data as input nodes, thus pushing the dimensionality much higher than 100 in most cases. In our proposed pipeline, less than 10 dimensions are needed.

### Pipeline

raw input (2D points) —> normalized input —> stroke separation —> 2D vectorization —> vector addition (3 < dimensions < 10) —> kNN —> character recognition


### Pipeline (detail)

We use an Apple Macbook Pro trackpad to input touch data. Apple’s MultitouchSupport private framework is used to obtain low-level access to the trackpad’s output. Source code for the Objective-C headers and subsequent Python wrappers are found in this file’s Modules/Technologies section. We then wrap slightly modified versions of these methods inside an importable module for better usability.

Normalization is performed in a standard way to obtain touch point values between 0 and 1. This procedure eliminates deviations caused by different scales.

Stroke separation is performed in two ways. First, physical strokes are separated trivially by analyzing touch point timestamps (timestamp data is provided by the MultitouchSupport framework). Next, additionally separation points can be mined in a variety of ways. For example, the algorithm can choose to break lines at points that experience a change in direction above a certain threshold.

2D vectorization is performed in a standard way:
    [(x_1, y_1), (x_2, y_2), ... , (x_n, y_n)]
    —>
    [(x_2 - x_1, y_2 - y_1), ... , (x_n - x_(n-1), y_n - y_(n-1))]

Vector addition in n dimensions is also performed using addition, starting from the origin. e.g. in three dimensions, the origin is [0.0, 0.0, 0.0]. Then, each vectorized stroke is added into two adjacent dimensions, with a plane shift by 1 after each stroke. e.g. the first stroke is (x, y) —> (x, y), the second stroke is (x, y) —> (y, z), the third strokes is (x, y) —> (z, x), the fourth stroke is (x, y) —> (x, y), and so on. 

The resultant of n-dimensional vector addition is a n-dimensional vector. This vector is used as the data input for our kNN algorithm. We use Euclidean distance to determine the nearest neighbors for each additional input. Our kNN implementation is standard. For each new instance, we calculate the distance between the instance and every one of the model’s instances to find the K nearest instances (by Euclidean distance). We then use a majority vote to determine the recognized character, yet values of confidence are easily obtained for all possible characters.

As our method of vector addition guarantees low-dimension resultants, the kNN algorithm does not need additional efficiency optimizations. Additionally, good training data will yield strong instance separation in the feature space.


### User Experience

The end user of this project is only exposed to the input and output of our pipeline. A GUI contains input display to draw trackpad data in real time. Below the input field is a display area for the top matches, with options to select amongst them. There is also potential for a separate ‘training’ window in which users can input their own characters to the kNN model to improve accuracy. This is user customization/personalization. Since handwriting is very personal, the variance between different users can be significant. Thus, personalizing the recognition model is important.


### Modules/Technologies

Apple MultitouchSupport Private Framework
/System/Library/PrivateFrameworks/MultitouchSupport.framework/MultitouchSupport

ctypes (default)
For type handling of the MultitouchSupport framework (Objective-C)

http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html
Source code that outlines use of MultitouchSupport and ctypes

string (default)

copy (default)

os (default)
For file management

time (default)
For file naming

pickle (default)
For file IO

math (default)
For calculating angles

eventBasedAnimation.Animation
For implementing UI

kNN algorithm
The algorithm’s implementation is original code.
