"""
main.py
~~~~~~~~~~~~~~~


"""


import multitouch
import eventBasedAnimation
import featureDetection
from time import sleep


###########################################


def initFn(data):
    data.windowTitle = 'main'
    (data.TrackpadWidth, data.TrackpadHeight) = (668, 484)
    data.drawing = False
    data.Trackpad = multitouch.Trackpad()


###########################################


def stepFn(data):
    pass


###########################################


def mouseMoveFn(event, data):
    pass



###########################################


def keyFn(event, data):
    # toggle drawing
    if (event.keysym == 'space'):
        if (data.drawing == False):
            data.drawing = True
            data.Trackpad.start()
        else:
            data.drawing = False
            data.Trackpad.stop()
            print data.Trackpad.touchData
            #print featureDetection.process(data.Trackpad.touchData)


###########################################


def drawFn(canvas, data):
    drawTrackpad(canvas, data)
    drawToggle(canvas, data)

def drawTrackpad(canvas, data):
    (cx, cy) = (data.width / 2, data.height / 2)
    rx = data.TrackpadWidth / 2
    ry = data.TrackpadHeight / 2
    x0 = cx - rx
    x1 = cx + rx
    y0 = cy + ry
    y1 = cy - ry
    canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)
    drawPoints(canvas, data)

def drawPoints(canvas, data):
    left = data.width / 2 - data.TrackpadWidth / 2
    top = data.height / 2 - data.TrackpadHeight / 2
    r = 10
    for (normx, normy, timestamp) in data.Trackpad.touchData:
        x = left + normx * data.TrackpadWidth
        y = data.height - (top + normy * data.TrackpadHeight)
        drawDot(canvas, x, y, r)

def drawDot(canvas, cx, cy, r, color='black'):
    x0 = cx - r
    x1 = cx + r
    y0 = cy - r
    y1 = cy + r
    canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)

def drawToggle(canvas, data):
    color = 'green' if (data.drawing == True) else 'red'
    drawDot(canvas, 15, 15, 10, color)


###########################################



def run():
    width = 800
    height = 600
    margin = 10
    eventBasedAnimation.run(
        initFn=initFn,
        stepFn=stepFn,
        drawFn=drawFn,
        mouseMoveFn=mouseMoveFn,
        keyFn=keyFn,
        width=width, height=height, margin=margin,
        timerDelay=10
    )

run()