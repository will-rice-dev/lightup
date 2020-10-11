import random
import operator
from .individualGenotype import IndividualGenotype

# This is where the parent selection and offspring creation happen.
def breed(population, board, config):
    offspring = []

    # Offspring is passed by reference so it changes in all methods below.
    if "parentTournyK" in config:
        parentTourny(population, board, config, offspring)
    elif config["parentFitnessProp"]:
        parentFitnessProp(population, board, config, offspring)
    elif config["parentUniform"]:
        parentUniform(population, board, config, offspring)

    if config["commaSurvival"]:
        return offspring
    else:
        return population + offspring

# Selects the survivors and returns a new array with mu population size.
def survivalSelection(population, board, config):
    if "survivalTournyK" in config:
        return survivalTourny(population, board, config)
    elif config["survivalTruncation"]:
        newPop = sorted(population, key=operator.attrgetter("score"))
        newPop = newPop[::-1]
        return newPop[:config["mu"]]
    elif config["survivalUniform"]:
        return survivalUniform(population, board, config)
    elif config["survivalFitnessProp"]:
        return survivalFitnessProp(population, board, config)

def survivalTourny(population, board, config):
    popCopy = [] # Need the copy so that population in parent function is unaffected.
    for i in range(len(population)):
        popCopy.append(population[i])
    newPop = []
    while len(newPop) < config["mu"]:
        tourny = random.sample(popCopy, k=config["survivalTournyK"])
        tourny.sort(key=operator.attrgetter("score")) # This sorts the list by the score variable.
        #tourny = tourny[::-1] # This reverses the list, putting the best fitnesses at the front.

        newPop.append(tourny[-1])
        # Below removes the survivor from the population so it is not chosen twice.
        popCopy.remove(tourny[-1])

    return newPop

def survivalUniform(population, board, config):
    popCopy = [] # Need the copy so that population in parent function is unaffected.
    for i in range(len(population)):
        popCopy.append(population[i])
    newPop = []

    while len(newPop) < config["mu"]:
        survivor = random.choice(popCopy)
        popCopy.remove(survivor)
        newPop.append(survivor)

    return popCopy

def survivalFitnessProp(population, board, config):
    newPop = []

    weights = [0 for _ in range(len(population))]

    minScore = 0
    for i in range(len(population)):
        curScore = population[i].score
        if curScore < minScore:
            minScore = curScore
        weights[i] = curScore

    # The minScore ensures that all weights are at least 1e-99. This
    #   now allows for negative fitnesses. Each weight gets the minScore
    #   value (either negative or zero) subtracted from it so that each weight
    #   goes up proportionally.
    weights = [weight - minScore + 1e-99 for weight in weights]

    for i in range(config["mu"]):
        survivor = random.choices(population, weights=weights, k=1)
        survivor = survivor[0]
        newPop.append(survivor)

        index = population.index(survivor)
        weights[index] = 0 # This ensures that it will not be duplicated.

    return newPop

def parentTourny(population, board, config, offspring):
    for i in range(config["lambda"]):
        tourny1 = random.sample(population, k=config["parentTournyK"])
        tourny1.sort(key=operator.attrgetter("score")) # This sorts the list by the score variable.
        parent1 = tourny1[-1]
        population.remove(parent1) # Remove temporarily to avoid asexual reproduction.

        tourny2 = random.sample(population, k=config["parentTournyK"])
        tourny2.sort(key=operator.attrgetter("score")) # This sorts the list by the score variable.
        parent2 = tourny2[-1]
        population.append(parent1) # Add back the first parent.

        # Offspring creation happens here by adding the two parents.
        # This uses a custom addition operator of the IndividualGenotype class
        #   in order to recombine the parernts and mutate the child.
        baby = parent1 + parent2
        offspring.append(baby)

def parentFitnessProp(population, board, config, offspring):
    weights = [0 for _ in range(len(population))]
    totalWithScores = 0

    minScore = 0
    for i in range(len(population)):
        curScore = population[i].score
        if curScore < minScore:
            minScore = curScore
        weights[i] = curScore

    # The minScore ensures that all weights are at least 1e-99. This
    #   now allows for negative fitnesses. Each weight gets the minScore
    #   value (either negative or zero) subtracted from it so that each weight
    #   goes up proportionally.
    weights = [weight - minScore + 1e-99 for weight in weights]

    for i in range(config["lambda"]):
        pick1 = random.choices(population, weights=weights, k=1)
        pick1 = pick1[0]

        # This is done to ensure that there is no asexual breeding.
        # It sets the weight of the chosen parent to zero, while also
        #   saving the initial weight in a temp variable.
        index = population.index(pick1)
        temp = weights[index]
        weights[index] = 0

        pick2 = random.choices(population, weights=weights, k=1)
        pick2 = pick2[0]

        # Resets the 1st parent's weight back to its initial value
        weights[index] = temp

        # Offspring creation happens here by adding the two parents.
        # This uses a custom addition operator of the IndividualGenotype class
        #   in order to recombine the parernts and mutate the child.
        baby = pick1 + pick2
        offspring.append(baby)

def parentUniform(population, board, config, offspring):
    for i in range(config["lambda"]):
        parent1 = random.choice(population)
        population.remove(parent1) # Remove temporarily to avoid asexual reproduction.

        parent2 = random.choice(population)
        population.append(parent1) # Add back the first parent.

        # Offspring creation happens here by adding the two parents.
        # This uses a custom addition operator of the IndividualGenotype class
        #   in order to recombine the parernts and mutate the child.
        baby = parent1 + parent2
        offspring.append(baby)
