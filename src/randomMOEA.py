import json
import random
from .baseGenotypeSetup import getBaseGenotype
from .individualGenotype import IndividualGenotype
from .genotypeOps import breed, survivalSelection
from .moeaOps import *

def runAllMOEA(board, config, probPath):
    log = "Result Log\n\n"

    log += "Problem Instance File: " + probPath + "\n"
    log += "Solution File: " + config["solPath"] + "\n"
    log += "Random Seed: " + str(config["usedSeed"]) + "\n\n"

    # Delelte usedSeed because it is not a user parameter, thus should not be put in the log file.
    del config["usedSeed"]

    log += "Config Used:\n"
    log += json.dumps(config) + "\n\n"

    # Creates the base genotype to be used by all future individuals.
    baseGenotype = getBaseGenotype(board, config)

    firstRun = True
    for i in range(config["numOfRuns"]):
        log += "Run " + str(i + 1) + '\n'

        runLog, topLevel = singleRunMOEA(board, config, baseGenotype)
        log += runLog

        # This keeps track of all runs and saves the very best
        # solution to later output.
        if firstRun:
            bestLevelOfAllRuns = topLevel
            firstRun = False
        else:
            bestLevelOfAllRuns, _ = compareDomination(bestLevelOfAllRuns, topLevel)

        log += "\n"
    print(log)

    # This will return a string of text that can be put onto the end
    #   of the solution output file.
    #solTxt = bestSolOfAllRuns.sol.getTxt()
    solTxt = getSolTxt(bestLevelOfAllRuns)
    return log, solTxt

def singleRunMOEA(board, config, baseGenotype):
    runLog = ""
    bestSol = ""

    # The initial population of size mu is created below.
    population = []
    for i in range(config["mu"]):
        population.append(IndividualGenotype(baseGenotype, board, config, brandNew=True))
    numOfFitnessEvals = config["mu"]
    levels = getLevels(population)

    avg1, b1, avg2, b2, avg3, b3 = evalPopulation(population)
    runLog += f"{numOfFitnessEvals}\t{avg1}\t{b1}\t{avg2}\t{b2}\t{avg3}\t{b3}\n"

    bestTopLevel = levels[0]
    evalsWithoutChange = 0
    if "noChangeForNEvals" in config:
        noChangeForNEvals = config["noChangeForNEvals"]
    else:
        noChangeForNEvals = config["numOfFitnessEvals"] # This will never terminate early.

    while numOfFitnessEvals < config["numOfFitnessEvals"]:
        population = evolve(board, config, population)
        numOfFitnessEvals += config["lambda"]

        levels = getLevels(population)
        avg1, b1, avg2, b2, avg3, b3 = evalPopulation(population)
        runLog += f"{numOfFitnessEvals}\t{avg1}\t{b1}\t{avg2}\t{b2}\t{avg3}\t{b3}\n"

        bestTopLevel, stayedSame = compareDomination(bestTopLevel, levels[0])
        if stayedSame:
            evalsWithoutChange += config["lambda"]
            if evalsWithoutChange >= noChangeForNEvals:
                break
        else:
            evalsWithoutChange = 0

    return runLog, bestTopLevel

def evolve(board, config, population):
    # Parent Select, offspring creation, and mutation.
    population = breed(population, board, config)
    getLevels(population) # Done to get scores on new genotypes
    # Survivor selection.
    return survivalSelection(population, board, config)

# Returns useful info about the population.
def evalPopulation(population):
    total1 = 0
    total2 = 0
    total3 = 0
    best1 = -1
    best2 = -1
    best3 = -1
    for ind in population:
        curMoea = ind.moea
        total1 += curMoea[0]
        total2 += curMoea[1]
        total3 += curMoea[2]

        if curMoea[0] > best1:
            best1 = curMoea[0]
        if curMoea[1] > best2:
            best2 = curMoea[1]
        if curMoea[2] > best3:
            best3 = curMoea[2]

    total1 /= len(population)
    total2 /= len(population)
    total3 /= len(population)

    return total1, best1, total2, best2, total3, best3

def getSolTxt(level):
    solTxt = ""
    numOfSols = len(level)
    for ind in level:
        moea = ind.moea
        solTxt += f"{moea[0]}\t{moea[1]}\t{moea[2]}\t{numOfSols}\n"
        solTxt += ind.sol.getMOEATxt()

    return solTxt
