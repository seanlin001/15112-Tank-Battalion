# Useful classes/utilities to deal with game data
import decimal
import time
class Tank(object):
    def __init__(self, x, y, orientation, speed, inMove, side):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.speed = speed
        self.inMove = inMove
        self.isKilled = False
        self.side = side
        self.birth = time.time()
    
    def moveTank(self):
        dx, dy = self.getMoveUnit()
        self.x += dx
        self.y += dy

    def getMoveUnit(self):
        if self.inMove:
            speed = self.speed
        else:
            speed = 0
        if self.orientation == 0:
            return 0, -speed
        if self.orientation == 1:
            return 0, speed
        if self.orientation == 2:
            return -speed, 0
        if self.orientation == 3:
            return speed, 0

    def shootBullet(self):
        b = Bullet(self.x, self.y, self.orientation, self.speed*3, self.side)
        b.moveBullet()
        return b

class EnemyTank(Tank):
    def __init__(self, x, y, orientation, speed, inMove, isActivated, actTime, side):
        super().__init__(x, y, orientation, speed, inMove, side)
        self.isActivated = isActivated
        self.actTime = actTime

    def getMoveUnit(self, t):
        if t < 5:
            return 0, 0
        if self.inMove:
            speed = self.speed
        else:
            speed = 0
        if self.orientation == 0:
            return 0, -speed
        if self.orientation == 1:
            return 0, speed
        if self.orientation == 2:
            return -speed, 0
        if self.orientation == 3:
            return speed, 0

    def moveTank(self, t):
            dx, dy = self.getMoveUnit(t)
            self.x += dx
            self.y += dy

class Bullet(object):
    def __init__(self, x, y, orientation, speed, side):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.speed = speed
        self.side = side

    def moveBullet(self):
        dx, dy = self.getMoveUnit()
        self.x += dx
        self.y += dy

    def getMoveUnit(self):
        speed = self.speed
        if self.orientation == 0:
            return 0, -speed
        if self.orientation == 1:
            return 0, speed
        if self.orientation == 2:
            return -speed, 0
        if self.orientation == 3:
            return speed, 0

class Explosion(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 60
        self.radius = .06
    
    def getShape(self):
        #xshape = [0, 0, 3, 2, 3, 0, -1, -2, -4, -5, -2, -4, -1,0]
        #yshape = [3, 2, 3, 0, -1, -2, -4, -5, -2, -4, -1,0, 0, 0]
        xshape = [1,4.5053,0.6238,1.1159,-0.2216,-3.113,-0.9004,-5,-0.9018,-3.1254,-0.2247,1.1004,0.6214,4.4984,1]
        yshape = [0,2.1684,0.7815,4.8739,0.9751,3.9127,0.4351,0.008,-0.4322,-3.9028,-0.9744,-4.8774,-0.7835,-2.1827,0]

        x=[self.x + self.radius* self.life*z for z in xshape]
        y=[self.y + self.radius* self.life*z for z in yshape]
        return x,y
        

def rowColToCoordinate(row, col, leftmargin, topmargin, rowheight, colwidth,pos):
    #default: bottom right coordinate
    x = colwidth * (col+1) + leftmargin
    y = rowheight * (row+1) + topmargin
    if pos ==0:#center
        x -=colwidth/2
        y-=rowheight/2
    if pos ==1:#topleft
        x -=colwidth
        y-=rowheight
    if pos == 2:#topright
        y -= rowheight
    if pos == 3:#bottomleft
        x -= rowheight
    return x, y


def coordinateToRowCol(x, y, leftmargin, topmargin, rowheight, colwidth):
    #input is center x, y

    # if pos ==1:#topleft
    #     x -=colwidth/2
    #     y -=rowheight/2
    # if pos == 2:#topright
    #     x +=colwidth/2
    #     y -=rowheight/2
    # if pos == 3:#bottomleft
    #     x -=colwidth/2
    #     y +=rowheight/2
    # if pos == 4:#bottomleft
    #     x +=colwidth/2
    #     y +=rowheight/2    
    
    row = roundHalfUp((y-topmargin)/rowheight-1)
    col = roundHalfUp((x-leftmargin)/colwidth-1)
    
    return row, col

def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

class Orientation(object):
    def __init__(self, o):
        self.o = o
        # 1, 2, 3, 4 = up, down, left, right


