import numpy as np

"""
The class SolutionBoard was made to keep track of variables for made solutions.
The only variables required to make one are:

startBoard:     The board with black cells, but no placed lights yet.
config:         The configuration dict.
lightPositions: A list of tuples (x, y) for light bulbs to be placed.

The board is created with the following numbers and what they represent:

-9:         A lit up white cell.
-1:         A white cell that is not lit up.
0 to 4:     Black cells with exactly that many adjacent lights.
5:          A blank black cell.
10:         A light bulb
"""
class SolutionBoard:
    def __init__(self, startBoard, config, lightPositions):
        # Copys the starting board to avoid changing by reference the board
        # without lights.
        self.board = np.copy(startBoard.board)

        self.config = config
        self.lightPositions = lightPositions

        # Copys over some useful variables from the board in the next few lines.
        self.blackCells = startBoard.blackCells
        self.xLimit = startBoard.x
        self.yLimit = startBoard.y
        self.whiteCount = startBoard.whiteCount

        # The lit cell count starts off at the number of bulbs being sent.
        self.litCount = len(lightPositions)

        self.placeLights()

        # Later going to be added to and multiplied by penalty coefficient.
        self.lightViolations = 0
        self.blackCellViolations = 0
        self.violations = self.lightViolations + self.blackCellViolations
        self.isValid = True

        # Really should be called fitness, but ran out of time to change
        # throughout the whole code.
        self.setLitCount()

        if "MOEA" == config["searchAlgorithm"]:
            firstObj = self.litCount
            secondObj = 1 / (self.lightViolations + 1) # Add one to avoid 1/0
            thirdObj = 1 / (self.blackCellViolations + 1) # Add one to avoid 1/0
            self.moea = (firstObj, secondObj, thirdObj)
            return

        self.score = self.litCount
        self.penalize()
        # I do this here to make the penalty function easier to tune.
        #   It is a lot harder to tune decimal penalty coefficients.
        self.score /= self.whiteCount

    def penalize(self):
        if "penaltyCoefficient" in self.config:
            penalty = self.violations * self.config["penaltyCoefficient"]
            self.score -= penalty
            if self.violations > 0:
                self.isValid = False
        else:
            if self.violations > 0:
                self.score = 0

    def placeLights(self):
        for x, y in self.lightPositions:
            self.board[x][y] = 10

    def setLitCount(self):
        # Checks to see if the config is enforcing the black number constraint.
        if self.config["enforceBlackCellConstraint"]:
            self.isBlackCellValid() # Increases the number of violations.

        for x, y in self.lightPositions:
            # These functions count number of lit cells and increase the number
            #   of violations if they run into another light.
            self.upX(x, y)
            self.downX(x, y)
            self.upY(x, y)
            self.downY(x, y)

    # The next four functions go through the board for each light and "light up"
    # the surrounding cells. If they run into another light, the functions
    # will return True, triggering the score to become zero.
    def upX(self, x, y):
        tempX = x + 1
        while tempX != self.xLimit:
            cellVal = self.board[tempX][y]
            if cellVal == 10:
                self.lightViolations += 1
                break
            elif cellVal  >= 0:
                break
            elif cellVal == -1:
                self.board[tempX][y] = -9
                self.litCount += 1
            tempX += 1

    def upY(self, x, y):
        tempY = y + 1
        while tempY != self.yLimit:
            cellVal = self.board[x][tempY]
            if cellVal == 10:
                self.lightViolations += 1
                break
            elif cellVal  >= 0:
                break
            elif cellVal == -1:
                self.board[x][tempY] = -9
                self.litCount += 1
            tempY += 1

    def downX(self, x, y):
        tempX = x - 1
        while tempX != -1:
            cellVal = self.board[tempX][y]
            if cellVal == 10:
                self.lightViolations += 1
                break
            elif cellVal  >= 0:
                break
            elif cellVal == -1:
                self.board[tempX][y] = -9
                self.litCount += 1
            tempX -= 1

    def downY(self, x, y):
        tempY = y - 1
        while tempY != -1:
            cellVal = self.board[x][tempY]
            if cellVal == 10:
                self.lightViolations += 1
                break
            elif cellVal  >= 0:
                break
            elif cellVal == -1:
                self.board[x][tempY] = -9
                self.litCount += 1
            tempY -= 1

    # Returns True only if all black cell conditions are met.
    # Does not check validity of lights hitting each other.
    def isBlackCellValid(self):
        for x, y in self.blackCells:
            cellVal = self.board[x][y]
            if cellVal == 5:
                continue

            neighboringLights = 0
            if x != 0:
                tempX = x - 1
                if self.board[tempX][y] == 10:
                    neighboringLights += 1
            if x != (self.xLimit - 1):
                tempX = x + 1
                if self.board[tempX][y] == 10:
                    neighboringLights += 1

            if y != 0:
                tempY = y - 1
                if self.board[x][tempY] == 10:
                    neighboringLights += 1
            if y != (self.yLimit - 1):
                tempY = y + 1
                if self.board[x][tempY] == 10:
                    neighboringLights += 1

            if neighboringLights != cellVal:
                self.blackCellViolations += abs(neighboringLights - cellVal)

    # Returns the positions of the placed lights in a format
    # suitable for the solution output file.
    def getTxt(self):
        lights = sorted(self.lightPositions)
        lightsReturn = str(self.litCount) + "\n"
        for x, y in lights:
            x += 1
            y += 1
            lightsReturn += str(x) + " " + str(y) + "\n"
        return lightsReturn

    def getMOEATxt(self):
        lights = sorted(self.lightPositions)
        lightsReturn = ""
        for x, y in lights:
            x += 1
            y += 1
            lightsReturn += str(x) + " " + str(y) + "\n"
        return lightsReturn
