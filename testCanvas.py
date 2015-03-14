"""
testCanvas.py
~~~~~~~~~~~~~~~

Basic implementation of eventBasedAnimation to help with testing

"""


import eventBasedAnimation
from time import sleep
from random import randint


###########################################


def initFn(data):
    data.windowTitle = 'testCanvas'
    (data.trackpadWidth, data.trackpadHeight) = (668, 484)
    data.drawing = False

    data.strokeData = [[(0.2972281873226166, 0.29405677318573), (0.35655108094215393, 0.3580721318721771), (0.3796665668487549, 0.3820224702358246), (0.4037025570869446, 0.4073033630847931), (0.4285568296909332, 0.4340626895427704), (0.45392248034477234, 0.4606741666793823), (0.47990182042121887, 0.4875813126564026), (0.5059834122657776, 0.5150798559188843), (0.5322695970535278, 0.5413956046104431), (0.5581466555595398, 0.5666764974594116), (0.5838191509246826, 0.5913660526275635), (0.608877956867218, 0.6147249937057495), (0.6330162882804871, 0.6358663439750671)]]
    data.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'grey']
    data.drawColor = data.colors[randint(0, len(data.colors) - 1)]


###########################################


def stepFn(data):
    pass


###########################################


def mouseMoveFn(event, data):
    pass


###########################################


def drawFn(canvas, data):
    drawTrackpad(canvas, data)

def drawTrackpad(canvas, data):
    (cx, cy) = (data.width / 2, data.height / 2)
    rx = data.trackpadWidth / 2
    ry = data.trackpadHeight / 2
    x0 = cx - rx
    x1 = cx + rx
    y0 = cy + ry
    y1 = cy - ry
    canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)
    drawStrokes(canvas, data)

def drawStrokes(canvas, data):
    for i in xrange(0, len(data.strokeData)):
        drawStroke(canvas, data, i)

def drawStroke(canvas, data, strokeNum):
    left = data.width / 2 - data.trackpadWidth / 2
    top = data.height / 2 - data.trackpadHeight / 2
    r = 10
    for (normx, normy) in data.strokeData[strokeNum]:
        x = left + normx * data.trackpadWidth
        y = data.height - (top + normy * data.trackpadHeight)
        drawDot(canvas, x, y, r, data.colors[strokeNum])

def drawDot(canvas, cx, cy, r, color='black'):
    x0 = cx - r
    x1 = cx + r
    y0 = cy - r
    y1 = cy + r
    canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)



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
        #keyFn=keyFn,
        width=width, height=height, margin=margin,
        timerDelay=10
    )

run()