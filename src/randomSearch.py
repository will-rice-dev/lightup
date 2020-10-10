import json
import random
from .solutionBoard import SolutionBoard

def runAllRandom(board, config, probPath):
    log = "Result Log\n\n"

    log += "Problem Instance File: " + probPath + "\n"
    log += "Solution File: " + config["solPath"] + "\n"
    log += "Random Seed: " + str(config["usedSeed"]) + "\n\n"

    # Delelte usedSeed because it is not a user parameter, thus should not be put in the log file.
    del config["usedSeed"]

    log += "Config Used:\n"
    log += json.dumps(config) + "\n\n"

    bestOfAllRuns = -1
    for i in range(config["numOfRuns"]):
        log += "Run " + str(i + 1) + '\n'

        runLog, runSol = singleRunRandom(board, config)
        log += runLog

        # This keeps track of all runs and saves the very best
        # solution to later output.
        if runSol.score > bestOfAllRuns:
            bestOfAllRuns = runSol.score
            bestSolOfAllRuns = runSol

        log += "\n"
    log += "Best of all runs: " + str(bestSolOfAllRuns.score)
    print(log)

    # This will return a string of text that can be put onto the end
    # of the solution output file.
    solTxt = bestSolOfAllRuns.getTxt()
    return log, solTxt

def singleRunRandom(board, config):
    bestRunSoFar = -1
    runLog = ""
    bestSol = ""
    for i in range(config["numOfFitnessEvals"]):
        # Creates the random search and stores the
        # fitness and the solution itself.
        curRun, curSol = randomBoard(board, config)

        if curRun > bestRunSoFar:
            runLog += str(i + 1) + "\t" + str(curRun) + '\n'
            bestRunSoFar = curRun
            bestSol = curSol

    return runLog, bestSol

def randomBoard(board, config):
    # First selects a number of lights to place.
    # Then it picks those lights from the list of white cells.
    numOfLights = random.randrange(board.whiteCount) + 1
    lightPositions = random.sample(board.whiteCells, k=numOfLights)

    # Sends the light positions to get back a solution board.
    sol = SolutionBoard(board, config, lightPositions)
    return sol.score, sol
