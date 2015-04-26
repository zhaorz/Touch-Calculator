"""
main.py
~~~~~~~~~~~~~~~


WolframAlpha AppID: RAJVVX-8GEGHXV5LU

"""



import eventBasedAnimation

import classifier





class MainWindow(eventBasedAnimation.Animation):

    def onInit(self):
        self.input = classifier.Classifier(0, 400, self.width, 300)

    def onStep(self):
        self.input.step()

    def onDraw(self, canvas):
        self.input.draw(canvas)




    def onMouse(self, event): pass
    def onKey(self, event): pass 
    def onMouseMove(self, event): pass
    def onMouseDrag(self, event): pass
    def onMouseRelease(self, event): pass
    def onKeyRelease(self, event): pass
    def onQuit(self): pass







































width = 700
height = 700
timerDelay = 64
MainWindow(width=width, height=height, timerDelay=timerDelay).run()








