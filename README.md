# Touch Calculator

Richard Zhao | 2015 | Carnegie Mellon University

richardz@andrew.cmu.edu

This project was made for 15-112 in spring 2015, an introductory programming
couse taught by Professor David Kosbie.

## About

<a href="http://www.youtube.com/watch?feature=player_embedded&v=9xGWnnozi-M&feature=youtu.be
" target="_blank"><img src="https://raw.githubusercontent.com/zhaorz/Touch-Calculator/master/design/screenshot.jpg" 
alt="Touch Calculator Video" width="660" height="471" border="10" /></a>

Touch Calculator is a Python program for Mac that performs basic numerical and
scientific calculations. Instead of using keyboard input, Touch Calculator
accepts input from the Mac touchpad.

There are two main forms of input: button and draw. Button mode behaves like a
regular pocket calculator. Tap the buttons to input numbers and basic operators.
To input more complex functions and constants, use draw mode. Users in draw mode
can use their finger to draw characters on the touchpad. The touchpad has self
resets if input is taken too long (which prevents lag).

No mouse control is allowed while the application window is active. To quit,
use `command-Q` or `ctrl-Q`.

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

    To create a standalone applet from the source. Not included because the file
    size is much larger (~17 MB).

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

#### From build (debug mode)

In the top level directory, execute

    $ ./dist/Touch\ Calculator.app/Contents/MacOS/Touch\ Calculator

which runs the program direction from the Terminal, and displays console
output.

#### From source

In the top level directory, execute

    $ python main.py

## Technology

#### Feature Detection

The process.py module contains a feature detection pipeline for raw trackpad
drawings. It implements an original algorithm that adds vectorized strokes
in an arbitrary dimensionality while dimension switching in between each
addition.

The pipeline contains normalization, vectorization, and a collection of
other processes.

The module is also able to analyze more traditional features, such as
length, curvature, and number of strokes. All together, the processing
outputs feature vectors of length 11.

#### Machine Learning
    
A custom implementation of the K-Nearest-Neighbors algorithm is used to 
classify input data. Each input is processed to an 11-dimensional feature
vector which is classified by the kNN algorithm.

The relatively low dimensionality provides fast computation time while
preserving high accuracy. The classifier by default includes only 462
instances of data for 32 unique characters. This is just under an average
of 15 training instances for each character, an very low number for
traditional machine learning techniques.

Users can also train their own data sets and add new characters. The
dataCollection module provides a GUI to train new data. After training,
the data must either be processed into a model or added to an existing one,
using the model module. To switch to this new model, change the model name
in line 113 of main.py.

If the user needs to build a standalone app of the new data, the app must
be rebuilt using py2app. The existing distribution must be removed first.

    $ rm -rf build dist
    $ python setup.py py2app

This rebuilds the app, which is still found in the dist/ directory.

## License

This code is avaiable for use under the [MIT License]
(https://github.com/zhaorz/Touch-Calculator/blob/master/LICENSE).

## Citations

1. **eventBasedAnimation.py** - all

    From Carnegie Mellon Professor <a
    href="http://www.cs.cmu.edu/~112/notes/eventBasedAnimation.py">David Kosbie</a>.
    Provides animation framework.

2.  **multitouch.py** - lines 23-117 

    From <a href="http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html">blog.sendapatch.se</a>. 
    The source was modified into object oriented code.

3.  **mouse.py** - lines 27-36

    From the <a
    href="https://developer.apple.com/library/mac/documentation/GraphicsImaging/Conceptual/QuartzDisplayServicesConceptual/Articles/MouseCursor.html">Apple Quartz Display Services</a> documentation. 
    Modified to work in Python using PyObjC bindings.

4.  **TouchCalculator.icns** - all

    Carbon copy of the Apple default Calculator app icon.

