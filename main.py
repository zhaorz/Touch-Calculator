import trackpad
import eventBasedAnimation


###########################################


def initFn(data):
    (data.trackpadWidth, data.trackpadHeight) = (668, 484)
    data.strokes = []
    data.drawing = False
    data.trackpad = trackpad.trackpad()


###########################################


def stepFn(data):
    pass


###########################################


def mouseMoveFn(event, data):
    if (data.drawing == True):
        data.strokes.append(data.trackpad.stroke())
        print len(data.strokes)

###########################################


def keyFn(event, data):
    # toggle drawing
    if (event.keysym == 'space'):
        data.drawing = not data.drawing
        print data.drawing
    # clear
    elif (event.keysym == 'r'):
        data.strokes = []



###########################################


def drawFn(canvas, data):
    drawTrackpad(canvas, data)
    drawToggle(canvas, data)

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
    for stroke in data.strokes:
        drawStroke(canvas, data, stroke)

def drawStroke(canvas, data, stroke):
    left = data.width / 2 - data.trackpadWidth / 2
    top = data.height / 2 - data.trackpadHeight / 2
    r = 10
    for (normx, normy) in stroke:
        x = left + normx * data.trackpadWidth
        y = data.height - (top + normy * data.trackpadHeight)
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