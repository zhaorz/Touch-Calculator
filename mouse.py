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
from Quartz import CGDisplayHideCursor
from Quartz import CGDisplayShowCursor
from Quartz import CGAssociateMouseAndMouseCursorPosition
from Quartz import CGDisplayMoveCursorToPoint
from Quartz import CGMainDisplayID
from Quartz.CoreGraphics import kCGNullDirectDisplay


def lockCursor(x, y):
    """Moves cursor to pixel location (x, y) and locks movement."""
    CGDisplayHideCursor(kCGNullDirectDisplay)
    CGAssociateMouseAndMouseCursorPosition(False)
    CGDisplayMoveCursorToPoint(CGMainDisplayID(), (x,y))

def freeCursor():
    """Release mouse control."""
    CGAssociateMouseAndMouseCursorPosition(True)
    CGDisplayShowCursor(kCGNullDirectDisplay)
