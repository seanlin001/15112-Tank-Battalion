# Generates new maps as the levels progress

class Cell:
    def __init__(self, row, col, cellType):
        self.row = row
        self.col = col
        self.cellType = cellType
        # default cellType: Empty '.'
        # cellType 1: Base 'b'
        # cellType 2: Brick '#'
        # cellType 3: Steel '@'
        # cellType 4: Water 'w'
        # cellType 5: Sand 's'

# Visual representation of the default level 1 (From Battle City)
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

def buildDefaultMap():
    return buildMapFromString(defaultLevel)
 
def buildMapFromString(mapString):
    map = dict()
    i =0
    j=0
    # print("map")
    for row in mapString.split('\n'):
        map[i]={}
        j=0
        for char in row:
            cell = Cell(i, j, char)
            map[i][j]=cell
            j+=1
        # print(i, len(map[i]))
        i+=1
    
    return map
            