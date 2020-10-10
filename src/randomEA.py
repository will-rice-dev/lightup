import json
import random
from .baseGenotypeSetup import getBaseGenotype
from .individualGenotype import IndividualGenotype
from .genotypeOps import breed, survivalSelection

def runAllEA(board, config, probPath):
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

    bestOfAllRuns = -1
    for i in range(config["numOfRuns"]):
        log += "Run " + str(i + 1) + '\n'

        runLog, runSol = singleRunEA(board, config, baseGenotype)
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
    #   of the solution output file.
    solTxt = bestSolOfAllRuns.sol.getTxt()
    return log, solTxt

def singleRunEA(board, config, baseGenotype):
    bestRunSoFarScore = -1
    runLog = ""
    bestSol = ""

    # The initial population of size mu is created below.
    population = []
    for i in range(config["mu"]):
        population.append(IndividualGenotype(baseGenotype, board, config, brandNew=True))
    numOfFitnessEvals = config["mu"]

    avgScore, bestScoreInPop, bestIndividualInRun = evalPopulation(population)
    runLog += str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreInPop) + '\n'

    if "noChangeForNEvals" not in config:
        while numOfFitnessEvals < config["numOfFitnessEvals"]:
            # Bulk of computing is done below.
            population = evolve(board, config, population)
            numOfFitnessEvals += config["lambda"]

            avgScore, bestScoreInPop, bestIndividualInPop = evalPopulation(population)
            runLog += str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreInPop) + '\n'

            if bestScoreInPop > bestIndividualInRun.score:
                bestIndividualInRun = bestIndividualInPop
    else:
        evalsWithoutChange = 0
        while numOfFitnessEvals < config["numOfFitnessEvals"]:
            population = evolve(board, config, population)
            numOfFitnessEvals += config["lambda"]

            avgScore, bestScoreInPop, bestIndividualInPop = evalPopulation(population)
            runLog += str(numOfFitnessEvals) + "\t" + str(avgScore) + '\t' + str(bestScoreInPop) + '\n'

            if bestScoreInPop > bestIndividualInRun.score:
                bestIndividualInRun = bestIndividualInPop
                evalsWithoutChange = 0
            else:
                evalsWithoutChange += config["lambda"]
                if evalsWithoutChange >= config["noChangeForNEvals"]:
                    break
    return runLog, bestIndividualInRun

def evolve(board, config, population):
    # Parent Select, offspring creation, and mutation.
    population = breed(population, board, config)
    # Survivor selection.
    return survivalSelection(population, board, config)

# Returns useful info about the population.
def evalPopulation(population):
    totScore = 0
    bestScore = -1
    bestIndividual = ""

    for individual in population:
        curScore = individual.score
        totScore += curScore
        if curScore > bestScore:
            bestScore = curScore
            bestIndividual = individual

    avgScore = totScore / len(population)
    return avgScore, bestScore, bestIndividual
