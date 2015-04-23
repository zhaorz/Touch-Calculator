"""
multitouch.py
~~~~~~~~~~~~~~~
Richard Zhao

Access raw touchpad data using Apple's MultitouchSupport private framework.
To start data collection, create a Trackpad() instance and call its start()
method. To stop, call stop(). Data for a single start-stop cycle is stored in
Trackpad's touchData list. See touch_callback() for the types of data stored.

Source code for everything except touch_callback(), start(), and stop() from
http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html
The source was modified to be importable.
"""


import ctypes


class MTPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class MTVector(ctypes.Structure):
    _fields_ = [("position", MTPoint),
                ("velocity", MTPoint)]

class MTData(ctypes.Structure):
    _fields_ = [
      ("frame", ctypes.c_int),
      ("timestamp", ctypes.c_double),
      ("identifier", ctypes.c_int),
      ("state", ctypes.c_int),  # Current state (of unknown meaning).
      ("unknown1", ctypes.c_int),
      ("unknown2", ctypes.c_int),
      ("normalized", MTVector),  # Normalized position and vector of
                                 # the touch (0 to 1).
      ("size", ctypes.c_float),  # The area of the touch.
      ("unknown3", ctypes.c_int),
      # The following three define the ellipsoid of a finger.
      ("angle", ctypes.c_float),
      ("major_axis", ctypes.c_float),
      ("minor_axis", ctypes.c_float),
      ("unknown4", MTVector),
      ("unknown5_1", ctypes.c_int),
      ("unknown5_2", ctypes.c_int),
      ("unknown6", ctypes.c_float),
    ]


class Trackpad(object):

    # Initializes contents of private framework MultitouchSupport
    def __init__(self):
        self.touchData = []  # holds data from start() method call

        self.CFArrayRef = ctypes.c_void_p
        self.CFMutableArrayRef = ctypes.c_void_p
        self.CFIndex = ctypes.c_long

        self.MultitouchSupport = ctypes.CDLL("/System/Library/PrivateFrameworks/" + 
                                        "MultitouchSupport.framework/MultitouchSupport")

        self.CFArrayGetCount = self.MultitouchSupport.CFArrayGetCount
        self.CFArrayGetCount.argtypes = [self.CFArrayRef]
        self.CFArrayGetCount.restype = self.CFIndex

        self.CFArrayGetValueAtIndex = self.MultitouchSupport.CFArrayGetValueAtIndex
        self.CFArrayGetValueAtIndex.argtypes = [self.CFArrayRef, self.CFIndex]
        self.CFArrayGetValueAtIndex.restype = ctypes.c_void_p

        self.MTDeviceCreateList = self.MultitouchSupport.MTDeviceCreateList
        self.MTDeviceCreateList.argtypes = []
        self.MTDeviceCreateList.restype = self.CFMutableArrayRef

        self.MTDataRef = ctypes.POINTER(MTData)

        self.MTContactCallbackFunction = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, 
            self.MTDataRef, ctypes.c_int, ctypes.c_double, ctypes.c_int)

        self.MTDeviceRef = ctypes.c_void_p

        self.MTRegisterContactFrameCallback = self.MultitouchSupport.MTRegisterContactFrameCallback
        self.MTRegisterContactFrameCallback.argtypes = [self.MTDeviceRef, self.MTContactCallbackFunction]
        self.MTRegisterContactFrameCallback.restype = None

        self.MTDeviceStart = self.MultitouchSupport.MTDeviceStart
        self.MTDeviceStart.argtypes = [self.MTDeviceRef, ctypes.c_int]
        self.MTDeviceStart.restype = None

        self.MTDeviceStop = self.MultitouchSupport.MTDeviceStop
        self.MTDeviceStop.argtypes = [self.MTDeviceRef]
        #MTDeviceStop.restype = None

    def _cfarray_to_list(self, arr):
        self.rv = []
        self.n = self.CFArrayGetCount(arr)
        for i in xrange(self.n):
            self.rv.append(self.CFArrayGetValueAtIndex(arr, i))
        return self.rv

    def init_multitouch(self, cb):
        self.strokeStart = False
        self.devices = self._cfarray_to_list(self.MultitouchSupport.MTDeviceCreateList())
        for device in self.devices:
            self.MTRegisterContactFrameCallback(device, cb)
            self.MTDeviceStart(device, 0)
        return self.devices

    def stop_multitouch(self, devices):
        self.strokeStart = True
        for device in devices:
            self.MTDeviceStop(device)

    def touch_callback(self, device, data_ptr, n_fingers, timestamp, frame):
        data = data_ptr[0]      # only use the first finger
        pos = data.normalized.position
        p = (pos.x, pos.y, timestamp)
        self.touchData.append(p)    # add point to return array
        return 0

    def start(self):
        del self.touchData[:]   # reset data
        self.touch_callback = self.MTContactCallbackFunction(self.touch_callback)
        self.devs = self.init_multitouch(self.touch_callback)

    def stop(self):
        self.stop_multitouch(self.devs)



class VisualTrackpad(Trackpad):
    """A graphical representation of the Trackpad class.

    This version draws a toggle when receiving input.
    
    Args:
        x (int): Left canvas coordinate (in pixels).
        y (int): Top canvas coordinate.
        width (int): Width of the visual trackpad.
        height (int): Height of the visual trackpad.

    Attributes:
        isDrawing (bool): True if currently receiving input, False otherwise.
        fg (str): foreground color
        bg (str): background color
        active (str): active trackpad color
        highlight (str): highlight color

    """
    def __init__(self, x, y, width, height):
        super(VisualTrackpad, self).__init__()        # call parent __init__
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isDrawing = False
        self.fg = "#666666"
        self.bg = "#e5e6e6"
        self.active = "#cae2ed"
        self.highlight = "#72bdf6"     

    def draw(self, canvas):
        x0 = self.x
        y0 = self.y
        x1 = self.x + self.width
        y1 = self.y + self.height
        color = self.bg if self.isDrawing == False else self.active
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
        self.drawData(canvas)

    def drawData(self, canvas):
        r = 5
        """
        # draw the most recent point larger and highlighted
        if (self.touchData != []):
            (normx0, normy0, time0) = self.touchData[-1]       # most recent point
            x0 = self.x + normx0 * self.width
            y0 = self.y + self.height - normy0 * self.height
            self.drawDot(canvas, x0, y0, r * 2, self.highlight)
        """
        for (normx, normy, timestamp) in self.touchData:
            x = self.x + normx * self.width
            y = self.y + self.height - normy * self.height
            self.drawDot(canvas, x, y, r, self.fg)

    def drawDot(self, canvas, cx, cy, r, color):
        x0 = cx - r
        x1 = cx + r
        y0 = cy - r
        y1 = cy + r
        canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)
