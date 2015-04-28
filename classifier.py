"""
classifier.py
~~~~~~~~~~~~~~~
The Classifier class handles touch input and recognition using kNN. The only
input device used is the trackpad. Selecting suggested characters, clearing
input, etc. are handled by tapping the sides of the trackpad, which are mapped
to buttons in the GUI.



"""


# Standard libraries
import time

# 15-112 libraries
from eventBasedAnimation import Animation

# Packaged libraries 
import knn
import model
import mouse
import process
import multitouch



class Classifier(object):
    """Frame that includes trackpad input and recognition tools.

    The draw() and step() methods must be called for proper functionality.
    Button clicks are handled by the click() method.

    Args:
        x (int): X position in main frame.
        y (int): Y position in main frame.
        width (int): Width in pixels.
        height (int): Height in pixels.
        model (str): Name of classification model.
        state (str, optional): Either 'active' or 'inactive'.

    Attributes:
        result (str or None): The character picked by the user.
        panelSize (int): Pixel size of each of the two panels.

    """
    def __init__(self, x, y, width, height, model, state="active"):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.state = state
        self.panelSize = self.width / 6
        self.trackpad = RecognitionTrackpad(
            self.x + self.panelSize,                # x
            self.y,                                 # y
            self.width - 2 * self.panelSize,        # width
            self.height,                            # height
            model, 11)                    # model and dimensions
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
        self.updateButtons()

    def reset(self):
        self.trackpad.reset()
        self.updateButtons()
    
    def click(self, (normx, normy)):
        x = self.x + self.width * normx
        y = self.y + self.height - self.height * normy
        for button in (self.settings.buttons + self.recognition.buttons):
            if (button.intersect(x, y) == True):
                button.highlight(0)
                self.result = button.value
                self.trackpad.reset()

    def hover(self, (normx, normy)):
        """highlights the button being hovered over."""
        x = self.x + self.width * normx
        y = self.y + self.height - self.height * normy
        for button in (self.settings.buttons + self.recognition.buttons):
            if (button.intersect(x, y) == True):
                button.highlight(1)

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
                button.value = ""
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
        bounds (float): the proportion of the trackpad that constitutes a
            touch click.
        clickAreaData (3 - tuple):
            x (float): Normalized x position.
            y (float): Normalized y position.
            time (float): System time.
        results (dict): Contains sym:proportion for the kth Nearest Neighbors.

    """
    def __init__(self, x, y, width, height, modelName, dimensions):
        super(RecognitionTrackpad, self).__init__(x, y, width, height)
        self.processor = process.Feature()
        self.recogModel = model.Model(modelName, dimensions)
        self.bounds = 1.0 / 6.0      # area of click area on each side
        self.clickAreaData = None
        self.results = dict()

    def touch_callback(self, device, data_ptr, n_fingers, timestamp, frame):
        """Overrides touch_callback() in Parent.

        Appends points to touchData if the touch lies inbetween the bounds.
        Otherwise, most recent point is added to clickAreaData.
        """
        data = data_ptr[0]      # only use the first finger
        pos = data.normalized.position
        p = (pos.x, pos.y, timestamp)
        if (pos.x > self.bounds and pos.x < 1.0 - self.bounds):
            self.touchData.append(p)    
            self.lastTouch = p[:2] + (time.time(),)
        else:
            self.clickAreaData = p[:2] + (time.time(),)
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
    """Set of Button objects.

    Args:
        x (int): X position of left side of Panel.
        y (int): Y position of top of Panel.
        width (int): Width.
        height (int): Height.
        numButtons (int): Number of vertical buttons in the Panel.

    Attributes:
        buttons (list): Collection of Button objects.
        numButtons (int)

    """
    def __init__(self, x, y, width, height, numButtons):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.numButtons = numButtons
        self.initButtons()
    
    def initButtons(self):
        self.buttons = []
        x0 = self.x
        width = self.width
        height = self.height / self.numButtons
        for i in xrange(self.numButtons):
            y0 = self.y + height * i
            self.buttons.append(Button(x0, y0, width, height, outline=True))

    def draw(self, canvas):
        for button in self.buttons:
            button.draw(canvas)
    
    def step(self):
        for button in self.buttons:
            button.step()


class Settings(Panel):

    def __init__(self, x, y, width, height, numButtons):
        super(Settings, self).__init__(x, y, width, height, numButtons)
        self.initButtonLabels()
        self.initButtonColors()

    def initButtonLabels(self):
        self.buttons[0].label = "C"
        self.buttons[0].value = "clear"
        self.buttons[1].label = "AC"
        self.buttons[1].value = "allClear"
        self.buttons[2].label = "123"
        self.buttons[2].value = "switch"
        self.buttons[3].label = "="
        self.buttons[3].value = "equals"

    def initButtonColors(self):
        """Equals gets a different color"""
        self.buttons[3].fg = "#ffffff"
        self.buttons[3].bg = "#f79332"
        self.buttons[3].activeColor = "#c36c18"



class Button(object):
    """Standard clickable Button object.

    Args:
        x (int): X position.
        y (int): Y position.
        width (int): Width.
        height (int): Height.
        kwargs: Can be used to override default labels.

    Attributes:
        label (str): Primary label, displayed in larger font.
        subLabel (str): Secondary label, displayed in smaller font.
        value (str): Operator or stored value of button, which sometime differs
            from its label.

    """
    def __init__(self, x, y, width, height, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.margin = self.width / 15
        self.fg = "#1a1a1a"             # foreground color: dark grey
        self.bg = "#e5e6e6"             # background color: light grey
        self.activeColor = "#d5e5f8"    # active color: light blue
        self.label = ""
        self.subLabel = ""
        self.value = ""
        self.clickTimer = 0
        self.mainFont = ("Helvetica Neue Light", str(self.width / 5))
        self.subFont = ("Helvetica Neue Light", str(self.width / 12))
        self.outline = False
        self.__dict__.update(kwargs)

    def draw(self, canvas):
        x0 = self.x
        x1 = x0 + self.width
        y0 = self.y
        y1 = y0 + self.height
        color = self.bg if self.clickTimer == 0 else self.activeColor
        width = 0 if self.outline == False else 1
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=width,
                                outline="lightgrey")
        cx = x0 + self.width / 2
        cy = y0 + self.height / 2
        canvas.create_text(cx, cy, anchor="center", fill=self.fg,
                           text=self.label, font=self.mainFont)
        cy2 = y1 - self.width / 10
        canvas.create_text(cx, cy2, anchor="center", fill=self.fg,
                           text=self.subLabel, font=self.subFont)

    # def intersect(self, x, y):
    #     if ((self.x < x and x < self.x + self.width) and
    #         (self.y < y and y < self.y + self.height)):
    #         return True
    #     else:
    #         return False

    def intersect(self, x, y):
        """Test collision of pixel location with button.

        Registers as collision if touchPoint is within a certain padding from
        the actual border. This helps prevents false touches.

        Args:
            x (int): Pixel x location.
            y (int): Pixel y location.

        Returns:
            True if (x, y) is contained within the margin of the button,
                False otherwise

        """
        if ((self.x + self.margin < x) and 
            (x < self.x + self.width - self.margin) and
            (self.y + self.margin < y) and
            (y < self.y + self.height - self.margin)):
            return True
        else:
            return False

    def highlight(self, time):
        """Reset click timer"""
        self.clickTimer = time

    def step(self):
        """Count down click timer."""
        if (self.clickTimer > 0):
            self.clickTimer -= 1





if __name__ == "__main__":
    width = 700
    height = 300
    class ClassifierWindow(Animation):
        def onInit(self):
            self.classifier = Classifier(0, 0, width, height)
        def onDraw(self, canvas):
            self.classifier.draw(canvas)
        def onStep(self):
            self.classifier.step()
            mouse.mouseMove(10, 50)     # reset position
            mouse.hideCursor()
    timerDelay = 64
    mainWindow = ClassifierWindow(
        width=width, height=height, timerDelay=timerDelay)
    mainWindow.run()
