#################################################
# Tank Battalion
#
# name: Sean Lin
# andrew id: seanlin
#################################################
# Main game mechanics 

from cmu_112_graphics import *
from wallGeneration import *
from gameData import *
import math, random, time
def appStarted(app):
    app._root.resizable(False, False)
    # Sprites from https://www.spriters-resource.com/fullview/60016/
    app.instructionsImg = app.loadImage('instructions.png')
    app.playerTankImg = app.loadImage('playerTank.png')
    app.upPlayerTankImg = app.scaleImage(app.playerTankImg, 0.05)
    app.downPlayerTankImg = app.upPlayerTankImg.rotate(180)
    app.leftPlayerTankImg = app.upPlayerTankImg.rotate(90)
    app.rightPlayerTankImg = app.upPlayerTankImg.rotate(270)
    app.pTankImg = app.upPlayerTankImg
    app.enemyTank1Img = app.loadImage('enemyTank1.png')
    app.enemyTank1Img = app.scaleImage(app.enemyTank1Img, 1.6)
    app.upEnemyTank1Img = app.enemyTank1Img
    app.downEnemyTank1Img = app.upEnemyTank1Img.rotate(180)
    app.leftEnemyTank1Img = app.upEnemyTank1Img.rotate(90)
    app.rightEnemyTank1Img = app.upEnemyTank1Img.rotate(270)
    app.tankXBuffer, app.tankYBuffer = 9, 9
    #app.enemyTankXBuffer, app.enemyTankYBuffer = 12.8, 12.8
    app.rows = 26
    app.cols = 26
    app.score = 0
    app.leftMargin = 36
    app.rightMargin = 72
    app.topMargin = 18
    app.bottomMargin = 18
    app.rowHeight, app.colWidth = 18, 18
    app.menu = True
    app.menuInstructions = False
    app.tankOrientation = 0
    #app.playerTank = Tank(53, 237, 0, 3, False, 'u')
    #app.playerTank = Tank(app.width*0.3+app.leftMargin, app.height-app.bottomMargin*2, 0, 3, False, 'u')
    app.enemyTankList = []
    app.tankActivationTimeGap = 2
    app.timerDelay = 0
    app.stage = 1
    app.upBulletImg = app.loadImage('bullet.png')
    app.downBulletImg = app.upBulletImg.rotate(180)
    app.leftBulletImg = app.upBulletImg.rotate(90)
    app.rightBulletImg = app.upBulletImg.rotate(270)
    app.bullets = []
    app.bulletXBuffer = 4
    app.bulletYBuffer = 5.5
    # app.map = buildRandomMap(app.stage, 3, 15, 0, 26)#buildDefaultMap()
    #app.map = buildDefaultMap()
    app.map = buildRandomMap2(app.stage, 3, 15, 0, 26)#buildDefaultMap()
    app.maxEnemyTank = 20
    app.stageStartTime = time.time()
    app.lives = 3
    app.gameOver = False
    app.stagePassed = False
    createEnemies(app)
    setupPlayerTank(app)
    app.incomingEnemies = app.maxEnemyTank
    app.explosionList = []
    app.rewardPerTank = 100
    app.enemyShootFrequency = getEnemyShootFrequency(app)

def getEnemyShootFrequency(app):
    return min(.005 + .0005* app.stage, .02)

def newStage(app):
    app.incomingEnemies = app.maxEnemyTank
    app.stage +=1
    app.map = buildRandomMap2(app.stage, 3, 15, 0, 26)
    app.stagePassed = False
    app.stageStartTime = time.time()
    setupPlayerTank(app)
    app.explosionList = []
    app.enemyShootFrequency = getEnemyShootFrequency(app)
    app.enemyTankList = []
    createEnemies(app)

def buildMap(stage):
    if stage==1 or stage==2:
        map = buildDefaultMap()
    return map

def drawMenuScreen(app, canvas):
    canvas.create_text(app.width/2, 40, text='TANK', font='Arial 50 bold')
    canvas.create_text(app.width/2, 100, text='BATTALION', font='Arial 50 bold')
    canvas.create_text(app.width/2, app.height/2, text='P - PLAY', font='Arial 20')
    canvas.create_text(app.width/2, app.height/2+50, text='H - HELP', font='Arial 20')

def setupPlayerTank(app):
    app.playerTank = Tank(app.width*0.3+app.leftMargin, app.height-app.bottomMargin*2, 0, 3, False, 'u')

def keyPressed(app, event):
    if app.menu == True:
        if app.menuInstructions == True:
            if event.key.lower() == "q":
                closeInstructions(app)
        else: 
            if event.key.lower() == "h":
                app.menuInstructions = True
            if event.key.lower() == "p":
                app.menu = False
    elif app.menu == False:
        if event.key == 'Up':
            app.playerTank.orientation = 0
            app.pTankImg = app.upPlayerTankImg
            if app.playerTank.y-app.tankYBuffer < app.topMargin:
                app.playerTank.inMove = False
            else:
                app.playerTank.inMove = True
        elif event.key == 'Down':
            app.playerTank.orientation = 1
            app.pTankImg = app.downPlayerTankImg
            if app.playerTank.y+app.tankYBuffer > app.height-app.bottomMargin:
                app.playerTank.inMove = False
            else:
                app.playerTank.inMove = True
        elif event.key == 'Left':
            app.playerTank.orientation = 2
            app.pTankImg = app.leftPlayerTankImg
            if app.playerTank.x-app.tankXBuffer < app.leftMargin:
                app.playerTank.inMove = False
            else:
                app.playerTank.inMove = True
        elif event.key == 'Right':
            app.playerTank.orientation = 3
            app.pTankImg = app.rightPlayerTankImg
            if app.playerTank.x+app.tankXBuffer > app.width-app.rightMargin:
                app.playerTank.inMove = False
            else:
                app.playerTank.inMove = True
        elif event.key.lower() == 'x':
            b = app.playerTank.shootBullet()
            app.bullets.append(b)
        elif event.key.lower() == 'l':
            newStage(app)
        elif event.key == 'Enter' and app.stagePassed == True:
            newStage(app)
        elif event.key.lower() == 'q' and app.stagePassed == True:
            appStarted(app)
        elif event.key.lower() == 'q' and app.gameOver == True:
            appStarted(app)
            
        
def keyReleased(app, event):
    if event.key == 'Up' or event.key == 'Down' or event.key == 'Left' or event.key == 'Right':
        app.playerTank.inMove = False

def closeInstructions(app):
    app.menu = True
    app.menuInstructions = False
    
def timerFired(app):
    if app.gameOver == False and app.menu==False:
        if app.stagePassed==False:
            movePlayerTank(app)
            updateBullet(app)
            updateEnemyTank(app)
            updateExplosion(app)
            #printDebug(app)
        #else:
        #    newStage(app)
    

def updateExplosion(app):
    for i in reversed(range(len(app.explosionList))):
        e = app.explosionList[i]
        e.life -= 1
        if e.life < 0:
            app.explosionList.pop(i)

def drawInstructions(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    canvas.create_text(app.width/2, 40, text='INSTRUCTIONS', fill='white', font='Arial 20 bold')
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.instructionsImg))
    canvas.create_text(40, app.height-20, text='Q - QUIT', fill='white', font='Arial 10 bold')

def getCellBounds(app, row, col):
    x1, y1 = rowColToCoordinate(row, col, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth, 1)
    x2, y2 = rowColToCoordinate(row, col, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth, 4)
    return(x1, y1, x2, y2)

# # Grid will be invisible once wall generation is developed
# def drawGrid(app, canvas):
#     for row in range(app.rows):
#         for col in range(app.cols):
#             (x0, y0, x1, y1) = getCellBounds(app, row, col)
#             canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='')

def drawGame(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='gray')
    canvas.create_rectangle(app.leftMargin, app.topMargin, app.width-app.rightMargin, app.height-app.bottomMargin, fill='black')
    # drawGrid(app, canvas)
    drawPlayerTank(app, canvas)
    drawBullets(app, canvas)
    if(len(app.map.items())>0):
       drawMap(app, canvas)
    drawEnemyTank(app, canvas)

def createEnemies(app):
    for col in range(app.maxEnemyTank):
        x, y = rowColToCoordinate(0, col, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth, 0)
        tank = EnemyTank(x, y, 1, 2, True, False, col*app.tankActivationTimeGap, 'e')
        app.enemyTankList.append(tank)

def drawExplosion(app, canvas):
    for i in reversed(range(len(app.explosionList))):
        e = app.explosionList[i]
        x,y = e.getShape()
        canvas.create_polygon(x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3], x[4], y[4], x[5], y[5], x[6], y[6], x[7], y[7], x[8], y[8], x[9], y[9], x[10], y[10], x[11], y[11], x[12], y[12], x[13], y[13], x[14], y[14], fill='red')

def updateEnemyTank(app):
    for tank in app.enemyTankList:
        t = time.time() - app.stageStartTime - tank.actTime
        if not tank.isActivated:
            if  t > 0:
                tank.isActivated = True
        elif tank.isActivated and not tank.isKilled:
            dx, dy = tank.getMoveUnit(t)
            newX, newY = tank.x+dx, tank.y+dy
            cells = getImpactedCell(app, newX, newY, app.tankXBuffer, app.tankYBuffer, tank.orientation)
            canMove = not cellsWillBlock(app, cells, newX, newY)
            withinBoundary = withinBounds(app, newX, newY, app.tankXBuffer, app.tankYBuffer)
            if canMove and withinBoundary:
                tank.moveTank(t)
            else:
                k = random.randint(0,4)
                tank.orientation = (tank.orientation+k)%4
            r = random.uniform(0, 1)
            #shooting frequency control
            if tank.isActivated and not tank.isKilled:
                if r > 1- app.enemyShootFrequency:
                    b = tank.shootBullet()
                    app.bullets.append(b)
    incCount = 0
    killCount =0
    for tank in app.enemyTankList:
        if not tank.isActivated:
            incCount += 1
        if tank.isKilled:
            killCount +=1
    app.incomingEnemies = incCount
    if killCount == app.maxEnemyTank:
        app.stagePassed = True
    # enemyDebug(app)
        

def drawEnemyTank(app, canvas):
    for tank in app.enemyTankList:
        if tank.isActivated and not tank.isKilled:
            hsize = 9
            canvas.create_rectangle(tank.x-hsize, tank.y-hsize, tank.x+hsize, tank.y+hsize, fill='gray', outline='red')
            #canvas.create_image(tank.x, tank.y, image=ImageTk.PhotoImage(app.enemyTank1Img))

# def enemyDebug(app):
#     for tank in app.enemyTankList:
#         print(tank.x, tank.y)


def drawMap(app, canvas):
    for i in app.map:
        for j in app.map[i]:
            cell = app.map[i][j]
            image = None
            if cell.cellType != '.':
                x1, y1 = rowColToCoordinate(i, j, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth, 1)
                x2, y2 = rowColToCoordinate(i, j, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth, 4)
                if cell.cellType == '#':
                    canvas.create_rectangle(x1, y1, x2, y2, fill='firebrick', outline='black')
                elif cell.cellType == '@':
                    canvas.create_rectangle(x1, y1, x2, y2, fill='gainsboro', outline='gray')
                elif cell.cellType =='b':
                    if app.gameOver == True:
                        canvas.create_rectangle(x1, y1, x2, y2, fill='crimson', outline='')
                    else:
                        canvas.create_rectangle(x1, y1, x2, y2, fill='gold', outline='')
                    #print(i,j)
                    #print(x1, y1, x2, y2)

def drawBullets(app, canvas):
    for b in app.bullets:
        if b.orientation == 0:
            bulletImage = app.upBulletImg
        if b.orientation == 1:
            bulletImage = app.downBulletImg
        if b.orientation == 2:
            bulletImage = app.leftBulletImg
        if b.orientation == 3:
            bulletImage = app.rightBulletImg
        # canvas.create_image(b.x, b.y, image=ImageTk.PhotoImage(bulletImage))
        canvas.create_rectangle(b.x-4, b.y-5.5, b.x+4, b.y+5.5, fill='gray')

def updateBullet(app):
    for i in reversed(range(len(app.bullets))): 
        b = app.bullets[i]
        b.moveBullet()
        # if cell is brick, change to empty
        # Remove bullet from list if it reaches beyond boundaries
        # bx = app
        c1 = withinBounds(app, b.x, b.y, app.bulletXBuffer, app.bulletYBuffer)
        #c2: whether bullet hit brick
        c2 = False
        if c1:
            cells = getImpactedCell(app, b.x, b.y, app.bulletXBuffer+2, app.bulletYBuffer+2, app.bullets[i].orientation)
            for cell in cells:
                if cell[0] >= 0 and cell[0] <= app.rows and cell[1] >= 0 and cell[1] <= app.cols:
                    ce = app.map[cell[0]][cell[1]]
                    if ce.cellType == '#':
                        app.map[cell[0]][cell[1]].cellType = '.'
                        c2 = True
                    if ce.cellType == '@':
                        c2 = True
                    if ce.cellType == 'b':
                        app.gameOver = True
        if b.side =='e':
            c3 = bulletHitPlayerTank(app, b)
            if c3:
                app.lives -=1
                if app.lives == 0:
                    app.gameOver = True
                e = Explosion(app.playerTank.x, app.playerTank.y)
                app.explosionList.append(e)
                setupPlayerTank(app)
        else:
            j, c3 = bulletHitEnemyTank(app, b)
            if (j>=0 and c3):
                if app.enemyTankList[j].isActivated==True and app.enemyTankList[j].isKilled==False:
                    e = Explosion(app.enemyTankList[j].x, app.enemyTankList[j].y)
                    app.explosionList.append(e)
                    app.score += app.rewardPerTank
                    app.enemyTankList[j].isKilled=True
        c3 =False
        for tank in app.enemyTankList:
            hit = isHit(tank, b)
            if hit:
                e = Explosion(b.x, b.y)
                app.explosionList.append(e)
                c3 = True
                tank.isKilled = True

        if (not c1) or c2 or c3:
            app.bullets.pop(i)

def bulletHitPlayerTank(app, b):
    bx, by = b.x, b.y
    tx, ty = app.playerTank.x, app.playerTank.y
    notNewTank = time.time() - app.playerTank.birth >=5
    if abs(bx-tx) < app.bulletXBuffer + app.tankXBuffer and abs(by-ty) < app.bulletYBuffer + app.tankYBuffer and b.side == 'e' and notNewTank:
        return True
    else:
        return False

def bulletHitEnemyTank(app, b):
    bx, by = b.x, b.y
    res = False
    for i in reversed(range(len(app.enemyTankList))):
        tank = app.enemyTankList[i]
        tx, ty = tank.x, tank.y
        if abs(bx-tx) < app.bulletXBuffer + app.tankXBuffer and abs(by-ty) < app.bulletYBuffer + app.tankYBuffer and b.side == 'u':
            res= True
            break
    if res:
        return i, res
    else:
        return -1, res


def isHit(tank, bullet):
    d = ((tank.y-bullet.y)**2+(tank.x-bullet.x)**2)**0.5
    if d < 5 and tank.side != bullet.side and tank.isActivated and not tank.isKilled:
        return True
    else:
        return False
def withinBounds(app, x, y, xbuffer, ybuffer):
    c1 = x-xbuffer < app.leftMargin
    c2 = x+xbuffer > app.width-app.rightMargin
    c3 = y-ybuffer < app.topMargin
    c4 = y+ybuffer > app.height-app.bottomMargin
    if c1 or c2 or c3 or c4:
        return False
    else:
        return True

def isValidRow(app, row):
    if row>=0 and row<=app.rows-1:
        return True
    else:
        return False

def isValidCol(app, col):
    if col>=0 and col<=app.cols-1:
        return True
    else:
        return False

def getImpactedCell(app, x, y, xbuffer, ybuffer, orientaion):
    p1x, p1y = x-xbuffer, y-ybuffer
    p2x, p2y = x+xbuffer, y-ybuffer
    p3x, p3y = x-xbuffer, y+ybuffer
    p4x, p4y = x+xbuffer, y+ybuffer

    row1, col1=coordinateToRowCol(p1x, p1y, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth)
    row2, col2=coordinateToRowCol(p2x, p2y, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth)
    row3, col3=coordinateToRowCol(p3x, p3y, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth)
    row4, col4=coordinateToRowCol(p4x, p4y, app.leftMargin, app.topMargin, app.rowHeight, app.colWidth)

    res= [[row1, col1], [row2, col2], [row3, col3], [row4, col4]]
    if orientaion ==0:
        ores= [res[0], res[1]]
    if orientaion ==1:
        ores= [res[2], res[3]]
    if orientaion ==2:
        ores= [res[0], res[2]]
    if orientaion ==3:
        ores= [res[1], res[3]]
    result = []
    for i in range(len(ores)):
        if isValidRow(app, ores[i][0]) and isValidCol(app, ores[i][1]):
            result += [ores[i]]
    return result


def drawPlayerTank(app, canvas):
    if not app.playerTank.isKilled:
        canvas.create_image(app.playerTank.x, app.playerTank.y, image=ImageTk.PhotoImage(app.pTankImg))
        #hsize=9
        #canvas.create_rectangle(app.playerTank.x-9, app.playerTank.y-9, app.playerTank.x+9, app.playerTank.y+9, fill='green')
        if time.time() - app.playerTank.birth <=5:
            canvas.create_rectangle(app.playerTank.x-12, app.playerTank.y-12, app.playerTank.x+12, app.playerTank.y+12, fill='', outline = "white")
    

def cellsWillBlock(app, cells, newX, newY):
    result = False
    for cell in cells:
        #print("cell in cells:")
        #print(cell[0], cell[1])
        if cell[0] >= 0 and cell[0] <= app.rows-1 and cell[1] >= 0 and cell[1] <= app.cols-1:
            row = cell[0]
            col = cell[1]
            cres = app.map[row][col].cellType == '#' or app.map[row][col].cellType == '@'
            if cres:
                result = result or cres
    return result

def movePlayerTank(app):
    dx, dy = app.playerTank.getMoveUnit()
    newX, newY = app.playerTank.x+dx, app.playerTank.y+dy
    cells = getImpactedCell(app, newX, newY, app.tankXBuffer, app.tankYBuffer, app.playerTank.orientation)
    canMove = not cellsWillBlock(app, cells, newX, newY)
    withinBoundary = withinBounds(app, newX, newY, app.tankXBuffer, app.tankYBuffer)
    if canMove and withinBoundary:
        app.playerTank.moveTank()


def drawsideInfo(app, canvas):
    canvas.create_text(app.width-app.rightMargin/2, app.height*0.3, text=f'Incoming: {app.incomingEnemies}')
    canvas.create_text(app.width-app.rightMargin/2, app.height/2, text=f'Score: {app.score}')
    canvas.create_text(app.width-app.rightMargin/2, app.height*2/3, text=f'Lives: {app.lives}')
    canvas.create_text(app.width-app.rightMargin/2, app.height*3/4, text=f'Stage: {app.stage}')

    if app.gameOver == True:
        canvas.create_text(app.width/2, app.height/2, text='GAME OVER', fill='white', font='Arial 40 bold')
        canvas.create_text(app.width/2, app.height*2/3, text=f'SCORE: {app.score}', fill='white', font = 'Arial 30 bold')
        canvas.create_text(app.width/2, app.height*3/4, text='Q - QUIT', fill='white', font='Arial 10 bold')
    if app.stagePassed == True:
        canvas.create_text(app.width/2, app.height/2, text=f'STAGE {app.stage} PASSED', fill='white', font='Arial 40 bold')
        canvas.create_text(app.width/2, app.height*2/3, text='Press ENTER for the next stage', fill='white', font='Arial 20 italic')
        canvas.create_text(app.width/2, app.height*3/4, text='Q - QUIT', fill='white', font='Arial 10 bold')

def redrawAll(app, canvas):
    if app.menu == True:
        drawMenuScreen(app, canvas)
        if app.menuInstructions == True:
            drawInstructions(app, canvas)
    if app.menu == False:
        drawGame(app, canvas)
        drawsideInfo(app, canvas)
        drawExplosion(app, canvas)
    

runApp(width=576, height=504)