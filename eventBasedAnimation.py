# eventBasedAnimation.py
# David Kosbie
EVENT_BASED_ANIMATION_VERSION = "1.07"

# change log
# 02-15-15 - 02-19-15: v1.03 - 1.07: DK:
#   * various bug fixes (+/-/>/< work, reset works)
#   * no pause on reset
#   * added help (ctrl-h) and about (ctrl-a / data.aboutText) dialogs
#   * added data.windowTitle
#   * require importing (no including framework in animation file)
#   * allow non-json-serializable types (like PhotoImage) in data. fields
#   * add motion and mouse released and key released events
#   * Error to add Canvas instance to data.foo
#   * Pretty-printed data.__str__() method for debugging aid
#   * Display errMsg in canvas on error/exception
# 02-14-15: v1.02: DK:
#   * Added MVC checking
#     * Error to write to data.foo in draw fn
#     * Error to access canvas.foo outside draw fn
# 02-09-15: v1.01: DK:
#   created, based on stepAnimation version 1.03
#   added MVC-friendly features:
#     * separated canvas and data (so it's just data, not canvas.data)
#     * only provide canvas or data as needed to functions
#     * controller does not get the draw function, so can't call it directly
#     * view (draw function) fails on setting write fields

from Tkinter import *
import sys
import traceback
import json
import random
import tkMessageBox

class Struct(object): pass

def makeReadOnlyStruct():
    _readOnly = [False] # do not place in struct!
    _dumpsCheck = [None]
    class ReadOnlyStruct(object):
        def setReadOnly(self, readOnly=True, useDumpsCheck=True):
            # use bogus default fn to hush json errors for unknown types
            to_json = lambda pythonObject: ""
            _readOnly[0] = readOnly
            if (useDumpsCheck == True):
                if readOnly:
                    _dumpsCheck[0] = json.dumps(self.__dict__, default=to_json)
                else:
                    oldDump = _dumpsCheck[0]
                    newDump = json.dumps(self.__dict__, default=to_json)
                    if (oldDump != newDump):
                        field = ""
                        (d1, d2) = (json.loads(oldDump), json.loads(newDump))
                        for key in d1:
                            if (d1[key] != d2[key]):
                                field = "." + key
                                break
                        raise Exception("Error: draw fn modified data" + field)
        def isReadOnly(self): return _readOnly[0]
        def __setattr__(self, name, value):
            if self.isReadOnly():
                raise Exception("Error: draw fn tried to set data." + name)
            if (isinstance(value, Canvas)):
                raise Exception("Error: do not create your own Canvas!")
            return object.__setattr__(self, name, value)
        def __str__(self):
            result = ""
            for key in sorted(self.__dict__.keys()):
                if (result != ""): result += "\n"
                result += "  %s: %s" % (key, self.__dict__[key])
            banner = "******************"
            return banner + "\nData fields:\n" + result + "\n" + banner
    return ReadOnlyStruct()

class BlockableCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        self._blocked = False
        return Canvas.__init__(self, *args, **kwargs)
    def setBlocked(self, blocked):
        self._blocked = blocked
    def __getattr__(self, name):
        if (self._blocked == True):
            raise Exception("Error accessing canvas while not in draw fn")
        return Canvas.__getattr__(self, name)

def run(initFn=None, mouseFn=None, keyFn=None, stepFn=None, drawFn=None,
        mouseMoveFn=None, mouseDragFn=None, mouseReleaseFn=None,
        keyReleaseFn=None,
        width=300, height=300, timerDelay=128,
        mvcCheckFrequency=1.0, **kwargs):

    assert(0 <= mvcCheckFrequency <= 1.0)
    # make sure no user modules defined in this module
    # (so users must import this module from external file)
    if (run.__module__ == "__main__"):
        raise Exception("run in main module (must import eventBasedAnimation)")
    for fn in [initFn, mouseFn, keyFn, stepFn, drawFn]:
        if ((fn != None) and (fn.__module__ == run.__module__)):
            errMsg = ("run in same module as %s" +
                      " (must import eventBasedAnimation)")
            raise Exception(errMsg % (fn.__name__))

    data = Struct()

    def reset():
        data.userData = makeReadOnlyStruct()
        data.userData.width = width
        data.userData.height = height
        data.userData.timerDelay = timerDelay # milliseconds
        data.userData.step = -1
        data.userData.__dict__.update(kwargs)
        data.isRunning = True
        data.errMsg = None

    def linewrap(s, maxPerLine):
        result = ""
        while (len(s) > maxPerLine):
            i = s.rfind(" ", 0, maxPerLine)
            if (i == -1): i = maxPerLine
            result += s[:i].strip() + "\n"
            s = s[i:]
        return result + s.strip()

    def callAnimationFn(fn, *args):
        try:
            if (fn != None):
                fn(*args)
        except Exception as error:
            print "***************\nError:", error
            traceback.print_exc(file=sys.stdout)
            data.isPaused = True
            data.errMsg = str(error)
            redrawAll()

    def redrawErrMsg():
        data.canvas.delete(ALL)
        data.canvas.setBlocked(False)
        msg = (linewrap(data.errMsg, 40) +
               "\nSee console for stack trace." + 
               "\nPress ctrl-r to reset.")
        data.canvas.create_text(width/2, height/4,
                                text=msg, font="Arial 16 bold", fill="red",
                                justify=LEFT)
        data.canvas.setBlocked(True)

    def redrawAll():
        data.canvas.delete(ALL)
        doMvcCheck = (random.random() <= mvcCheckFrequency)
        try:
            try:
                if (doMvcCheck): data.userData.setReadOnly(True)
                data.canvas.setBlocked(False)
                if (data.errMsg):
                    redrawErrMsg()
                else:
                    callAnimationFn(drawFn, data.canvas, data.userData)
            finally:
                data.canvas.setBlocked(True)
                if (doMvcCheck): data.userData.setReadOnly(False)
        except Exception as error:
            print "***************\nError:", error
            traceback.print_exc(file=sys.stdout)
            data.isPaused = True
            data.errMsg = str(error)
            redrawErrMsg()

    def doStep():
        data.userData.step += 1
        callAnimationFn(stepFn, data.userData)
        redrawAll()

    def doCommand(command):
        if (command == "go"): data.isPaused = False
        elif (command == "pause"): data.isPaused = True
        elif (command == "step"): data.isPaused = True; doStep()
        elif (command == "reset"):
            reset()
            callAnimationFn(initFn, data.userData)
            doStep()
        #elif (command == "jump"): doJump()
        elif (command == "+faster"):
            data.userData.timerDelay = max(1, data.userData.timerDelay/2)
        elif (command == "-slower"):
            data.userData.timerDelay = 2*data.userData.timerDelay
        elif (command == "help"): doHelp()
        elif (command == "about"): doAbout()
        elif (command == "quit"): quit()
        else:
            raise Exception("Unknown command: " + command)

    def onMousePressedWrapper(event):
        if (not data.isRunning): return        
        callAnimationFn(mouseFn, event, data.userData)

    def onMouseMovedWrapper(event):
        if (not data.isRunning): return        
        callAnimationFn(mouseMoveFn, event, data.userData)

    def onMouseDraggedWrapper(event):
        if (not data.isRunning): return        
        callAnimationFn(mouseDragFn, event, data.userData)

    def onMouseReleasedWrapper(event):
        if (not data.isRunning): return        
        callAnimationFn(mouseReleaseFn, event, data.userData)

    def showMessageBox(title, msg):
        paused = data.isPaused
        data.isPaused = True
        tkMessageBox.showinfo(title, msg, parent=data.root)
        data.isPaused = paused

    def doAbout():
        msg = "About:\n"
        try:
            userAboutText = str(data.userData.aboutText)
            msg += " ----------------------------\n"
            msg += userAboutText + "\n"
            msg += " ----------------------------\n"
        except: pass
        msg += "  eventBasedAnimation version %s\n" % (
                  EVENT_BASED_ANIMATION_VERSION)
        msg += "  by David Kosbie for 15-112\n"
        msg += "  see: www.cs.cmu.edu/~112"
        showMessageBox("Help", msg)

    def doHelp():
        msg =  "Help:\n"
        msg += "  Commands:\n"
        for key in commandMap:
            msg += "    ctrl-%c: %s\n" % (key, commandMap[key])
        showMessageBox("Help", msg)

    commandMap = {
        "g":"go", "p":"pause", "s":"step", "r":"reset",
        #"j":"jump",
        "+":"+faster", "-":"-slower", 
        "h":"help",
        "a":"about",
        "q":"quit"
    }

    commandAliasMap = {
        "plus":"+", "equal":"+", ">":"+", "greater":"+", "period":"+",
        "minus":"-", "underscore":"-", "<":"-", "less":"-", "comma":"-",
        "question":"h", "slash":"h"
    }

    def onKeyPressedWrapper(event):
        if (not data.isRunning): return
        ctrlPressed = bool(event.state & 0x4)
        if (ctrlPressed == True) and (event.keysym not in [None, ""]):
            ch = event.keysym
            if (ch in commandAliasMap):
                ch = commandAliasMap[ch]
            if (ch in commandMap):
                doCommand(commandMap[ch])
        else:
            callAnimationFn(keyFn, event, data.userData)

    def onKeyReleasedWrapper(event):
        if (not data.isRunning): return        
        callAnimationFn(keyReleaseFn, event, data.userData)

    def onTimerFiredWrapper():
        if (not data.isRunning): data.root.destroy(); return
        if (not data.isPaused): doStep()
        data.canvas.after(data.userData.timerDelay, onTimerFiredWrapper)         

    def quit():
        if (not data.isRunning): return
        data.isRunning = False
        if (data.runningInIDLE):
            # in IDLE, must be sure to destroy here and now
            data.root.destroy()
        else:
            # not IDLE, then we'll destroy in the canvas.after handler
            data.root.quit()

    def runAnimation():
        print "eventBasedAnimation version %s" % (
                  EVENT_BASED_ANIMATION_VERSION)
        print "Press ctrl-h for help / see list of commands."
        reset()
        data.isPaused = False
        data.root = Tk()
        data.root.configure(bg="gray")
        data.canvas = BlockableCanvas(data.root,
                             width=data.userData.width,
                             height=data.userData.height)
        data.canvas.pack()
        data.canvas.setBlocked(True)
        data.root.protocol("WM_DELETE_WINDOW", lambda: quit())
        data.runningInIDLE =  ("idlelib" in sys.modules)
        bindings = [("<Motion>"          , onMouseMovedWrapper),
                    ("<Button-1>"        , onMousePressedWrapper),
                    ("<B1-Motion>"       , onMouseDraggedWrapper),
                    ("<B1-ButtonRelease>", onMouseReleasedWrapper),
                    ("<Key>"             , onKeyPressedWrapper),
                    ("<KeyRelease>"      , onKeyReleasedWrapper)
                    ]
        for (event, handlerFn) in bindings:
            data.root.bind(event, handlerFn)
        callAnimationFn(initFn, data.userData)
        data.root.wm_title(data.userData.__dict__.get("windowTitle",
                                             "eventBasedAnimation"))
        onTimerFiredWrapper()
        data.root.mainloop()

    runAnimation()

"""
import eventBasedAnimation

##########################
# example usage:
##########################

def sweepingBallInitFn(data):
    data.aboutText = "Sweeping Ball Demo by DK!"
    data.windowTitle = "Sweeping Ball Demo"
    data.x = data.width/2
    data.y = data.height/2

def sweepingBallKeyFn(event, data):
    if (event.keysym == "Up"):
        data.y = (data.y - 25) % data.height
    elif (event.keysym == "Down"):
        data.y = (data.y + 25) % data.height

def sweepingBallMouseFn(event, data):
    (data.x, data.y) = (event.x, event.y)

def sweepingBallStepFn(data):
    data.x = (data.x + 10) % data.width

def sweepingBallDrawFn(canvas, data):
    (cx, cy, r) = (data.x, data.y, 20)
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="blue")
    canvas.create_text(data.width/2, 20,
                       text="Try up/down keys + mouse press anywhere")

eventBasedAnimation.run(
    initFn=sweepingBallInitFn,
    stepFn=sweepingBallStepFn,
    mouseFn=sweepingBallMouseFn,
    keyFn=sweepingBallKeyFn,
    drawFn=sweepingBallDrawFn,
    timerDelay=100,
    )

##########################
# error demos:
##########################

# Fail case #1: creating a new data field in a draw fn
def drawFnWithModelWriteError1(canvas, data):
    data.foo = "this should fail!"
eventBasedAnimation.run(drawFn=drawFnWithModelWriteError1)

# Fail case #2: modifying a mutable data field in a draw fn
def initFn(data):
    data.foo = [42]
def drawFnWithModelWriteError2(canvas, data):
    data.foo[0] = "this should fail!"
eventBasedAnimation.run(initFn=initFn, drawFn=drawFnWithModelWriteError2)

# Fail case #3: saving canvas to global and trying to draw in an event fn
canvas_as_global = None
def stepFnCanvasAsGlobalError(data):
    if (canvas_as_global != None):
        msg = "This should fail, using a global canvas from a stepFn!"
        canvas_as_global.create_text(data.width/2, data.height/2, text=msg)
        canvas_as_global.update()
def drawFnCanvasAsGlobalError(canvas, data):
    canvas.create_oval(10, 10, 20, 20, fill="blue")
    global canvas_as_global
    canvas_as_global = canvas
eventBasedAnimation.run(drawFn=drawFnCanvasAsGlobalError,
                        stepFn=stepFnCanvasAsGlobalError)
"""
