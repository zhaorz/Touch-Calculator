# from 
# http://blog.sendapatch.se/2009/november/macbook-multitouch-in-python.html

from __future__ import with_statement
import time
import ctypes
import threading
from ctypes.util import find_library

CFArrayRef = ctypes.c_void_p
CFMutableArrayRef = ctypes.c_void_p
CFIndex = ctypes.c_long

MultitouchSupport = ctypes.CDLL("/System/Library/PrivateFrameworks/" + 
                                "MultitouchSupport.framework/MultitouchSupport")

CFArrayGetCount = MultitouchSupport.CFArrayGetCount
CFArrayGetCount.argtypes = [CFArrayRef]
CFArrayGetCount.restype = CFIndex

CFArrayGetValueAtIndex = MultitouchSupport.CFArrayGetValueAtIndex
CFArrayGetValueAtIndex.argtypes = [CFArrayRef, CFIndex]
CFArrayGetValueAtIndex.restype = ctypes.c_void_p

MTDeviceCreateList = MultitouchSupport.MTDeviceCreateList
MTDeviceCreateList.argtypes = []
MTDeviceCreateList.restype = CFMutableArrayRef

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

MTDataRef = ctypes.POINTER(MTData)

MTContactCallbackFunction = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, 
    MTDataRef, ctypes.c_int, ctypes.c_double, ctypes.c_int)

MTDeviceRef = ctypes.c_void_p

MTRegisterContactFrameCallback = MultitouchSupport.MTRegisterContactFrameCallback
MTRegisterContactFrameCallback.argtypes = [MTDeviceRef, MTContactCallbackFunction]
MTRegisterContactFrameCallback.restype = None

MTDeviceStart = MultitouchSupport.MTDeviceStart
MTDeviceStart.argtypes = [MTDeviceRef, ctypes.c_int]
MTDeviceStart.restype = None

MTDeviceStop = MultitouchSupport.MTDeviceStop
MTDeviceStop.argtypes = [MTDeviceRef]
#MTDeviceStop.restype = None

def _cfarray_to_list(arr):
    rv = []
    n = CFArrayGetCount(arr)
    for i in xrange(n):
        rv.append(CFArrayGetValueAtIndex(arr, i))
    return rv


def init_multitouch(cb):
    devices = _cfarray_to_list(MultitouchSupport.MTDeviceCreateList())
    for device in devices:
        MTRegisterContactFrameCallback(device, cb)
        MTDeviceStart(device, 0)
    return devices

def stop_multitouch(devices):
    for device in devices:
        MTDeviceStop(device)

@MTContactCallbackFunction
def touch_callback(device, data_ptr, n_fingers, timestamp, frame):
    fingers = []
    for i in xrange(n_fingers):
        fingers.append(data_ptr[i])
    touches[:] = [(frame, timestamp, fingers)]
    return 0


touches_lock = threading.Lock()
touches = []

devs = init_multitouch(touch_callback)


fingers = []

while True:
    if touches:
        frame, timestamp, fingers = touches.pop()

    if (len(fingers) > 1):
        break
    #print frame, timestamp

    for i, finger in enumerate(fingers):
        pos = finger.normalized.position
        vel = finger.normalized.velocity

        x = pos.x
        y = pos.y
        p = (x, y)
        print "finger", i, "at", (x, y)

    time.sleep(0.01)

stop_multitouch(devs)