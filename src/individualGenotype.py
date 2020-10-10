from .solutionBoard import SolutionBoard
import random

"""
Class for each individual in a population. It goes ahead and generates the
    solution at time of creation. The brandNew flag indicates whether the
    individual is being created at the very start of a run or if it is the
    product of two parent individuals.

genotype: A list of form [[bool, (x,y)], [bool, (x,y)], ...] where the bool
            indicates whether a light should be placed on the white space
            at coordinate (x,y).
"""
class IndividualGenotype:
    def __init__(self, baseGenotype, board, config, brandNew):
        self.genotype = [gene[:] for gene in baseGenotype.genotype]
        self.alwaysLightCells = baseGenotype.alwaysLightCells

        # These are saved so that they can be used later in offspring creation
        self.baseGenotype = baseGenotype
        self.board = board
        self.config = config

        # Only create a new sequence and evaluate it if the individual comes
        #   without any parents.
        if brandNew:
            self.randomizeGenes()
            self.sol = self.generateSol(board, config)
            self.score = self.sol.score

    # Chooses a random number of lights to place and places them in random spots.
    def randomizeGenes(self):
        numOfLights = random.randrange(len(self.genotype)) + 1
        lightPositions = random.sample(self.genotype, k=numOfLights)
        for gene in lightPositions:
            gene[0] = True

    # Generates the SolutionBoard that goes along with the genotype.
    def generateSol(self, board, config):
        cellLights = [light[:] for light in self.alwaysLightCells]
        for isLight, cell in self.genotype:
            if isLight:
                cellLights.append(cell)

        sol = SolutionBoard(board, config, cellLights)
        return sol

    """
    This overwrites the "IndividualGenotype + IndividualGenotype" to form
        an offspring of type IndividualGenotype from two parents.
    self is parent 1, and other is parent 2.

    This is where recombination and mutation take place.
    """
    def __add__(self, other):
        # Below creates a brand new IndividualGenotype without evaluating it yet.
        baby = IndividualGenotype(self.baseGenotype, self.board, self.config, brandNew=False)

        newGenotype = []
        for i in range(len(self.genotype)):
            # Here the combination of genes happens, with there being a 50/50 chance
            #   of which parent the child inherits the gene from.
            whichGene = random.randint(1, 2)
            if whichGene == 1:
                newGene = self.genotype[i]
            else:
                newGene = other.genotype[i]
            # Mutation happens below. Currently, about 1 gene per generation is mutated.
            shouldMutate = random.randint(1, self.config["mutationRate"])
            if shouldMutate == 1:
                newGene[0] = not newGene[0]
            newGenotype.append(newGene)

        # Sets the new genotype and evaluates it.
        baby.genotype = newGenotype
        baby.sol = baby.generateSol(self.board, self.config)
        baby.score = baby.sol.score

        return baby
