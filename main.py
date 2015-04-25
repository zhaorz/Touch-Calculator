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
        self.trackpad = RecognitionTrackpad(140, 0, 560, self.height)
        self.recognition = Panel(700, 0, 140, self.height, 4)
        self.settings = Settings(0, 0, 140, self.height, 4)



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
        self.settings.draw(canvas)



    def onStep(self):
        self.trackpad.step()
        self.updateButtonLabels(self.trackpad.results, self.recognition)
    


    def updateButtonLabels(self, newLabels, panel):
        """Finds the correct labels in newLabels and updates panel buttons.

        Args:
            newLabels (dict): Dictionary of label:confidence pairs.
            panel (Panel): The panel whose buttons are being updated.

        Returns: None

        """
        labels = knn.topNClasses(newLabels, self.recognition.numPanels)
        for i in xrange(len(labels)):
            label, subLabel = labels[i]
            panel.buttons[i].label = label
            panel.buttons[i].subLabel = subLabel
        # reset remaining labels
        for i in xrange(len(labels), self.recognition.numPanels):
            panel.buttons[i].label = ""
            panel.buttons[i].subLabel = ""

    


    def onMouse(self, event):
        self.recognition.onMouse(event)



    def onMouseMove(self, event): pass
    def onMouseDrag(self, event): pass
    def onKeyRelease(self, event): pass
    def onQuit(self): pass


class RecognitionTrackpad(multitouch.VisualTrackpad):

    def __init__(self, x, y, width, height):
        super(RecognitionTrackpad, self).__init__(x, y, width, height)
        self.processor = process.Feature()
        self.recogModel = model.Model("test_model_11", 5)
        self.results = dict()

    def step(self):
        """Perform knn on the current instanceData"""
        k = 10      # use 10 nearest points
        self.processor.update(self.touchData)
        instance = self.processor.feature
        self.results = self.recogModel.modelKNN(instance, k)


class Panel(object):

    def __init__(self, x, y, width, height, numPanels):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.numPanels = numPanels
        self.initButtons()
    
    def initButtons(self):
        self.buttons = []
        x0 = self.x
        width = self.width
        height = self.height / self.numPanels
        for i in xrange(self.numPanels):
            y0 = height * i
            self.buttons.append(Button(x0, y0, width, height))

    def draw(self, canvas):
        for button in self.buttons:
            button.draw(canvas)
        self.drawLines(canvas)

    def drawLines(self, canvas):
        """Draws separators"""
        x0, x1 = self.x, self.x + self.width
        buttonHeight = self.height / self.numPanels
        for i in xrange(1, self.numPanels):
            y = buttonHeight * i
            canvas.create_line(x0, y, x1, y, fill="lightgrey")
    
    def onMouse(self, event):
        for button in self.buttons:
            button.intersect(event.x, event.y)


class Settings(Panel):

    def __init__(self, x, y, width, height, numPanels):
        super(Settings, self).__init__(x, y, width, height, numPanels)
        self.initButtonLabels()

    def initButtonLabels(self):
        self.buttons[0].label = "clear"
        self.buttons[1].label = "_"

    def draw(self, canvas):
        super(Settings, self).draw(canvas)
        self.drawDivider(canvas)

    def drawDivider(self, canvas):
        x = self.x + self.width
        y0 = self.y
        y1 = y0 + self.height
        canvas.create_line(x, y0, x, y1, fill="lightgrey", width=2)





    



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







width = 840
height = 400
margin = 25
timerDelay = 64
mainWindow = MainWindow(
    width=width, height=height, margin=margin, timerDelay=timerDelay)
mainWindow.run()

























