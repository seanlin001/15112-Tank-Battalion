from cmu_112_graphics import *
from wallGeneration import *
import math

def appStarted(app):
    app.rows = 26
    app.cols = 26
    app.margin = 18
    app.menu = True
    app.menuInstructions = False

def drawMenuScreen(app, canvas):
    canvas.create_text
    if app.menuInstructions == True:
        canvas.create_text

def keyPressed(app, event):
    if app.menu == True:
        if app.menuInstructions == True:
            if event.key.lower() == "q":
                resetApp(app)
        else: 
            if event.key.lower() == "h":
                app.menuInstructions = True
            if event.key.lower() == "p":
                app.menu = False
        
def resetApp(app):
    app.menu = True
    app.menuInstructions = False
    

def drawInstructions(app, canvas):
    canvas.create_rectangle(50, 50, app.width-50, app.height-50, fill='black')
    canvas.create_text(app.width/2, 80, text='INSTRUCTIONS', fill='white', font='Arial 20 bold')

def getCellBounds(app, row, col):
    gridWidth  = app.width - 6*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin*2 + col * cellWidth
    x1 = app.margin*2 + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return(x0, y0, x1, y1)

# Grid will be invisible once wall generation is developed
def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1)

def drawGame(app, canvas):
    drawGrid(app, canvas)
    # Wall generation
    # Tank
    # Enemy sequence


def redrawAll(app, canvas):
    if app.menu == True:
        drawMenuScreen(app, canvas)
        if app.menuInstructions == True:
            drawInstructions(app, canvas)
    if app.menu == False:
        drawGame(app, canvas)

runApp(width=576, height=504)