"""
testCanvas.py
~~~~~~~~~~~~~~~

Basic implementation of eventBasedAnimation to help with testing.

testCanvas class should be initialized with a single keyword argument
named points. points should be a list with elements that are tuples
of form (x, y, time).

"""


import eventBasedAnimation
from random import randint


class TestWindowPoints(eventBasedAnimation.Animation):
    """TestWindowPoints(points).run() creates a window that draws all a list
    of points."""

    def __init__(self, points):
        super(TestWindowPoints, self).__init__()
        self.points = points

    def onInit(self):
        self.windowTitle = "Test Canvas - points"
    
    def onDraw(self, canvas):
        self.drawPoints(canvas, self.points)

    def drawPoints(self, canvas, points, color="darkgrey"):
        for point in points:
            x, y = point[:2]
            cx = x * self.width
            cy = self.height - y * self.height
            self.drawDot(canvas, cx, cy, 5, color)

    def drawDot(self, canvas, cx, cy, r, color="black"):
        x0 = cx - r
        x1 = cx + r
        y0 = cy - r
        y1 = cy + r
        canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)


class TestWindowStrokes(TestWindowPoints):
    """TestWindowStrokes(strokes).run() creates a window that draws each
    stroke in strokes in a different color. Each strokes is a list of points."""

    def __init__(self, strokes):
        super(TestWindow, self).__init__()
        self.strokes = strokes
        colors = ["red", "orange", "green", "blue", "purple", "darkgrey"]

    def onDraw(self, canvas):
        for i in xrange(len(self.strokes)):
            color = colors[i % len(colors)]
            points = self.strokes[i]
            drawPoints(canvas, points, color)
