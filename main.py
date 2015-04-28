"""
main.py
~~~~~~~~~~~~~~~


WolframAlpha AppID: RAJVVX-8GEGHXV5LU

"""



import eventBasedAnimation

import classifier
import touchCalculator
import mathParser





class MainWindow(eventBasedAnimation.Animation):

    def onInit(self):
        self.windowTitle = "main"
        self.input = TextDisplay(0, 0, self.width, 100,
            bgImage=eventBasedAnimation.PhotoImage(file="graphics/top_700.gif"))
        self.output = TextDisplay(
            0, 100, self.width, 150, fg="#ffffff", bg="#3a475c",
            font=("Helvetica Neue UltraLight", "72"),
            bgImage=eventBasedAnimation.PhotoImage(file="graphics/bottom_700.gif"))
        self.clsf = classifier.Classifier(0, 250, self.width, 300,
                                          state="inactive")
        self.calculator = touchCalculator.Calculator(0, 250, self.width, 300,
                                                     state="active")
        self.charset = ['A', 'B', 'C', 'D', 'E', 'F',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '*', '/', '+', '-', '^', '(', ')', '.']

    def onStep(self):
        if (self.clsf.state == "active"):
            self.clsf.step()
        else:
            self.calculator.step()
        self.getInput()

    def getInput(self):
        src = self.clsf if self.clsf.state == "active" else self.calculator
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
        try:
            result = str(eval("".join(self.input.evalString)))
        except:
            result = "Error"
        self.output.displayText = [result]

    def switch(self):
        self.clsf.trackpad.reset()
        self.calculator.trackpad.reset()
        """Switch input source states."""
        if (self.clsf.state == "active"):            
            self.clsf.state = "inactive"
            self.calculator.state = "active"
        else:
            self.clsf.state = "active"
            self.calculator.state = "inactive"

    def onDraw(self, canvas):
        self.input.draw(canvas)
        self.output.draw(canvas)
        if (self.clsf.state == "active"):
            self.clsf.draw(canvas)
        else:
            self.calculator.draw(canvas)




    def onMouse(self, event): pass
    def onKey(self, event): pass 
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
        self.fg = "#efefef"
        self.bgImage = None
        self.__dict__.update(kwargs)

    def addInput(self, char):
        if (type(char) != str and type(char) != unicode):
            return -1
        self.displayText.append(mathParser.displayChar(char))
        self.evalString.append(mathParser.evalChar(char))


    def delete(self):
        self.displayText.pop()

    def reset(self):
        self.displayText = []
        self.evalString = []

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
        cx = self.width - self.margin
        cy = self.y + self.height / 2
        msg = "".join(self.displayText)
        canvas.create_text(cx, cy, anchor="e", text=msg,
                           fill=self.fg, font=self.font)




































width = 690
height = 550
timerDelay = 64
MainWindow(width=width, height=height, timerDelay=timerDelay).run()








