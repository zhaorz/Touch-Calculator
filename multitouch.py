"""
multitouch.py
~~~~~~~~~~~~~~~

A customized wrapper for source code found at
http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html

Wrapped code into classes to use as an importable module.

"""


import time
import ctypes
import threading
from ctypes.util import find_library


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
        self.touchData = []  # holds data from one call of stroke()
        self.strokeData = []

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
        self.fingers = []
        for i in xrange(n_fingers):
            self.fingers.append(data_ptr[i])
            # Only send first finger's data
            for finger in self.fingers[:1]:
                pos = finger.normalized.position
                p = (pos.x, pos.y, timestamp)
                self.touchData.append(p)    # add point to return array
        #self.touches[:] = [(frame, timestamp, self.fingers)]
        return 0

    def start(self):
        del self.touchData[:]   # reset data
        self.touch_callback = self.MTContactCallbackFunction(self.touch_callback)
        self.touches_lock = threading.Lock()
        self.devs = self.init_multitouch(self.touch_callback)

    def stop(self):
        self.stop_multitouch(self.devs)







