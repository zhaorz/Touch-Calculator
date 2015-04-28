"""
touchCalculator.py
~~~~~~~~~~~~~~~
The touchCalculator class provides a calculator implementation for use with
trackpads.


"""

from eventBasedAnimation import Animation

import time

import knn
import model
import mouse
import process
import multitouch

from classifier import RecognitionTrackpad
from classifier import Panel
from classifier import Settings
from classifier import Button


class Calculator(object):

    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.panelSize = self.width / 6
        self.trackpad = CalculatorTrackpad(
            self.x + self.panelSize,                # x
            self.y,                                 # y
            self.width - 2 * self.panelSize,        # width
            self.height)                            # height
        self.calculator = CalculatorButtons(
            self.x + self.panelSize,
            self.y,
            self.width - 2 * self.panelSize,
            self.height)
        self.settings = Settings(
            self.x,                                 # x
            self.y,                                 # y
            self.panelSize,                         # width
            self.height,                            # height
            4)                                      # numButtons
        self.trackpad.start()
        self.result = None

    def draw(self, canvas):
        self.settings.draw(canvas) 
        self.calculator.draw(canvas)

    def step(self):
        self.settings.step()
        self.calculator.step()
        self.controlMouse()
        self.updateButtons()

    def controlMouse(self):
        """Anchors mouse to top left corner and hides the cursor."""
        mouse.mouseMove(self.x + 10, self.y + 50)     # reset position
        mouse.hideCursor()

    def click(self, (normx, normy)):
        x = self.x + self.width * normx
        y = self.y + self.height - self.height * normy
        for button in (self.settings.buttons + self.calculator.buttons):
            if (button.intersect(x, y) == True):
                button.highlight(0)
                print "click", button.label
                self.result = button.value
                self.trackpad.reset()

    def hover(self, (normx, normy)):
        """highlights the button being hovered over."""
        x = self.x + self.width * normx
        y = self.y + self.height - self.height * normy
        for button in (self.settings.buttons + self.calculator.buttons):
            if (button.intersect(x, y) == True):
                print "highlight", button.label
                button.highlight(1)
   
    def updateButtons(self):
        self.updateButtonClick()

    def updateButtonClick(self):
        # Create local copy of trackpad.clickAreaData
        touchPoint = self.trackpad.clickAreaData
        if (touchPoint != None):
            touchTime = touchPoint[2]
            currentTime = time.time()
            # touch has finished
            if (abs(touchTime - currentTime) > 0.05):
                self.trackpad.clickAreaData = None
                self.click(touchPoint[:2])
            else:   # touch in progress
                self.hover(touchPoint[:2])



class CalculatorTrackpad(RecognitionTrackpad):

    def __init__(self, x, y, width, height):
        super(RecognitionTrackpad, self).__init__(x, y, width, height)
        self.bounds = 1.0 / 6.0      # area of click area on each side
        self.clickAreaData = None
        self.results = dict()

    def touch_callback(self, device, data_ptr, n_fingers, timestamp, frame):
        """Overrides touch_callback() in Parent.

        Only appends data points to clickAreaData. This trackpad doesn't need
        to record touchData.
        """
        data = data_ptr[0]      # only use the first finger
        pos = data.normalized.position
        p = (pos.x, pos.y, timestamp)
        self.clickAreaData = p[:2] + (time.time(),)
        return 0



class CalculatorButtons(object):
    """
     7 | 8 | 9 
     4 | 5 | 6
     1 | 2 | 3
       0   | . 

    """
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.numbers = self.initNumbers()
        self.ops = self.initOperators()
        self.buttons = self.numbers #+ self.ops

    def initNumbers(self):
        buttons = []
        buttonWidth = self.width / 3
        buttonHeight = self.height / 4
        buttonCounter = 0
        font = ("Helvetica Neue Light", "26")
        for row in xrange(2, -1, -1):       # init 1 - 9 first
            for col in xrange(3):
                x = self.x + col * buttonWidth
                y = self.y + row * buttonHeight
                buttons.append(Button(x, y, buttonWidth, buttonHeight,
                                      mainFont=font, outline=True))
                buttons[buttonCounter].label = str(buttonCounter + 1)
                buttons[buttonCounter].value = str(buttonCounter + 1)
                buttonCounter += 1
        zeroButton = Button(
            self.x, self.y + 3 * buttonHeight, 2 * buttonWidth, buttonHeight,
            mainFont=font, outline=True)
        zeroButton.label = zeroButton.value = "0"
        decimalButton = Button(
            self.x + 2 * buttonWidth, self.y + 3 * buttonHeight,
            buttonWidth, buttonHeight, mainFont=font, outline=True)
        decimalButton.label = decimalButton.value = "."
        buttons.extend([zeroButton, decimalButton])
        return buttons

    def initOperators(self):
        pass

    def draw(self, canvas):
        for button in self.numbers:
            button.draw(canvas)

    def step(self):
        for button in self.buttons:
            button.step()



if __name__ == "__main__":
    width = 700
    height = 300
    class CalculatorWindow(Animation):
        def onInit(self):
            self.calculator = Calculator(0, 0, width, height)
        def onDraw(self, canvas):
            self.calculator.draw(canvas)
        def onStep(self):
            self.calculator.step()
    timerDelay = 64
    mainWindow = CalculatorWindow(
        width=width, height=height, timerDelay=timerDelay)
    mainWindow.run()
