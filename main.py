"""
main.py
~~~~~~~~~~~~~~~


"""


# 15-112 module
from eventBasedAnimation import Animation

import multitouch
import model
from time import sleep
import knn
import process



class MainWindow(Animation):

    def onInit(self):
        self.windowTitle = "Character Recognition"
        self.trackpad = multitouch.VisualTrackpad(0, 0, self.width, self.height)
        self.recognition = Recognition(560, 0, 140, self.height, 4)



    def onKey(self, event):
        if (event.keysym == "space"):
            if (self.trackpad.isDrawing == False):
                self.trackpad.isDrawing = True
                self.trackpad.start()
            else:
                self.trackpad.isDrawing = False
                self.trackpad.stop()



    def onDraw(self, canvas):
        self.trackpad.draw(canvas)
        self.recognition.draw(canvas)



    def onStep(self):
        self.recognition.instanceData = self.trackpad.touchData
        self.recognition.step()
        
    


    def onMouse(self, event):
        self.recognition.onMouse(event)



    def onMouseMove(self, event): pass
    def onMouseDrag(self, event): pass
    def onKeyRelease(self, event): pass
    def onQuit(self): pass




class Recognition(object):
    """Recognition(x, y, width, height, n)
    n is the number of suggestion boxes"""

    def __init__(self, x, y, width, height, n):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.n = n
        self.initButtons()
        self.initModel()
        self.instanceData = []          # data to be classified
        self.processor = process.Feature()
        self.proportions = dict()

    def initButtons(self):
        """Initializes n suggestion boxes"""
        self.buttons = []
        x0 = self.x
        width = self.width
        height = self.height / self.n
        for i in xrange(self.n):
            y0 = height * i
            self.buttons.append(Button(x0, y0, width, height))

    def initModel(self):
        """Initializes a Model class for knn"""
        self.knnModel = model.Model("test_model_10", 4)        

    def draw(self, canvas):
        for button in self.buttons:
            button.draw(canvas)
        self.drawLines(canvas)

    def drawLines(self, canvas):
        """Draws separators"""
        x0, x1 = self.x, self.x + self.width
        buttonHeight = self.height / self.n
        for i in xrange(1, self.n):
            y = buttonHeight * i
            canvas.create_line(x0, y, x1, y, fill="lightgrey")

    def step(self):
        """Perform knn on the current instanceData"""
        k = 10      # use 10 nearest points
        self.processor.update(self.instanceData)
        instance = self.processor.feature
        self.proportions = self.knnModel.kNearestNeighborProportions(instance, k)
        self.updateLabels()
        for button in self.buttons:
            button.step()

    def updateLabels(self):
        """Finds the top n matches in self.proportions and sets the correct
        box labeling."""
        labels = knn.topNClasses(self.proportions, self.n)
        for i in xrange(len(labels)):
            label, subLabel = labels[i]
            self.buttons[i].label = label
            self.buttons[i].subLabel = subLabel
        # reset remaining labels
        for i in xrange(len(labels), self.n):
            self.buttons[i].label = ""
            self.buttons[i].subLabel = ""


    def onMouse(self, event):
        for button in self.buttons:
            button.intersect(event.x, event.y)






class Button(object):
    """Button(x, y, width, height[, **kws])"""

    def __init__(self, x, y, width, height, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = self.width / 10
        self.fg = "#1a1a1a"             # foreground color: dark grey
        self.bg = "#e5e6e6"             # background color: light grey
        self.activeColor = "#d5e5f8"    # active color: light blue
        self.label = ""
        self.subLabel = ""
        self.clickTimer = 0
        self.__dict__.update(kwargs)

    def draw(self, canvas):
        x0 = self.x
        x1 = x0 + self.width
        y0 = self.y
        y1 = y0 + self.height
        color = self.bg if self.clickTimer == 0 else self.activeColor
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
        cx = x0 + self.width / 2
        cy = y0 + self.height / 2
        font = "Arial " + str(self.width / 5)
        canvas.create_text(cx, cy, anchor="center", fill=self.fg,
                           text=self.label, font=font)
        cy2 = y1 - self.margin
        font2 = "Arial " + str(self.width / 12)
        canvas.create_text(cx, cy2, anchor="center", fill=self.fg,
                           text=self.subLabel, font=font2)

    def intersect(self, x, y):
        if ((self.x < x and x < self.x + self.width) and
            (self.y < y and y < self.y + self.height)):
            self.clicked(1)

    def clicked(self, time):
        """Reset click timer"""
        self.clickTimer = time

    def step(self):
        """Count down click timer."""
        if (self.clickTimer > 0):
            self.clickTimer -= 1







width = 700
height = 400
margin = 25
timerDelay = 64
mainWindow = MainWindow(
    width=width, height=height, margin=margin, timerDelay=timerDelay)
mainWindow.run()

























