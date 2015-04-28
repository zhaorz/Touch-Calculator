"""
touchCalculator.py
~~~~~~~~~~~~~~~
The touchCalculator class provides a calculator implementation for use with
trackpads.

An instance of Calculator is self-drawing and interactive. For best results,
only have one instance of either Calculator or Classifier active at the same
time. On initialization, state defaults to "active".

"""

# 15-112 module
from eventBasedAnimation import Animation

# Standard libraries
import time

# Packaged libraries
import mouse
import multitouch

# UI elements
from classifier import RecognitionTrackpad
from classifier import Panel
from classifier import Settings
from classifier import Button



class Calculator(object):
    """Frame that includes calculator keys, operators, and settings.

    The draw() and step() methods must be called for proper functionality.
    Mouse is anchored by default at top left corner of the frame.
    Button clicks are handled by the click() method.

    Args:
        x (int): X position in main frame.
        y (int): Y position in main frame.
        width (int): Width in pixels.
        height (int): Height in pixels.
        state (str, optional): Must be either "active" or "inactive".

    Attributes:
        result (str or None): Current button click. Read by main.
        panelSize (int): Pixel size of each of the two panels.

    """
    def __init__(self, x, y, width, height, state="active"):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.state = state
        self.panelSize = self.width / 6
        self.trackpad = CalculatorTrackpad(
            self.x + self.panelSize,                # x
            self.y,                                 # y
            self.width,                             # width
            self.height)                            # height
        self.calculator = CalculatorButtons(
            self.x + self.panelSize,
            self.y,
            self.width - self.panelSize,
            self.height)
        self.settings = Settings(
            self.x,                                 # x
            self.y,                                 # y
            self.panelSize,                         # width
            self.height,                            # height
            4)                                      # numButtons
        self.settings.buttons[2].label = "draw"     # switch label
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
                print "click", button.value
                self.result = button.value
                self.trackpad.reset()

    def hover(self, (normx, normy)):
        """Highlights the button being hovered over."""
        x = self.x + self.width * normx
        y = self.y + self.height - self.height * normy
        for button in (self.settings.buttons + self.calculator.buttons):
            if (button.intersect(x, y) == True):
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
    """Underfeatured version of RecognitionTrackpad.

    Only keeps track of one data point, the most recent one. The data point
    contains system time, which is used to calculate touch clicks.
    Width and height are noncritical because this trackpad isn't drawn.
    
    Args:
        x (int): Left canvas coordinate (in pixels).
        y (int): Top canvas coordinate.
        width (int): Width of the trackpad.
        height (int): Height of the trackpad.

    Attributes:
        clickAreaData (tuple): Contains normalized x and y and a system time.

    """
    def __init__(self, x, y, width, height):
        super(RecognitionTrackpad, self).__init__(x, y, width, height)
        self.clickAreaData = None

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
    """A collection of self-drawing buttons for the calculator.

                | 7 | 8 | 9 |
                | 4 | 5 | 6 |
                | 1 | 2 | 3 |
                |   0   | . |

    Args:
        x (int): Left canvas coordinate (in pixels).
        y (int): Top canvas coordinate.
        width (int): Width of only the buttons and operators (no settings).
        height (int): Height of the frame.

    Attributes:
        buttons (list): List of Button objects.

    """
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.numbers = self.initNumbers()
        self.ops = self.initOperators()
        self.buttons = self.numbers + self.ops

    def initNumbers(self):
        buttons = []
        buttonWidth = self.width * 4 / 15
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
        buttons = []
        buttonWidth = self.width / 5
        buttonHeight = self.height / 4
        x = self.x + self.width - buttonWidth
        labels = [u'\u00f7', u'\u00d7', '-', '+']
        values = ['/', '*', '-', '+']
        font = ("Helvetica Neue Light", "26")
        for i in xrange(4):
            y = self.y + i * buttonHeight
            buttons.append(Button(x, y, buttonWidth, buttonHeight,
                                  mainFont=font, outline=True, label=labels[i],
                                  value=values[i], fg="#ffffff", bg="#f79332",
                                  activeColor="#c36c18"))
        return buttons


    def draw(self, canvas):
        for button in self.buttons:
            button.draw(canvas)

    def step(self):
        for button in self.buttons:
            button.step()



if __name__ == "__main__":
    width = 690
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
