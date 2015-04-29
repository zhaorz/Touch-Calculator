"""
mouse.py
~~~~~~~~~~~~~~~

Functions that hook Apple's Quartz framework to python. Used for locking down
the mouse position.

Slight modifications to convert code to python.

Original source code from: 
https://developer.apple.com/library/mac/documentation/GraphicsImaging/
Conceptual/QuartzDisplayServicesConceptual/Articles/MouseCursor.html
"""


# Apple Frameworks
import Quartz
from Quartz.CoreGraphics import kCGNullDirectDisplay

import time

##########################
# Code by Richard Zhao
##########################


def lockCursor(x, y):
    """Moves cursor to pixel location (x, y) and locks movement."""
    Quartz.CGDisplayHideCursor(kCGNullDirectDisplay)
    Quartz.CGAssociateMouseAndMouseCursorPosition(False)
    Quartz.CGDisplayMoveCursorToPoint(Quartz.CGMainDisplayID(), (x,y))

def freeCursor():
    """Release mouse control."""
    Quartz.CGAssociateMouseAndMouseCursorPosition(True)
    Quartz.CGDisplayShowCursor(kCGNullDirectDisplay)
