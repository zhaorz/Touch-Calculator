# Touch Calculator

Richard Zhao | 2015 | Carnegie Mellon University

richardz@andrew.cmu.edu

This project was made for 15-112 in spring 2015, an introductory programming
course taught by Professor David Kosbie and Professor Dave Andersen.

## About

<a href="http://www.youtube.com/watch?feature=player_embedded&v=9xGWnnozi-M&feature=youtu.be
" target="_blank"><img src="https://raw.githubusercontent.com/zhaorz/Touch-Calculator/master/graphics/screenshot.jpg"
alt="Touch Calculator Video" width="660" height="471" border="10" /></a>

Touch Calculator is a Python program for Mac that performs basic numerical and
scientific calculations. Instead of using keyboard input, Touch Calculator
accepts input from the Mac touchpad.

There are two main forms of input: button and draw. Button mode behaves like a
regular pocket calculator. Tap the buttons to input numbers and basic operators.
To input more complex functions and constants, use draw mode. Users in draw mode
can use their finger to draw characters on the touchpad. Drawings are recognized, and the top 4 matches are displayed for the user to
select.

Mouse control is disabled while the application window is active. To quit, use
`command-Q` or `ctrl-Q`.

Touch Calculator uses a real-time handwriting recognition engine. Its custom designed feature detection pipeline implements a novel method of projecting touch strokes in a n-dimensional feature space. The Technology section covers the technique in more detail.

## Getting Started

1. **Clone** into an empty directory.

        $ git clone https://github.com/zhaorz/Touch-Calculator.git

2. **Install PyObjC:** *(required)* for Mac OS X Quartz bindings in Python.

    Installation (with pip):

        $ pip install -U pyobjc

    or

        $ sudo pip install -U pyobjc

    For more information, visit the [PyObjC source website]
    (https://pythonhosted.org/pyobjc/install.html "PyObjC install Page")

3. **Install py2app:** *(optional)* to bundle the program into a standalone Mac
OS X applet.

    Installation:

        $ pip install -U py2app

    or

        $ sudo pip install -U py2app

    For more information, visit the [py2app source website]
    (https://pythonhosted.org/py2app/install.html "py2app install Page")

4. **Build** *(optional)*

    To create a standalone app.

        $ python setup.py py2app

    This creates a directory named 'dist' that contains the app. A directory
    named 'build' is also created that contains intermediate files. 'build' is
    unnecessary after packaging, so it can be removed with

        $ rm -rf build


## Usage

#### From dist/

On your local file system, navigate to dist/ and run the .app file.

To run the program directly from the Terminal,

    $ open -a dist/Touch\ Calculator.app

#### From source

In the top level directory, execute

    $ python main.py

#### From build (debug mode)

In the top level directory, execute

    $ ./dist/Touch\ Calculator.app/Contents/MacOS/Touch\ Calculator

which runs the program direction from the Terminal, and displays console
output.

## Technology

#### Feature Detection

The `process.py` module contains a feature detection pipeline for raw trackpad
input. It implements an original algorithm that adds vectorized strokes
in an arbitrary dimensional space.

In drawing mode, current touch data is continuously pushed through the pipeline and analyzed. First, each data set is normalized, and then a primitive stroke separation is performed. Each stroke becomes vectorized before length and curvature features are extracted.

Next, each stroke undergoes more rigorous splitting which scans for hard corners and changes in direction. Afterwards, the set of strokes is projected into a n-dimensional feature space by performing vector addition. We preserve the original order based on the stroke's timestamp, and consecutive vectors to the tips of previous ones. The algorithm is unique in that it performs each successive addition in an adjacent dimensional plane, thus increasing feature separation in the space. This method has several strengths, and a few weaknesses.

In terms of strengths, the algorithm is very good at separating features. Since handwriting is made of up a collection of strokes in various directions, it is relatively rare to have two characters that contain both similar strokes and similar stroke *directions*. Most people are consistent in the way they form characters, so with even minimal training, the algorithm achieves high recognition rates.

Additionally, the feature detection algorithm is extremely quick, and does not require the kind of extensive training that neural networks and other similar methods need. All together, the processing pipeline outputs feature vectors of length 11. (This varies on the number of dimensions used in the vector addition step.) In comparison to similar methods (which require as many vectors as the number of input pixels), 11 is very short. This is a significant advantage when an algorithm such as K-Nearest-Neighbors is used in the recognition stage.

In terms of weaknesses, the algorithm requires more data to generalize recognition. This is because different people have different handwriting styles. Writing "A" in one direction creates an entirely distinct feature vector than writing it in the other. Traditional handwriting recognition algorithms that only consider spatial location do not have this problem. The solution to this is to have a larger data set. (The course deadlines made it difficult to collect mass amounts of data, so I relied on my own handwriting samples, and relatively few others.)

#### Machine Learning

An implementation of the K-Nearest-Neighbors algorithm is used to
classify input data. Instances are the feature vectors from the processing pipeline outlined above.

The relatively low dimensionality provides fast computation time while
preserving high accuracy. The classifier by default includes only 462
instances of data for 32 unique characters. This is just under an average
of 15 training instances for each character, an very low number for
traditional machine learning techniques.

Users can also train their own data sets and add new characters. The
`dataCollection` module provides a GUI to train new data. After training,
the data must either be processed into a model or added to an existing one,
using the model module. To switch to this new model, change the model name
in line 113 of `main.py`.

If the user needs to build a standalone app of the new data, the app must
be rebuilt using py2app. The existing distribution must be removed first.

    $ rm -rf build dist
    $ python setup.py py2app

This rebuilds the app, which is still found in the `dist/` directory.

## License

This code is available for use under the [MIT License]
(https://github.com/zhaorz/Touch-Calculator/blob/master/LICENSE).

## Citations

All GUI's are created using Tkinter, a graphics package that comes installed with Python. The graphics used for the calculator background were produced by myself, but the design was inspired by Apple's native calculator app. The design of the drawing pad was influenced by Apple's Chinese character input keyboard.

The feature detection pipeline was designed and implemented by myself. The kNN algorithm used for classification is generic.

The following is code that was authored by other people. Each listing has the filename and line numbers of where the code is.

1. **eventBasedAnimation.py** - all

    From Carnegie Mellon Professor <a
    href="http://www.cs.cmu.edu/~112/notes/eventBasedAnimation.py">David Kosbie</a>.
    An animation framework for Tkinter.

2.  **multitouch.py** - lines 23-117

    From <a href="http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html">blog.sendapatch.se</a>.
    A collection of functions, CPython bindings, and Apple Multitouch wrappers for getting raw input on Macbook's. The original code was modified to fit into this project's architecture.

3.  **mouse.py** - lines 27-36

    From the <a
    href="https://developer.apple.com/library/mac/documentation/GraphicsImaging/Conceptual/QuartzDisplayServicesConceptual/Articles/MouseCursor.html">Apple Quartz Display Services</a> documentation. A few functions that control the mouse position (so it doesn't interferer with drawing). Modified from Objective C to work in Python using PyObjC bindings.

4.  **TouchCalculator.icns** - all

    A carbon copy of the Apple default Calculator app icon.

