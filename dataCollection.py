"""
dataCollection.py
~~~~~~~~~~~~~~~


"""

import multitouch
import string
import copy
from eventBasedAnimation import Animation



class MainWindow(Animation):

    def onInit(self):
        self.initTrackpad()
        self.initCharactersDisplay()
        self.initDataDisplay()
        self.initInstructionsDisplay()

    def initTrackpad(self):
        self.trackpad = DataCollectionTrackpad()
        self.trackpad.x, self.trackpad.y = 25, 375
        self.trackpad.width, self.trackpad.height = 415, 300
        self.trackpad.isDrawing = False
    
    def initCharactersDisplay(self):
        self.display = CharactersDisplay(
            x=25, y=50, width=self.width, height=125, margin=self.margin)

    def initDataDisplay(self):
        self.chars = DataDisplay(
            x=25, y=225, width=self.width, height=125, margin=self.margin)
        self.chars.touchData = self.trackpad.touchData   # alias for raw data
        self.chars.charData = dict()    # dict for char:touchData values

    def initInstructionsDisplay(self):
        self.instructions = InstructionsDisplay(
            x=490, y=375, width=485, height=300, margin=self.margin)
        self.instructions.numCells = self.display.numCells
        self.instructions.activeCell = self.display.activeCell
        self.instructions.completedCells = self.display.completedCells
        self.instructions.isDrawing = self.trackpad.isDrawing


    def onMouse(self, event): pass
    
    def onKey(self, event): 
        if (event.keysym == "space"):
            if (self.trackpad.isDrawing == False):
                self.trackpad.isDrawing = True
                self.trackpad.start()
            else:
                self.trackpad.isDrawing = False
                self.trackpad.stop()
                #print self.trackpad.touchData
                #print featureDetection.process(data.Trackpad.touchData)
        elif (event.keysym == "Left" or event.keysym == "Right"):
            self.display.shift(event.keysym)
            self.chars.shift(event.keysym)
        elif (event.keysym == "Return"):
            self.save(self.chars.charData)

    # writes a file in current directory
    def save(self, d):
        f = open("charData.txt", "w")
        f.write(str(d))
        f.close

    def onStep(self):
        # Make aliases
        self.instructions.numCells = self.display.numCells
        self.instructions.activeCell = self.display.activeCell
        self.instructions.completedCells = self.display.completedCells
        self.instructions.isDrawing = self.trackpad.isDrawing

    
    def onDraw(self, canvas):
        self.drawHeader(canvas)
        self.trackpad.draw(canvas)
        self.display.draw(canvas)
        self.chars.draw(canvas)
        self.instructions.draw(canvas)

    def drawHeader(self, canvas):
        cx = self.width / 2
        cy = self.margin
        title = "Data Collection"
        canvas.create_text(cx, cy, anchor="center", text=title,
                           font="Arial 26 bold", fill="black")


    def onMouseMove(self, event): pass
    
    def onMouseDrag(self, event): pass
    
    def onMouseRelease(self, event): pass
    
    def onKeyRelease(self, event): pass
    
    def onQuit(self): pass


class CharactersDisplay(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.width = self.width - self.margin * 2
        self.activeColor = "orange"
        self.completedColor = "green"
        self.darkGrey = "#4A4A4A"
        self.initCells()

    def initCells(self):
        self.numCells = 7
        self.activeCell = 0         # currently drawing (highlight orange)
        self.completedCells = []    # done drawing (highlight green)
        self.targets = string.ascii_uppercase[0:self.numCells] # filler
        self.cellWidth = self.cellHeight = self.height
        self.cellMargin = (self.width + self.margin - 
                            self.numCells * self.cellWidth) / self.numCells

    # keysym is either left or right, move active/complete accordingly
    def shift(self, keysym):
        if (keysym == "Left"):
            if (self.activeCell == None):   # reached end, need to go backwards
                self.activeCell = self.numCells - 1
                self.completedCells.pop()
            elif (self.activeCell == 0):  # leftmost
                return
            else:
                self.activeCell -= 1
                self.completedCells.pop()   # remove rightmost from completed
        else:   # shift right
            if (self.activeCell == None):   # completed set
                return True
            elif (self.activeCell == self.numCells - 1):  # rightmost active
                self.completedCells.append(self.activeCell)
                self.activeCell = None
            else:
                self.completedCells.append(self.activeCell)
                self.activeCell += 1

    def draw(self, canvas):
        x0 = self.x
        y0 = self.y
        x1 = self.x + self.width
        y1 = self.y + self.height
        #canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)
        self.drawCells(canvas)

    def drawCells(self, canvas):
        top, left = self.x, self.y
        for i in xrange(self.numCells):
            x0 = top + i * (self.cellWidth + self.cellMargin)
            x1 = x0 + self.cellWidth
            y0 = left
            y1 = y0 + self.height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)
            canvas.create_text(x0 + self.cellWidth / 2,y0 + self.cellWidth / 2,
                               text=self.targets[i], font="Arial 48 bold")
            if (i == self.activeCell):
                self.drawHighlightBox(canvas, x0, y0, x1, y1, self.activeColor)
            elif (i in self.completedCells):
                self.drawHighlightBox(canvas, x0, y0, x1, y1, 
                                      self.completedColor)

    def drawHighlightBox(self, canvas, x0, y0, x1, y1, color, width=3):
        # Draw 4 outline around box
        canvas.create_line((x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0),
                            fill=color, width=width, capstyle="projecting")


class DataDisplay(CharactersDisplay):

    # override
    def shift(self, keysym):
        if (keysym == "Left"):
            self.shiftLeft()
        else:
            self.shiftRight()

    def shiftLeft(self):
        if (self.activeCell == None):   # reached end, need to go backwards
            self.activeCell = self.numCells - 1
            self.completedCells.pop()
        elif (self.activeCell == 0):  # leftmost
            return
        else:
            self.activeCell -= 1
            self.completedCells.pop()   # remove rightmost from completed

    def shiftRight(self):
        if (self.activeCell == None):   # completed set
            return True
        elif (self.activeCell == self.numCells - 1):  # rightmost active
            self.completedCells.append(self.activeCell)
            self.addData(self.activeCell)
            self.activeCell = None
        else:
            self.completedCells.append(self.activeCell)
            self.addData(self.activeCell)
            self.activeCell += 1

    # Writes current touchData to charData
    def addData(self, activeCell):
        target = self.targets[activeCell]       # character string
        self.charData[target] = copy.deepcopy(self.touchData)   


    # override (draw data instead of target)
    def drawCells(self, canvas):
        top, left = self.x, self.y
        for i in xrange(self.numCells):
            x0 = top + i * (self.cellWidth + self.cellMargin)
            x1 = x0 + self.cellWidth
            y0 = left
            y1 = y0 + self.height
            canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)
            if (i == self.activeCell):
                self.drawHighlightBox(canvas, x0, y0, x1, y1, self.activeColor)
            elif (i in self.completedCells):
                self.drawHighlightBox(canvas, x0, y0, x1, y1, 
                                      self.completedColor)
                self.drawData(canvas, x0, y0, x1, y1, self.targets[i])

    def drawData(self, canvas, x0, y0, x1, y1, character):
        margin = (x1 - x0) / 8      # margin for data cells = 1/8 width
        width = height = (x1 - x0) - margin * 2
        for (x, y, time) in self.charData[character]:
            cx = x0 + margin + x * width
            cy = y0 + margin + height - y * height
            self.drawDot(canvas, cx, cy, 3, self.darkGrey)

    def drawDot(self, canvas, cx, cy, r, color='black'):
        x0 = cx - r
        x1 = cx + r
        y0 = cy - r
        y1 = cy + r
        canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)


# Keeps track of state and displays appropriate user instruction
class InstructionsDisplay(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def draw(self, canvas):
        self.drawTitle(canvas)
        self.drawInstructions(canvas)

    def default(self):
        msg = "Draw the orange-highlighted character"
        return msg

    def drawTitle(self, canvas):
        cx = self.x + self.width / 2
        cy = self.y + self.margin / 2
        msg = "Instructions"
        canvas.create_text(cx, cy, anchor="center", text=msg,
                           font="Arial 22 bold")

    def drawInstructions(self, canvas):
        msg = []
        msg.append(self.default())
        msg.append(self.spacebar())
        msg.append(self.arrow())
        msg.append(self.save())
        msg = '\n'.join(msg)    # put each instruction on its own line
        y = self.y + self.margin * 2
        canvas.create_text(self.x, y, anchor="nw", text=msg, font="Arial 18")

    def spacebar(self):
        variable = "start" if self.isDrawing == False else "stop"
        msg = "Press space to " + variable + " drawing."
        return msg

    def arrow(self):
        msg = "Press right arrow to confirm this character.\n"
        msg += "Press left arrow to go to previous character."
        return msg

    def save(self):
        # final character is done
        if ((self.numCells - 1) in self.completedCells):
            return "Press return to save"
        else:
            return ""



# Input trackpad data and draws it
class DataCollectionTrackpad(multitouch.Trackpad):

    def draw(self, canvas):
        x0 = self.x
        y0 = self.y
        x1 = self.x + self.width
        y1 = self.y + self.height
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightgrey", width=0)
        self.drawToggle(canvas)
        self.drawData(canvas)

    # draws points in self.touchData in real time
    def drawData(self, canvas):
        left = self.x
        top = self.y
        r = 6
        for (normx, normy, timestamp) in self.touchData:
            x = left + normx * self.width
            y = top + self. height - normy * self.height
            self.drawDot(canvas, x, y, r)

    # Green/Red dot corresponding to self.isDrawing
    def drawToggle(self, canvas):
        color = 'green' if (self.isDrawing == True) else 'red'
        r = 10
        self.drawDot(canvas, self.x + 2 * r, self.y + 2 * r, r, color)

    def drawDot(self, canvas, cx, cy, r, color="#4A4A4A"):
        x0 = cx - r
        x1 = cx + r
        y0 = cy - r
        y1 = cy + r
        canvas.create_oval(x0, y0, x1, y1, fill=color, width=0)






width = 1000
height = 700
margin = 25
dataCollectionWindow = MainWindow(width=width, height=height, margin=margin)
dataCollectionWindow.run()
