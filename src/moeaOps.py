
# Returns the more dominant of a vs. b.
#   Also returns True if a is more dominant.
def compareDomination(a, b):
    aDoms = 0
    bDoms = 0
    for ind in a:
        for other in b:
            if dominates(ind.moea, other.moea):
                aDoms += 1
                break
    for ind in b:
        for other in a:
            if dominates(ind.moea, other.moea):
                bDoms += 1
                break
    if aDoms >= bDoms:
        return a, True
    else:
        return b, False

# Returns a list of lists, representing the levels of domination where
#   levels[0] is the most dominant. Each individual item is a genotype.
def getLevels(population):
    levels = []
    for ind in population:
        insert(levels, 0, ind) # Always try to insert each genotype at the top.

    for i in range(len(levels)):
        curLevel = i + 1
        for ind in levels[i]:
            # Fitness is 1/level so that higher fitness means more dominant.
            ind.score = 1 / curLevel

    return levels

# Returns True if and only if A dominates B.
def dominates(a, b):
    flag = False
    for i in range(len(a)):
        if a[i] < b[i]:
            return False
        if a[i] > b[i]:
            flag = True
    return flag

# This function inserts a new genotype into the levels based on domination.
#   It also kicks out genotypes that it dominates into the next level.
def insert(levels, i, cur):
    if i == len(levels):
        levels.append([cur])
        return

    addFlag = True
    toRemoveFromLevel = [] # Items to later be removed, once all iteration is done.
    for ind in levels[i]:
        if dominates(cur.moea, ind.moea):
            insert(levels, i+1, ind) # This kicks the dominated ind to the next level.
            toRemoveFromLevel.append(ind)
        elif dominates(ind.moea, cur.moea):
            insert(levels, i+1, cur) # cur was dominated so it moves to the next level.
            addFlag = False
            break

    if addFlag:
        levels[i].append(cur)
    for ind in toRemoveFromLevel:
        levels[i].remove(ind)
