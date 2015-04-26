"""
classifier.py
~~~~~~~~~~~~~~~
The Classifier class handles touch input and recognition using kNN. The only
input device used is the trackpad. Selecting suggested characters, clearing
input, etc. are handled by tapping the sides of the trackpad, which are mapped
to buttons in the GUI.



"""


# 15-112 module
from eventBasedAnimation import Animation

# Standard Libraries
import time

# Packaged files 
import knn
import model
import mouse
import process
import multitouch



class Classifier(Animation):


    def onInit(self):
        self.windowTitle = "Character Recognition"
        self.trackpad = RecognitionTrackpad(
            self.panelSize,                     # x
            0,                                  # y
            self.width - 2 * self.panelSize,    # width
            self.height)                        # height
        self.recognition = Panel(
            self.width - self.panelSize,        # x
            0,                                  # y
            self.panelSize,                     # width
            self.height,                        # height
            4)                                  # numPanels
        self.settings = Settings(
            0,                                  # x
            0,                                  # y
            self.panelSize,                     # width
            self.height,                        # height
            4)                                  # numPanels
        self.trackpad.start()

    def onDraw(self, canvas):
        self.trackpad.draw(canvas)
        self.recognition.draw(canvas)
        self.settings.draw(canvas) 

    def onStep(self):
        self.trackpad.step()
        self.updateButtonLabels(self.trackpad.results, self.recognition)
        self.settings.step()
        self.recognition.step()
        self.updateButtonClick()
        self.controlMouse()

    def controlMouse(self):
        mouse.mouseMove(10, 50)     # reset position
        mouse.hideCursor()

    def updateButtonClick(self):
        touchPoint = self.trackpad.clickAreaData
        if (touchPoint != None):
            touchTime = touchPoint[2]
            currentTime = time.time()
            if (abs(touchTime - currentTime) > 0.05):
                print "Clicked", touchPoint
                self.trackpad.clickAreaData = None
                self.click(touchPoint[:2])
            else:
                print "Hover", touchPoint
                self.hover(touchPoint[:2])

    def click(self, (normx, normy)):
        panel = self.settings if normx < 0.5 else self.recognition
        button = int((1 - normy) * panel.numPanels)
        panel.buttons[button].highlight(0)
        if (panel == self.settings and button == 0):     # clear button
            self.trackpad.reset()

    def hover(self, (normx, normy)):
        panel = self.settings if normx < 0.5 else self.recognition
        button = int((1 - normy) * panel.numPanels)
        panel.buttons[button].highlight(1)

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

 
    def onMouse(self, event): pass



    def onMouseMove(self, event): pass
    def onMouseDrag(self, event): pass
    def onKeyRelease(self, event): pass

    def onQuit(self):
        if (self.trackpad.isDrawing == True):
            self.trackpad.stop()
        mouse.showCursor()



class RecognitionTrackpad(multitouch.VisualTrackpad):
    """VisualTrackpad that includes data for touch clicking.

    Main caller uses results of knn to update recognition panel.
    Main caller uses self.clickAreaData to calculate touch clicks.

    Args:
        x (int): Left canvas coordinate (in pixels).
        y (int): Top canvas coordinate.
        width (int): Width of the visual trackpad.
        height (int): Height of the visual trackpad.

    Attributes:
        isDrawing (bool): True if currently receiving input, False otherwise.
        fg (str): foreground color
        bg (str): background color
        active (str): active trackpad color
        highlight (str): highlight color
        results (dict): Contains sym:proportion for the kth Nearest Neighbors.
        bounds (float): the proportion of the trackpad that constitutes a
            touch click.
        clickAreaData (tuple):
            x (float): Normalized x position.
            y (float): Normalized y position.
            time (float): System time.

    """
    def __init__(self, x, y, width, height):
        super(RecognitionTrackpad, self).__init__(x, y, width, height)
        self.processor = process.Feature()
        self.recogModel = model.Model("test_model_11", 5)
        self.results = dict()
        self.bounds = 1.0 / 6.0      # area of click area on each side
        self.clickAreaData = None

    # Override the callback function
    def touch_callback(self, device, data_ptr, n_fingers, timestamp, frame):
        data = data_ptr[0]      # only use the first finger
        pos = data.normalized.position
        p = (pos.x, pos.y, timestamp)
        if (pos.x > self.bounds and pos.x < 1.0 - self.bounds):
            self.touchData.append(p)    
        else:
            self.clickAreaData = (p[:2] + (time.time(),))
        return 0

    def step(self):
        """Perform knn on the current instanceData"""
        k = 10      # use 10 nearest points
        self.processor.update(self.touchData)
        instance = self.processor.feature
        self.results = self.recogModel.modelKNN(instance, k)

    def reset(self):
        del self.touchData[:]
        self.clickAreaData = None



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
    
    def step(self):
        for button in self.buttons:
            button.step()


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
        # self.activeColor = "#d5e5f8"    # active color: light blue
        self.activeColor = "green"
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
            print "clicked!"
            self.highlight(1)

    def highlight(self, time):
        """Reset click timer"""
        self.clickTimer = time

    def step(self):
        """Count down click timer."""
        if (self.clickTimer > 0):
            self.clickTimer -= 1





if __name__ == "__main__":
    width = 840
    height = 400
    panelSize = 140
    timerDelay = 64
    mainWindow = Classifier(
        width=width, height=height, panelSize=panelSize, timerDelay=timerDelay)
    mainWindow.run()
