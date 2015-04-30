Touch Calculator

for Mac OS X 10.6+

~~~~~~~~~~~~~~~~~~~

Richard Zhao 2015
Carnegie Mellon University
for 15-112 Spring 2015, Professor David Kosbie

~~~~~~~~~~~~~~~~~~~


About
~~~~~~~~~
Touch Calculator is a Python program that performs basic numerical and
scientific calculations. Instead of using keyboard input, Touch Calculator
accepts input from the Mac touchpad.

There are two main forms of input: button and draw. Button mode behaves like a
regular pocket calculator. Tap the buttons to input numbers and basic operators.
To input more complex functions and constants, use draw mode. Users in draw mode
can use their finger to draw characters on the touchpad. The touchpad has self
resets if input is taken too long (which prevents lag).

No mouse control is allowed while the application window is active. To quit,
press command-Q, command-W, or ctrl-Q.


Installation
~~~~~~~~~
External modules:
    PyObjC: for Mac OS X Cocoa bindings in Python.
    py2app: to bundle the program into a standalone Mac OS X applet.

Build (optional):
    To create a standalone applet from the source. Not included because the file
    size is much larger (~17 MB).

        $ python setup.py py2app

    This creates a directory named dist that contains the app. The build
    directory contains intermediate files and can be deleted.


Citations
~~~~~~~~~
multitouch.py - lines 23-117 
    http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html
    The source was modified to be importable.

mouse.py - lines 27-36
    https://developer.apple.com/library/mac/documentation/GraphicsImaging/
    Conceptual/QuartzDisplayServicesConceptual/Articles/MouseCursor.html
    Modified to work as PyObjC bindings.

TouchCalculator.icns
    Carbon copy of the Apple default Calculator app icon.

















