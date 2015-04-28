"""
main.py
~~~~~~~~~~~~~~~
Touch Calculator

for Mac OS X 10.6+


Richard Zhao 2015
~~~~~~~~~~~~~~~

A calculator with the ability to touch type as well as draw out special
characters. Drawings are recognized using a custom feature detection algorithm
and standard machine learning techniques (namely knn).


Installation:
    All third-party dependencies are included with the source. Touchpad
    frameworks are meant for Mac OS X versions 10.6 and higher.

Getting Started:
    The window opens to touch calculator input at first. The bottom portion
    of the screen is essentially a one-to-one mapping of the physical
    touchpad. Press where the keys are to type. Input is displayed in the top
    input box. Pressing the '=' key evaluates the input.

    Toggle between touch calculator and drawing calculator by pressing either
    '123' or 'draw', the third button down from the left. In drawing mode,
    recognition suggestions appear on the right hand side. Under each match,
    there is a number between 0.0 and 1.0 that indicates the recognition
    confidence.

Training the Classifier:
    The default character set is described in the readme.txt. To train any of
    these characters, uncomment the desired sets in the dataCollection's
    MainWindow class init() function.

    Then, in model.py, load the most recent model, extend it using the new data,
    and save it.

    Adding new characters is similar. First, train them in dataCollection.py.
    Then, add them to the model. Finally, the user must define how to both
    display the character and evaluate them. This is done in evaluate.py.
    In each of the dictionaries, define the desired displayChar mapping and 
    evalChar mapping.

Troubleshooting:
    The classifier is only lightly trained at first. Users have a wide variance
    of handwriting styles. For best results, users should personalize the 
    classifier by performing a few training rounds.

"""


# Standard libraries
import math

# 15-112 libraries
import eventBasedAnimation

# Packaged libraries
import classifier
import calculator
import evaluate
import mouse





class MainWindow(eventBasedAnimation.Animation):

    def onInit(self):
        self.windowTitle = "main"
        self.input = TextDisplay(0, 0, self.width, 100, margin=15,
            font=("Helvetica Neue UltraLight", "48"),
            bgImage=eventBasedAnimation.PhotoImage(file="graphics/top_690.gif"))
        self.output = TextDisplay(
            0, 100, self.width, 150, margin=15,
            font=("Helvetica Neue UltraLight", "80"),
            bgImage=eventBasedAnimation.PhotoImage(file="graphics/bottom_690.gif"))
        self.clsf = classifier.Classifier(0, 250, self.width, 300,
                                          "test_model_23",
                                          state="inactive")
        self.calc = calculator.Calculator(0, 250, self.width, 300,
                                                     state="active")
        self.isPaused = False

    def onStep(self):
        if (self.clsf.state == "active"):
            self.clsf.step()
        else:
            self.calc.step()
        self.getInput()
        if (self.isPaused == False):
            self.controlMouse()

    def controlMouse(self):
        """Anchors mouse to top left corner and hides the cursor."""
        mouse.mouseMove(10, 50)     # reset position
        mouse.hideCursor()

    def getInput(self):
        src = self.clsf if self.clsf.state == "active" else self.calc
        if (src.result != None):
            res = src.result
            if (res == "clear"):
                self.clear()
            elif (res == "allClear"):
                self.allClear()
            elif (res == "equals"):
                self.evaluate()
            elif (res == "switch"):
                print "switching..."
                self.switch()
            else:
                self.input.addInput(res)
            src.result = None

    def clear(self):
        if (self.clsf.trackpad.touchData != []):    # clear drawing
            self.clsf.trackpad.reset()
        else:                                       # del input
            self.input.delete()

    def allClear(self):
        self.clsf.trackpad.reset()
        self.input.reset()
        self.output.reset()

    def evaluate(self):
        print self.input.evalString
        result = evaluate.evaluate(self.input.evalString)
        self.output.displayText = [result]

    def switch(self):
        self.clsf.trackpad.reset()
        self.calc.trackpad.reset()
        """Switch input source states."""
        if (self.clsf.state == "active"):            
            self.clsf.state = "inactive"
            self.calc.state = "active"
        else:
            self.clsf.state = "active"
            self.calc.state = "inactive"

    def onDraw(self, canvas):
        self.input.draw(canvas)
        self.output.draw(canvas)
        if (self.clsf.state == "active"):
            self.clsf.draw(canvas)
        else:
            self.calc.draw(canvas)

    def onKey(self, event):
        if (event.keysym == "space"):
            if (self.isPaused == True):
                self.unpause()
            else:
                self.pause()

    def pause(self):
        self.isPaused = True
        self.clsf.trackpad.stop()
        self.calc.trackpad.stop()
        mouse.showCursor()

    def unpause(self):
        self.isPaused = False
        self.clsf.trackpad.start()
        self.calc.trackpad.start()


    def onMouse(self, event): pass
    def onMouseMove(self, event): pass
    def onMouseDrag(self, event): pass
    def onMouseRelease(self, event): pass
    def onKeyRelease(self, event): pass
    def onQuit(self): pass




class TextDisplay(object):

    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y, self.width, self.height = x, y , width, height
        self.margin = self.width / 10
        self.displayText = []
        self.evalString = []
        self.font = ("Helvetica Neue UltraLight", str(self.height / 3))
        self.bg = "#212834"
        self.fg = "#ffffff"
        self.bgImage = None
        self.__dict__.update(kwargs)

    def addInput(self, char):
        if (type(char) != str and type(char) != unicode):
            return -1
        self.displayText.append(evaluate.displayChar(char))
        self.evalString.append(evaluate.evalChar(char))
        print "display:", repr("".join(self.displayText))
        print "eval:", repr("".join(self.evalString))


    def delete(self):
        if (self.displayText != []):
            self.displayText.pop()
        if (self.evalString != []):
            self.evalString.pop()

    def reset(self):
        del self.displayText[:]
        del self.evalString[:]

    def draw(self, canvas):
        if (self.bgImage != None):
            canvas.create_image(self.x, self.y, image=self.bgImage,
                                anchor="nw")
        else:
            x0 = self.x
            x1 = self.x + self.width
            y0 = self.y
            y1 = self.y + self.height
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.bg, width=0)
        cx = self.x + self.width - self.margin
        cy = self.y + self.height - self.margin
        msg = "".join(self.displayText)
        canvas.create_text(cx, cy, anchor="se", text=msg,
                           fill=self.fg, font=self.font)



width = 690
height = 550
timerDelay = 64
MainWindow(width=width, height=height, timerDelay=timerDelay).run()
