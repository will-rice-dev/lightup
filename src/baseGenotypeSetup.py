from .solutionBoard import SolutionBoard
import numpy as np

# Returns a BaseGenotype class defined at the bottom of the file.
def getBaseGenotype(board, config):
    whiteCells = sorted(board.whiteCells)
    baseGenotype = []

    if config["validityForcedInit"]:
        alwaysLightCells = forceValidity(board, config)
        baseGenotype = BaseGenotype(board, config, alwaysLightCells)
    else:
        baseGenotype = BaseGenotype(board, config)

    print(f"Base Genotype: {baseGenotype.genotype}")
    print(f"Always Light Cells: {baseGenotype.alwaysLightCells}")
    return baseGenotype

"""
Only run if validityForcedInit is in the config file.
It returns a list of form [(x,y), (x,y), ...] where (x,y) are coordinates
    where a light should always be placed.
"""
def forceValidity(board, config):
    blackCellsWithMult = sorted(board.blackCells)
    runAgainFlag = True

    neverLightCells = []
    alwaysLightCells = []

    # The while loop is continually run until there are no more changes defined below.
    while runAgainFlag:
        runAgainFlag = False
        cellsToRemove = []
        for x, y in blackCellsWithMult:
            sol = SolutionBoard(board, config, alwaysLightCells)
            boardCopy = np.copy(sol.board)

            curCell = boardCopy[x][y]
            if curCell == 5:
                cellsToRemove.append((x,y))

            neighbors = getNeighbors(board, boardCopy, x, y, neverLightCells)
            if curCell == 0:
                cellsToRemove.append((x,y))
                neverLightCells += neighbors
                # Run the loop again because of new neverLightCells.
                runAgainFlag = True
            elif len(neighbors) == curCell:
                alwaysLightCells += neighbors
                # Run the loop again because of new lit spots on board.
                runAgainFlag = True
                cellsToRemove.append((x,y))
        for cell in cellsToRemove:
            blackCellsWithMult.remove(cell)

    return alwaysLightCells

# Returns all neighbors of (x,y) where a light could possibly be placed.
def getNeighbors(board, boardCopy, x, y, neverLightCells):
    xLimit = board.x
    yLimit = board.y
    neighbors = []
    if x > 0:
        tempX = x - 1
        if boardCopy[tempX][y] == -1 and (tempX, y) not in neverLightCells:
            neighbors.append((tempX, y))
    if x < (xLimit - 1):
        tempX = x + 1
        if boardCopy[tempX][y] == -1 and (tempX, y) not in neverLightCells:
            neighbors.append((tempX, y))

    if y > 0:
        tempY = y - 1
        if boardCopy[x][tempY] == -1 and (x, tempY) not in neverLightCells:
            neighbors.append((x, tempY))
    if y < (yLimit - 1):
        tempY = y + 1
        if boardCopy[x][tempY] == -1 and (x, tempY) not in neverLightCells:
            neighbors.append((x, tempY))

    return neighbors

"""
Below is a class with a few helpful variables used in every future individual.

genotype: A list of form [[False, (x,y)], [False, (x,y)], ...] where
            the boolean is whether the light is placed in the (x,y) white space.
            Each boolean is set to False because this is the base version.
alwaysLightCells: A list of form [(x,y), (x,y), ...] where
            (x,y) are coordinates of white cells where lights should always be
            placed. This is empty if validityForcedInit is not in the config file
"""
class BaseGenotype:
    def __init__(self, board, config, alwaysLightCells=[]):
        sol = SolutionBoard(board, config, alwaysLightCells)
        whiteCellsList = np.argwhere(sol.board == -1)

        self.genotype = []
        for x, y in whiteCellsList:
            self.genotype.append([False, (x, y)])

        self.alwaysLightCells = alwaysLightCells
