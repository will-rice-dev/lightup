#!/usr/bin/python3
from sys import argv
from src.board import Board
from src.randomSearch import runAllRandom
from src.randomEA import runAllEA
from src.randomMOEA import runAllMOEA
import json
import random
from datetime import datetime

DEFAULT_CONFIG = "configs/defaultConfig.json"

def main():
    if len(argv) == 3:
        probPath = argv[1]
        configPath = argv[2]
    elif len(argv) == 2:
        print('Using the default config file since none was specified!')
        probPath = argv[1]
        configPath = DEFAULT_CONFIG
    else:
        print('An inappropriate number of arguments were passed!')
        return

    print(f'The problem file passed is: {probPath}')
    print(f'The config file passed is: {configPath}')
    probFile = loadFile(probPath)
    configFile = loadFile(configPath)

    board = Board(probFile)
    config = buildConfig(configFile)
    print(board)

    # The bulk of the computing goes here.
    if config["searchAlgorithm"] == "Random Search":
        logTxt, solTxt = runAllRandom(board, config, probPath)
    elif config["searchAlgorithm"] == "EA":
        logTxt, solTxt = runAllEA(board, config, probPath)
    elif config["searchAlgorithm"] == "MOEA":
        logTxt, solTxt = runAllMOEA(board, config, probPath)

    writeFile(config["logPath"], logTxt)

    solTxt = board.wholeFile + "\n" + solTxt
    writeFile(config["solPath"], solTxt)


# The following two functions abstract out
# the file loading and writing from the main method.
def loadFile(path):
    file = open(path, 'r')
    return file

def writeFile(fileName, fileString):
    file = open(fileName, 'w')
    file.write(fileString)
    file.close()

# The following reads the json config file and puts it into a python dict.
# It also sets the random seed.
def buildConfig(configFile):
    config = json.loads(configFile.read())
    configFile.close()
    if "givenSeed" in config:
        random.seed(config["givenSeed"])
        config["usedSeed"] = config["givenSeed"]
    else:
        dt = datetime.now()
        microseconds = dt.microsecond
        random.seed(microseconds)
        config["usedSeed"] = microseconds
    return config

if __name__ == '__main__':
    main()
