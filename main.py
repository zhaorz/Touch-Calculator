"""
main.py
~~~~~~~~~~~~~~~


WolframAlpha AppID: RAJVVX-8GEGHXV5LU

"""



import eventBasedAnimation

import classifier





class MainWindow(eventBasedAnimation.Animation):

    def onInit(self):
        self.trackpad = classifier.Classifier(0, 400, self.width, 300)
        self.input = InputDisplay(0, 0, self.width, 200)

    def onStep(self):
        self.trackpad.step()
        self.getInput()

    def getInput(self):
        if (self.trackpad.result != None):
            self.input.addInput(self.trackpad.result)
            self.trackpad.result = None




    def onDraw(self, canvas):
        self.trackpad.draw(canvas)
        self.input.draw(canvas)




    def onMouse(self, event): pass
    def onKey(self, event): pass 
    def onMouseMove(self, event): pass
    def onMouseDrag(self, event): pass
    def onMouseRelease(self, event): pass
    def onKeyRelease(self, event): pass
    def onQuit(self): pass




class InputDisplay(object):

    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y , width, height
        self.margin = self.width / 10
        self.displayText = ""
        self.bg = "#212834"
        self.fg = "#ffffff"

    def addInput(self, char):
        if (type(char) != str):
            return -1
        self.displayText += char

    def delete(self):
        self.displayText = self.displayText[:-1]

    def draw(self, canvas):
        x0 = self.x
        x1 = self.x + self.width
        y0 = self.y
        y1 = self.y + self.height
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.bg, width=0)
        cx = self.width - self.margin
        cy = self.y + self.height / 2
        font = ("Helvetica Neue UltraLight", str(self.height / 5))
        canvas.create_text(cx, cy, anchor="e", text=self.displayText,
                           fill=self.fg, font=font)




































width = 700
height = 700
timerDelay = 64
MainWindow(width=width, height=height, timerDelay=timerDelay).run()








