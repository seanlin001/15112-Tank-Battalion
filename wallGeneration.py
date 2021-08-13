# Generates new maps as the levels progress
import random
import math
class Cell:
    def __init__(self, row, col, cellType):
        self.row = row
        self.col = col
        self.cellType = cellType
        # default cellType: Empty '.'
        # cellType 1: Base 'b'
        # cellType 2: Brick '#'
        # cellType 3: Steel '@'

# Visual representation of stage 1
defaultLevel = '''..........................
..........................
...###....#...#...#...#...
..#...#...@@.@@...#...#...
..#.......#.@.#...#...#...
..#.......#.@.#...#...#...
..#.......#...#...#...#...
..#...#...#...#...#...#...
...###....#...#....###....
@@@....................@@@
@@......................@@
....#.......#......###....
...##......##.....#...#...
....#.......#.........#...
....#.......#........#....
....#.......#.......#.....
....#.......#......#......
...###.....###....#####...
..........................
..##..##..##..##..##..##..
..##..##..##..##..##..##..
..##..##..........##..##..
..##..##..........##..##..
..##..##...####...##..##..
...........#bb#...........
...........#bb#...........'''

randomTemplate = '''..........................
..........................
..........................
............@@..........@@
..........................
@@.........@@@@...........
.....###..............##..
...........######.........
..........................
.................@@.......
..........................
..........................
..........................
..........................
..........................
..........................
@@@....................@@@
..........................
..........................
..##..##..##..##..##..##..
..##..##..##..##..##..##..
..##..##..........##..##..
..##..##..........##..##..
..##..##...####...##..##..
...........#bb#...........
...........#bb#...........'''

# Random map generation method 1, randomly modifying map from template map 
def buildRandomMap(stage, row0, row1, col0, col1):
    if stage ==1:
        fillProb=0
        b2sProb=0
    else:
        fillProb = math.exp(0.1*(stage-1)-1)
        fillProb = fillProb/(1+fillProb)
        b2sProb =math.exp(.01*(stage-1)-3)
        b2sProb = b2sProb/(1+b2sProb)
    map = buildMapFromString(randomTemplate)
    count=0
    for i in range(row0, row1):
        for j in range(col0, col1):
            ch=map[i][j].cellType
            r = random.uniform(0, 1)
            if ch=='.' and r > 1- fillProb:
                map[i][j].cellType = '#'
                count+=1
            elif ch=='#' and r > 1-b2sProb:
                map[i][j].cellType = '@'
                count+=1
    return map

# Random map generation method 2, builds random map and validates with DFS
# DFS to test whether map is connected, and avoid the generation of isolated unreachable space; 
# However, DFS itself is not enough to guarantee a valid map
# This is because tanks cannot pass the aisle with width of one block only
# This limitation is solved by adding extra constrain to limit the length of steel per row

def buildRandomMap2(stage, row0, row1, col0, col1):
    if stage ==1:
        result =buildDefaultMap()
        return result

    else:
        t1=0.4
        t2=0.6
        hasValidMap = False
        result = None

        while(not hasValidMap):
            map = buildMapFromString(randomTemplate)
            for i in range(row0, row1):
                r = random.uniform(0, 1)
                k0 = col0+random.randint(0, col1-col0)
                k1 = col0+random.randint(0, col1-col0)
                kmin = min(k1,k0)
                kmax = max(k1,k0)
                if r < t1:
                    ch = '#'

                elif r < t2:
                    ch = '.'

                else:
                    ch = '@'

                for k in range(kmin, kmax):
                    s = ch
                    if k-kmin > 6 and ch =='@':
                        s = '#'
                    map[i][k] = Cell(i, k, s)

            cc = ConnectedComponent(map)
            if cc.getNC()==1:
                hasValidMap = True
                result = map
    return result

def buildDefaultMap():
    return buildMapFromString(defaultLevel)
 
def buildMapFromString(mapString):
    map = dict()
    i =0
    j=0
    for row in mapString.split('\n'):
        map[i]={}
        j=0
        for char in row:
            cell = Cell(i, j, char)
            map[i][j]=cell
            j+=1
        i+=1
    
    return map

class ConnectedComponent:
    def __init__(self, map):
        nrow = len(map.keys())
        ncol = len(map[0].keys())
        self.nrow = nrow
        self.ncol = ncol
        self.visited = [[False for i in range(ncol)] for j in range(nrow)]
        self.componentId = [[-1 for i in range(ncol)] for j in range(nrow)]
        self.count=0
        self.map=map
        for row in range(nrow):
            for col in range(ncol):
                if(self.visited[row][col]==False):
                    self.dfs(map, row, col)
                    self.count+=1
    
    # CITATION: Modified from Java implementation of DFS from Algorithms, 4th Edition by Robert Sedgewick and Kevin Wayne
    def dfs(self, map, row, col):
        self.visited[row][col]=True
        self.componentId[row][col]=self.count
        adjs = self.getConnectedNeighbor(row, col)
        for nbrow, nbcol in adjs:
            if self.visited[nbrow][nbcol]==False:
                self.dfs(map, nbrow, nbcol)

    def connected(self, row1, col1, row2, col2):
        return self.componentId[row1][col1]==self.componentId[row2][col2]

    def getComonentId(self, row, col):
        return self.componentId[row][col]
    
    def getComponentCount(self):
        return self.count

    def isValidRowCol(self, row, col):
        if 0<= row <= self.nrow-1 and 0<= col <=self.ncol-1:
            return True
        else:
            return False

    connectedType = {'.':1, '#':1, '@':2, 'b':3}
    def getConnectedNeighbor(self, row, col):
        res=[]
        nn=[[row-1, col], [row+1, col], [row, col-1], [row, col+1]]
        for i, j in nn:
            if self.isValidRowCol(i, j):
                currentchar =self.map[row][col].cellType
                nbchar = self.map[i][j].cellType
                if self.connectedType[currentchar]==self.connectedType[nbchar]:
                    res += [[i,j]]
        return res

    def getNC(self):
        indexSet = set()
        for i in range(self.nrow):
            for j in range(self.ncol):
                ch=self.map[i][j].cellType
                if ch=='.' or ch=='#':
                    indexSet.add(self.componentId[i][j])
        return len(indexSet)

# Test cases for DFS algorithm
testCase1 = '''....
@@@@
....
....'''

testCase2 = '''....
@@#@
....
....'''

testCase3 = '''....
@##@
....
....'''

def testTestCase(mapstring, id):
    print("testing case "+str(id))
    map=buildMapFromString(mapstring)
    cc = ConnectedComponent(map)
    print(mapstring)
    print("print componentId:")
    print(cc.componentId)
    print(cc.getComponentCount())
    print("getNC:")
    print(cc.getNC())

if (__name__ == '__main__'):
    testTestCase(testCase1, 1)
    testTestCase(testCase2, 2)
    testTestCase(testCase3, 3)
    mm=buildDefaultMap()