"""
main.py
~~~~~~~~~~~~~~~


WolframAlpha AppID: RAJVVX-8GEGHXV5LU

"""

import eventBasedAnimation

class Display(object):

    def __init__(self, x, y, width, height, **kwargs):
        self.x, self.y, self.width, self.height = x, y , width, height
        self.margin = self.width / 10
        self.displayText = ""
        self.font = ("Helvetica Neue UltraLight", str(self.height / 2))
        self.bg = "#212834"
        self.fg = "#efefef"
        self.bgImage = None
        # self.bgImage = eventBasedAnimation.PhotoImage(file="graphics/top_700.gif")
        self.__dict__.update(kwargs)

    def addInput(self, char):
        if (type(char) != str):
            return -1
        self.displayText += char

    def delete(self):
        self.displayText = self.displayText[:-1]

    def draw(self, canvas):
        if (self.bgImage != None):
            canvas.create_image(0, 0, image=self.bgImage)
        else:    
            x0 = self.x
            x1 = self.x + self.width
            y0 = self.y
            y1 = self.y + self.height
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.bg, width=0)
        cx = self.width - self.margin
        cy = self.y + self.height / 2
        canvas.create_text(cx, cy, anchor="e", text=self.displayText,
                           fill=self.fg, font=self.font)





if __name__ == "__main__":
    width = 700
    height = 100
    class DisplayWindow(eventBasedAnimation.Animation):
        def onInit(self):
            self.display = Display(0, 0, width, height)
            self.display.displayText = u"\u222b " + "sin(x) dx"
        def onDraw(self, canvas):
            self.display.draw(canvas)
    timerDelay = 64
    mainWindow = DisplayWindow(
        width=width, height=height, timerDelay=timerDelay)
    mainWindow.run()
