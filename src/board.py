import numpy as np

# Board was made into a class instead of a simple 2d array
# because there were other variables to keep track of.
# The board itself is stored as a 2d numpy array in self.board
class Board:
    def __init__(self, probFile):
        # Eventually becomes list of tuples (x, y)
        self.blackCells = []

        # Reads the whole file to save for the solution file later.
        # Seeks back to zero so the file can be read and processed later.
        self.wholeFile = probFile.read()
        probFile.seek(0)

        # The lengths of x and y are stored here.
        self.x = int(probFile.readline())
        self.y = int(probFile.readline())

        self.board = self.buildBoard(probFile)

        # Eventually becomes list of tuples (x, y)
        self.whiteCells = self.getWhiteCells()
        self.whiteCount = len(self.whiteCells)
        
        probFile.close()

    def buildBoard(self, probFile):
        # White spaces are stored as -1 in this representation.
        # This seperates them from the 0 block.
        board = np.zeros((self.x, self.y), dtype='int') - 1

        for line in probFile:
            line = line.split()
            # Subtract one from x and y because the file starts
            # the origin at (1,1) not (0,0)
            curX = int(line[0]) - 1
            curY = int(line[1]) - 1
            curZ = int(line[2])

            self.blackCells.append((curX, curY))
            board[curX][curY] = curZ

        return board

    # The white cells are gotten by creating tuples of all cells
    # and then subtracting the black cells.
    def getWhiteCells(self):
        allCells = []
        for i in range(self.x):
            for j in range(self.y):
                allCells.append((i,j))

        return list(set(allCells) - set(self.blackCells))

    # This allows the user to print the board in the way that
    # the input file submits it by rotating it 90 degrees.
    def __str__(self):
        rotatedBoard = np.rot90(self.board)
        return np.array_str(rotatedBoard)
