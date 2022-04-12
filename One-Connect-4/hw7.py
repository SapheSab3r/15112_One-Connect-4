#################################################
# hw7: One-Dimensional Connect Four
# name: Anqi Chen
# andrew id: aac2 
#
# collaborator(s) names and andrew ids: Ines (inesr) & James (jamesch2)
# 
#################################################

import cs112_n21_week3_linter
from cmu_112_graphics import *
import random, string, math, time

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# main app
#################################################

def appRestart(app):
    app.colorList = ['green', 'blue']
    app.outline = ''
    app.player = random.choice(app.colorList)
    boardAndCircles(app)
    
    app.board = app.cols // 2 * app.dotIndex
    app.gameOver = False
    app.placed = False 
    app.dotIndex = [1, 0]
    app.text = 'Select your 3-piece block'
    app.lineIndex = -1

    reSet(app)
    selectPlayer(app)

def reSet(app):
    app.selected = False 
    app.selectedLegal = False
    app.selectionIndex = -1

def appStarted(app):
    app.margin = 10
    app.cols = 10
    app.verticalLength = app.height / 3
    app.gap = 20
    app.click = 0 
    app.radius = 15
    
    app.color = ''
    app.selectionCenterIndex = -1
    appRestart(app)

#determine the first player based on the board order 
def boardAndCircles(app):
    if app.player == 'blue':
        app.dotIndex = [1,0]
        app.outline = 'lightBlue'
    else:
        app.dotIndex = [0,1]
        app.outline = 'lightGreen'

def keyPressed(app, event):
    if event.key == 'r':
        appRestart(app)

    elif app.gameOver == True:
        return 

    #increasing number of circles 
    elif (event.key == 'Right' or event.key == 'Up') and app.cols < 20:
        app.cols += 2
        reSet(app)
        app.board = app.cols // 2 * app.dotIndex
        
    #decreasing number of circles
    elif (event.key == 'Left' or event.key == 'Down') and app.cols > 6:
        app.cols -= 2
        reSet(app)
        app.board = app.cols // 2 * app.dotIndex

    #changing the current player when press 'p'
    elif event.key == 'p':
        if app.player == 'green':
            app.player = 'blue'
            app.outline = 'lightBlue'
        else:
            app.player = 'green'
            app.outline = 'lightGreen'

    elif event.key == 'c' and app.selectionIndex != -1:
        if app.board[app.selectionIndex] == 0:                
            app.board[app.selectionIndex - 1] = 0 
            app.board[app.selectionIndex + 1] = 0

        elif app.board[app.selectionIndex] == 1:  
            app.board[app.selectionIndex - 1] = 1
            app.board[app.selectionIndex + 1] = 1 

#get the index of the selected circle 
def getPieceIndex(app, x, y):
    cellWidth = app.width / app.cols
    r = (cellWidth / 2) * 0.85

    if app.height / 2 - r < y < app.height / 2 + r: 
        index = int(x / cellWidth)
        
    else:
        index = -1
        app.selectedLegal = False

    return index

#get the center cx, cy and the radius of the circle 
def getPieceCenterAndRadius(app, pieceIndex):
    cellWidth = app.width / app.cols
    r = (cellWidth / 2) * 0.85

    cx = cellWidth / 2 + cellWidth * pieceIndex
    cy = app.height / 2  
    return cx, cy, r

def mousePressed(app, event):
    if app.gameOver == True:
        return 

    app.selectionIndex = getPieceIndex(app, event.x, event.y)#the mouse index
    selectDots(app)
    checkSameColorSelection(app)

    #if the selected circles being stored and the second click is head 
    if app.click == 1 and app.selectionIndex == 0: 
        app.board = (app.board[app.selectionCenterIndex - 1 : 
                        app.selectionCenterIndex + 2] + 
                            app.board[0 : app.selectionCenterIndex - 1] +
                            app.board[app.selectionCenterIndex + 2: ])

        app.click = 0
        app.placed = True  

    #if the selected circles being stored and the second click is tail
    elif app.click == 1 and app.selectionIndex == len(app.board) - 1:
        app.board = (app.board[0 : app.selectionCenterIndex - 1] + 
                            app.board[app.selectionCenterIndex + 2 : ] +
                            app.board[app.selectionCenterIndex - 1 : 
                            app.selectionCenterIndex + 2])

        app.click = 0
        app.placed = True 

    checkWinning(app)
    selectPlayer(app)
    
#check if the selected three circles are the same color 
def checkSameColorSelection(app):
    if 1 < app.selectionIndex < len(app.board) - 2: 
        if (app.board[app.selectionIndex] == app.board[app.selectionIndex - 1] 
            and app.board[app.selectionIndex] == 
                app.board[app.selectionIndex + 1]):
                    app.selected = False 
                    app.click = 0
                    app.color = 'pink'
                    app.text = 'Block must contain current player'

#changing the color of the box based on the position of circle being selected
def selectDots(app):
    if 0 < app.selectionIndex < len(app.board) - 1: #if not head or tail 
        app.selectedLegal = True

        #if the selected range is illegal to move 
        if app.selectionIndex == 1 or app.selectionIndex == len(app.board) - 2:
            app.selected = False
            app.click = 0
            app.color = 'pink'
            app.text = 'End cannot be in block'

        #if the selected range is legal to move 
        elif (1 < app.selectionIndex < len(app.board) - 2 
                and app.placed == False):
            app.selected = True 
            app.selectionCenterIndex = app.selectionIndex
            app.click = 1
            app.color = 'orange'
            app.text = 'Select end to move block to'

    else:
        app.selectedLegal = False
            
#check if there are 4 same circles in a row 
def checkWinning(app):
    for i in range(len(app.board) - 3):
        if (app.board[i] == app.board[i + 1] and 
                app.board[i + 1] == app.board[i + 2] and
                    app.board[i + 2] == app.board[i + 3]):
                        app.lineIndex = i 
                        app.text = 'Game Over!!!!!'
                        app.gameOver = True
                        break
                        
def selectPlayer(app):
    if app.gameOver == True:
        return 

    #swtching the players' colors
    elif app.player == 'green' and app.placed == True:
        app.placed = False
        app.player = 'blue'
        app.outline = 'lightBlue'
        app.text = 'Select your 3-piece block'
        
    elif app.player == 'blue' and app.placed == True:
        app.placed = False
        app.player = 'green'
        app.outline = 'lightGreen'
        app.text = 'Select your 3-piece block'
        
def redrawAll(app, canvas):
    drawTitle(app, canvas)
    drawInstructions(app, canvas)
    drawCurrentPlayerAndMessage(app, canvas)
    drawSelectionBox(app, canvas)
    drawBoard(app, canvas)
    drawLine(app, canvas)
    drawRules(app, canvas)
    
def drawTitle(app, canvas):
    canvas.create_text(app.width / 2, 0 + app.margin, 
                        text = 'One-Dimensional Connect Four!',
                        font = 'Arial 25 bold', anchor = 'n')

def drawInstructions(app, canvas):
    messages = ['See rules below.',
                'Click interior piece to select center of 3-piece block.',
                'Click end piece to move that block to that end.',
                'Change board size (and then restart) with arrow keys.',
                'For debugging, press c to set the color of selected block.',
                'For debugging, press p to change the current player.',
                'Press r to restart.',
               ]
    gap = app.gap * 2 + app.gap / 2
    for line in messages: 
        canvas.create_text(app.width / 2, 0 + gap, text = line,
                            font = 'Arial 18 bold')
        gap += 20
        

def drawRules(app, canvas):
    messages = [
  "The Rules of One-Dimensional Connect Four:",
  "Arrange N (10 by default) pieces in a row of alternating colors.",
  "Players take turns to move three pieces at a time, where:",
  "      The pieces must be in the interior (not on either end)",
  "      The pieces must be adjacent (next to each other).",
  "      At least one moved piece must be the player's color.",
  "The three pieces must be moved in the same order to either end of the row.",
  "The gap must be closed by sliding the remaining pieces together.",
  "The first player to get four (or more) adjacent pieces of their color wins!",
               ]

    gap = app.margin * 5
    for line in messages:
        canvas.create_text(app.margin, app.height / 2 + gap + app.margin * 2, 
                            text = line,
                            font = 'Arial 18 bold', anchor = 'w')
        gap += 20

def drawCurrentPlayerAndMessage(app, canvas):
    canvas.create_text(app.width / 2, app.verticalLength + app.gap, 
                        text = 'Current Player:', font = 'Arial 18 bold',
                        fill = app.player, anchor = 'e')
 
    canvas.create_text(app.width / 2 + app.gap * 2, 
                            app.verticalLength + app.gap, 
                            text = app.text, 
                            font = 'Arial 18 bold',
                            fill = app.player, anchor = 'w')
    
    canvas.create_oval(app.width / 2 + app.gap - app.radius, 
                        app.verticalLength + app.gap - app.radius, 
                        app.width / 2 + app.gap + app.radius, 
                        app.verticalLength + app.gap + app.radius,
                        width = 4,
                        outline = app.player,
                        fill = app.outline)
    
def drawSelectionBox(app, canvas):
    if app.selectedLegal == True:
        cellWidth = app.width / app.cols
        length = cellWidth / 2
        cx, cy, r = getPieceCenterAndRadius(app, app.selectionIndex)
        canvas.create_rectangle(cx - cellWidth - length, 
                                cy - cellWidth / 2, 
                                cx + cellWidth + length, cy + cellWidth / 2,
                                outline = app.color, fill = app.color)

def drawBoard(app, canvas):
    for col in range(len(app.board)):
        cx, cy, r = getPieceCenterAndRadius(app, col)
        
        if app.board[col] == 0:
            color = 'lightGreen'
            outline = 'green'
        else:
            color = 'lightBlue'
            outline = 'blue'

        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
                            outline = outline, width = 4, fill = color)

def drawLine(app, canvas):
    if app.gameOver == True:
        cx, cy, r = getPieceCenterAndRadius(app, app.lineIndex)
        cellWidth = app.width / app.cols
        length = 3 * cellWidth

        canvas.create_line(cx, cy, cx + length, cy, width = 3, 
                            fill = 'black')

def main():
    cs112_n21_week3_linter.lint()
    runApp(width=650, height=550)

if __name__ == '__main__':
    main()