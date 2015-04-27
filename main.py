"""
main.py
~~~~~~~~~~~~~~~


WolframAlpha AppID: RAJVVX-8GEGHXV5LU

"""



import eventBasedAnimation

import classifier





class MainWindow(eventBasedAnimation.Animation):

    def onInit(self):
        self.clsf = classifier.Classifier(0, 400, self.width, 300)
        self.input = TextDisplay(0, 0, self.width, 200)
        self.output = TextDisplay(
            0, 200, self.width, 200, fg="#ffffff", bg="#3a475c",
            font=("Helvetica Neue UltraLight", "72"))
        self.charset = ['A', 'B', 'C', 'D', 'E', 'F',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                        '*', '/', '+', '-', '^']

    def onStep(self):
        self.clsf.step()
        self.getInput()

    def getInput(self):
        if (self.clsf.result != None):
            res = self.clsf.result
            if (res == "clear"):
                self.clear()
            elif (res == "AC"):
                self.allClear()
            elif (res == "="):
                print "equals pressed"
                self.evaluate()
            else:
                self.input.addInput(self.clsf.result)
            self.clsf.result = None

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
        if (self.isLegal(self.input.displayText) == False):
            return -1
        print "input display:", self.input.displayText
        try:
            result = str(eval(self.input.displayText))
        except:
            result = "Error"
        print "result:", result
        self.output.displayText = result

    def isLegal(self, s):
        for c in s:
            print c
            if c not in self.charset:
                return False
        return True

    def onDraw(self, canvas):
        self.clsf.draw(canvas)
        self.input.draw(canvas)
        self.output.draw(canvas)




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
        self.displayText = ""
        self.font = ("Helvetica Neue UltraLight", str(self.height / 5))
        self.bg = "#212834"
        self.fg = "#efefef"
        self.__dict__.update(kwargs)

    def addInput(self, char):
        if (type(char) != str):
            return -1
        self.displayText += char

    def delete(self):
        self.displayText = self.displayText[:-1]

    def reset(self):
        self.displayText = ""

    def draw(self, canvas):
        x0 = self.x
        x1 = self.x + self.width
        y0 = self.y
        y1 = self.y + self.height
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.bg, width=0)
        cx = self.width - self.margin
        cy = self.y + self.height / 2
        canvas.create_text(cx, cy, anchor="e", text=self.displayText,
                           fill=self.fg, font=self.font)




































width = 700
height = 700
timerDelay = 64
MainWindow(width=width, height=height, timerDelay=timerDelay).run()








