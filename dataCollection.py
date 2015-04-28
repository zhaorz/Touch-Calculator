"""
dataCollection.py
~~~~~~~~~~~~~~~

Program that collects trackpad character data. 

Enter the desired characters to be collected in MainWindow.initCharacterSets(). 
Note that the program is only designed to collect 7 characters per set
(for sake of Tkinter latency). There can be unlimited number of sets.

When all sets have data entered, the user is prompted to press s to save.
The data is saved in the /data directory and is given a name based on the
time saved.

The final output data consists of a list of dictionaries--each dictionary
corresponding with the character set number. Each dictionary has 7 keys,
corresponding to the characters in that particular set.
"""


# Default libraries
import string
import copy
import os

# 15-112 libraries
from eventBasedAnimation import Animation

# Custom libraries
import multitouch
import fileIO
import mouse



class MainWindow(Animation):

    def onInit(self):
        self.windowTitle = "Data Collection"
        self.initCharacterSets()
        self.initTrackpad()
        self.initCharactersDisplay()
        self.initDataDisplay()
        self.initInstructionsDisplay()
        self.saveDialogueTimer = 0
        self.data = list()      # empty container for user data

    # Character sets must have length 7
    def initCharacterSets(self):
        self.characterSets = [
            # ["0", "U", "3", "2", "8", "9", "6"]
            # ["A", "B", "C", "D", "E", "F", "7"]
            # ["0", "1", "2", "3", "4", "5", "6"],
            # ["8", "9", "A", "B", "C", "D", "E"],
            # ["F", "0", "1", "2", "3", "4", "5"],
            # ["6", "7", "8", "9", " ", ",", "."]
            # ['*', '/', '+', '-', '^', '(', ')'],
            # ['*', '/', '+', '-', '^', '(', ')'],
            # ['*', '/', '+', '-', '^', '(', ')'],
            # ['*', '/', '+', '-', '^', '(', ')'],
            # ['*', '/', '+', '-', '^', '(', ')']
            # div       # mult      # pi            # sqrt
            # [u'\u00f7', u'\u00d7', u'\u03c0', 'e', u'\u221a', '%', '.'],
            # [u'\u00f7', u'\u00d7', u'\u03c0', 'e', u'\u221a', '%', '.'],
            # [u'\u00f7', u'\u00d7', u'\u03c0', 'e', u'\u221a', '%', '.'],
            # [u'\u00f7', u'\u00d7', u'\u03c0', 'e', u'\u221a', '%', '.'],
            # [u'\u00f7', u'\u00d7', u'\u03c0', 'e', u'\u221a', '%', '.']
            # ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', '!'],
            # ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', '!'],
            # ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', '!'],
            # ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', '!'],
            # ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', '!']
            ['ln', 'log', '', '', '', '', ''],
            ['ln', 'log', '', '', '', '', ''],
            ['ln', 'log', '', '', '', '', ''],
            ['ln', 'log', '', '', '', '', ''],
            ['ln', 'log', '', '', '', '', ''],
            ]
        for charSet in self.characterSets:
            assert(len(charSet) == 7)
        self.currentCharacterSet = 0


    def initTrackpad(self):
        self.trackpad = multitouch.VisualTrackpad(25, 375, 415, 300)
        self.trackpad.active = "#cae2ed"

    
    def initCharactersDisplay(self):
        # First target set is first set in characterSets
        self.display = CharactersDisplay(
            x=25, y=50, width=self.width, height=125, margin=self.margin,
            targets=self.characterSets[self.currentCharacterSet])

    def initDataDisplay(self):
        self.chars = DataDisplay(
            x=25, y=225, width=self.width, height=125, margin=self.margin,
            targets=self.characterSets[self.currentCharacterSet])
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
        elif (event.keysym == "Up"):
            if (self.trackpad.isDrawing == True):   # stop trackpad input
                self.trackpad.isDrawing = False
                self.trackpad.stop()
            self.chars.saveChar()
        elif (event.keysym == "Down"):
            self.chars.deleteChar()
        elif (event.keysym == "s"):
            # test if all cells completed
            if ((self.display.numCells - 1) in self.display.completedCells):
                self.save(self.data)
        elif (event.keysym == "Return"):    # next character set
            # test if all cells completed
            if ((self.display.numCells - 1) in self.display.completedCells):
                self.nextSet()

    # writes a file in current directory
    def save(self, d):
        self.data.append(self.chars.charData)   # add last data set to output
        filename = fileIO.timeStr() + ".txt"
        if (filename in os.listdir("data/")):
            print "Error, file already exists"
            return False
        path = "data/" + filename
        fileIO.writeTo(path, d)
        self.saveSuccess()

    # Stores current self.chars.charData in self.data and swaps in next charSet
    def nextSet(self):
        self.data.append(self.chars.charData) 
        if (self.currentCharacterSet == len(self.characterSets) - 1):
            # already on last set, ready to save
            pass
        else:   # reinitialize with next set
            self.currentCharacterSet += 1
            self.initCharactersDisplay()
            self.initDataDisplay()



    def onStep(self):
        # Send information so instructions can draw appropriately
        self.instructions.numCells = self.display.numCells
        self.instructions.activeCell = self.display.activeCell
        self.instructions.completedCells = self.display.completedCells
        self.instructions.isDrawing = self.trackpad.isDrawing
        self.instructions.currentCharacterSet = self.currentCharacterSet
        self.instructions.totalSets = len(self.characterSets)
        if (self.saveDialogueTimer > 0):
            self.saveDialogueTimer -= 1
        self.controlMouse()

    def controlMouse(self):
        """Anchors mouse to top left corner and hides the cursor."""
        mouse.mouseMove(10, 50)     # reset position
        mouse.hideCursor()

    # Display save success dialogue for some time
    def saveSuccess(self):
        self.saveDialogueTimer = 30

    def onDraw(self, canvas):
        self.drawHeader(canvas)
        self.trackpad.draw(canvas)
        self.display.draw(canvas)
        self.chars.draw(canvas)
        self.instructions.draw(canvas)
        self.drawSaveDialogue(canvas)

    def drawHeader(self, canvas):
        cx = self.width / 2
        cy = self.margin
        title = "Data Collection"
        canvas.create_text(cx, cy, anchor="center", text=title,
                           font="Arial 26 bold", fill="black")
        self.drawSetProgress(canvas)

    def drawSetProgress(self, canvas):
        x = y = self.margin
        msg = ("Set " + str(self.currentCharacterSet + 1) + " of " +
                str(len(self.characterSets)))
        canvas.create_text(x, y, anchor="w", text=msg, font="Arial 18")


    def drawSaveDialogue(self, canvas):
        if (self.saveDialogueTimer == 0):   # don't draw
            return
        x = self.width - self.margin * 2
        y = self.height - self.margin
        msg = "Save successful!\nPress ctrl+r to enter more data"
        canvas.create_text(x, y, text=msg, anchor="se", 
                           font="Arial 22 bold", fill="green")

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

    # Adds current touchData to activeCell dictionary value
    def saveChar(self):
        target = self.targets[self.activeCell]       # character string
        self.charData[target] = copy.deepcopy(self.touchData)  

    # Clears activeCell dictionary value
    def deleteChar(self):
        target = self.targets[self.activeCell]      # character string
        if (target not in self.charData.keys()):    # character doesn't exist
            return False
        del self.charData[target]

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
                self.drawData(canvas, x0, y0, x1, y1, self.targets[i])
            elif (i in self.completedCells):
                self.drawHighlightBox(canvas, x0, y0, x1, y1, 
                                      self.completedColor)
                self.drawData(canvas, x0, y0, x1, y1, self.targets[i])

    def drawData(self, canvas, x0, y0, x1, y1, character):
        if (character not in self.charData.keys()):
            return
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
        msg = '\n'.join(msg)    # put each instruction on its own line
        y = self.y + self.margin * 2
        canvas.create_text(self.x, y, anchor="nw", text=msg, font="Arial 18")
        self.drawSave(canvas)
        self.drawNextSet(canvas)

    def spacebar(self):
        variable = "start" if self.isDrawing == False else "stop"
        msg = "Press space to " + variable + " drawing."
        return msg

    def arrow(self):
        msg = "Press up arrow to confirm this character.\n"
        msg += "Press down arrow to delete this character.\n"
        msg += "Press left arrow to go to previous character.\n"
        msg += "Press right arrow to go to next character."
        return msg

    def drawNextSet(self, canvas):
        # This set done
        if ((self.numCells - 1) in self.completedCells and
            self.currentCharacterSet != self.totalSets - 1):
            msg = "Press return for next set"
        else:
            return
        y = self.y + self.height - 2 * self.margin
        canvas.create_text(self.x, y, anchor="w", text=msg,
                           fill="orange", font="Arial 18 bold")


    def drawSave(self, canvas):
        # final character in final set is done 
        if ((self.numCells - 1) in self.completedCells and
            self.currentCharacterSet == self.totalSets - 1):
            msg = "Press s to save"
        else:
            return
        y = self.y + self.height - 1 * self.margin
        canvas.create_text(self.x, y, anchor="w", text=msg,
                           fill="orange", font="Arial 18 bold")




width = 1000
height = 700
margin = 25
dataCollectionWindow = MainWindow(width=width, height=height, margin=margin)
dataCollectionWindow.run()
