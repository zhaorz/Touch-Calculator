"""
mouse.py
~~~~~~~~~~~~~~~

Functions that hook Apple's mouse framework to python. Used for locking down
the mouse position.

Slight modifications to condense code.

Original source code from: 
http://www.geekorgy.com/index.php/2010/06/
    python-mouse-click-and-move-mouse-in-apple-mac-osx-snow-leopard-10-6-x/

"""


# Apple Frameworks
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
import Quartz


##########################
# Code by Richard Zhao
##########################

def hideCursor():
    Quartz.CGDisplayHideCursor(Quartz.CGMainDisplayID())

def showCursor():
    Quartz.CGDisplayShowCursor(Quartz.CGMainDisplayID())


##########################
# Code from source:
##########################


def mouseEvent(mode, posx, posy):
        event = CGEventCreateMouseEvent(
                    None, 
                    mode, 
                    (posx, posy), 
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, event)

def mouseMove(posx, posy):
        mouseEvent(kCGEventMouseMoved, posx, posy);

def mouseClick(posx,posy):
        # uncomment this line if you want to force the mouse 
        # to MOVE to the click location first (I found it was not necessary).
        #mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx,posy);
        mouseEvent(kCGEventLeftMouseUp, posx,posy);
