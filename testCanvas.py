"""
testCanvas.py
~~~~~~~~~~~~~~~

Basic implementation of eventBasedAnimation to help with testing.

testCanvas class should be initialized with a single keyword argument
named points. points should be a list with elements that are tuples
of form (x, y, time).

"""


import eventBasedAnimation
from time import sleep
from random import randint


class TestWindow(eventBasedAnimation.Animation):

    def onInit(self):
        self.windowTitle = "Test Canvas"
        self.drawWidth = self.width - self.margin * 2
        self.drawHeight = self.height - self.margin * 2
        self.darkGrey = "#4A4A4A"
    
    def onDraw(self, canvas):
        self.drawBackground(canvas)
        self.drawPoints(canvas)

    def drawBackground(self, canvas):
        x0 = self.margin
        x1 = self.width - self.margin
        y0 = self.margin
        y1 = self.height - self.margin
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)

    def drawPoints(self, canvas):
        for (x, y, time) in self.points:
            cx = self.margin + x * self.drawWidth
            cy = self.height - self.margin - y * self.drawHeight
            self.drawDot(canvas, cx, cy, 5, self.darkGrey)

    def drawDot(self, canvas, cx, cy, r, color="black"):
        x0 = cx - r
        x1 = cx + r
        y0 = cy - r
        y1 = cy + r
        canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)
