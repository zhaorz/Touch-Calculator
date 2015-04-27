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
        self.trackpad = RecognitionTrackpad(
            self.x + self.panelSize,                # x
            self.y,                                 # y
            self.width - 2 * self.panelSize,        # width
            self.height)                            # height
        self.recognition = Panel(
            self.x + self.width - self.panelSize,   # x
            self.y,                                 # y
            self.panelSize,                         # width
            self.height,                            # height
            4)                                      # numButtons
        self.settings = Settings(
            self.x,                                 # x
            self.y,                                 # y
            self.panelSize,                         # width
            self.height,                            # height
            4)                                      # numButtons
        self.trackpad.start()
        self.result = None

    def draw(self, canvas):
        self.trackpad.draw(canvas)
        self.recognition.draw(canvas)
        self.settings.draw(canvas) 

    def step(self):
        self.trackpad.step()
        self.settings.step()
        self.recognition.step()
        self.controlMouse()
        self.updateButtons()

    def controlMouse(self):
        """Anchors mouse to top left corner and hides the cursor."""
        mouse.mouseMove(self.x + 10, self.y + 50)     # reset position
        mouse.hideCursor()

    def click(self, (normx, normy)):
        panel = self.settings if normx < 0.5 else self.recognition
        button = int((1 - normy) * panel.numButtons)
        panel.buttons[button].highlight(0)
        self.result = panel.buttons[button].value
        self.trackpad.reset()

    def hover(self, (normx, normy)):
        """highlights the button being hovered over."""
        panel = self.settings if normx < 0.5 else self.recognition
        button = int((1 - normy) * panel.numButtons)
        panel.buttons[button].highlight(1)
   
    def updateButtons(self):
        self.updateButtonLabels(self.trackpad.results, self.recognition)
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

    def updateButtonLabels(self, newLabels, panel):
        """Finds the correct labels in newLabels and updates panel buttons.

        Args:
            newLabels (dict): Dictionary of label:confidence pairs.
            panel (Panel): The panel whose buttons are being updated.

        Returns: None

        """
        if (self.trackpad.touchData == []):         # empty data
            for button in self.recognition.buttons:
                button.label = ""
                button.subLabel = ""
            return
        labels = knn.topNClasses(newLabels, self.recognition.numButtons)
        for i in xrange(len(labels)):
            label, subLabel = labels[i]
            panel.buttons[i].label = label
            panel.buttons[i].value = label
            panel.buttons[i].subLabel = subLabel
        # reset remaining labels
        for i in xrange(len(labels), self.recognition.numButtons):
            panel.buttons[i].label = ""
            panel.buttons[i].value = ""            
            panel.buttons[i].subLabel = ""

 



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
