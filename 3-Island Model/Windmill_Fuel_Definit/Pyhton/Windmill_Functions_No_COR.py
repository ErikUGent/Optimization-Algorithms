from typing import List
import numpy as np
import random
import operator
import pandas as pd
import json
import Windmill_Classes as WmC


def createRoute(windmillList):
    return random.sample(windmillList, len(windmillList))


def initialPopulation(popSize, windmillList):
    population = []
    for i in range(0, popSize):
        population.append(createRoute(windmillList))
    return population


def rankRoutes(population):
    fitnessResults = {}

    for i in range(0, len(population)):
        fitnessResults[i] = WmC.Fitness(population[i]).routeFitness()

    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

# Arrange the first 20 (Elitesize) by it's fitness index
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
# For the other 80 (population-Elitesize), attach a random percentage to each index.
# Then put this percentage in the right place in the ranking.
# As a result, you get 100 sorted indexes
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i, 3]:
                selectionResults.append(popRanked[i][0])
                break

    return selectionResults

# Make from index list of indexes created in the selection function, a list of ranked routes.
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])

    return matingpool


def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]
    child = childP1 + childP2

    return child


def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0, eliteSize):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)

    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            windmill1 = individual[swapped]
            windmill2 = individual[swapWith]

            individual[swapped] = windmill2
            individual[swapWith] = windmill1

    return individual


def mutatePopulation(population, mutationRate):
    mutatedPop = []

    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)

    return mutatedPop


def nextGeneration(currentGen, eliteSize, mutationRate):

    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)

    return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):

    pop = initialPopulation(popSize, population)
    writeTo(f"{', '.join(windmillObjToNames(population))} |")
    writeTo(f"{str(1 / rankRoutes(pop)[0][1])} |")

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)

    writeTo(f"{str(1 / rankRoutes(pop)[0][1])} |")

    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    print(bestRoute)
    return bestRoute


def windmill_fill_list():
    """[This function will open the JSON file with windmill data and convert it to a list of Windmill-objects]

    Returns:
        [List(WmC.Windmill())]: [A list of Windmill-objects]
    """
    list = []
    jsondata = jsonToData()

    for data in jsondata:
        list.append(WmC.Windmill(data['name'], data['x-cord'], data['y-cord']))

    return list


def writeTo(string="\n", file="Windmill_tests.md") -> None:
    """[This function will open the .md file and write to it]

        Args:
        string (str, optional): [A string that you want to be written at the bottom of the .md file. Defaults to "\n".
        file (str, optional): [The .md-file whereto you want to write]. Defaults to "Windmill_tests.md".    
    """

    file = open(file, "a")
    file.write(string)
    file.close()


def sortBestRoute(route, firstWindmill):
    routeMapped = windmillObjToNames(route)
    indexOfWindmill = routeMapped.index(firstWindmill)
    firstPart = route[:indexOfWindmill]
    lastPart = route[indexOfWindmill:]
    newRoute = lastPart + firstPart
    return newRoute

def jsonToData(file='Windmills.json', datasetName='Windmill_dataset'):
    with open(file, 'r') as f:
        datasetsdict = json.load(f)
    jsondata = datasetsdict[datasetName]
    
    return jsondata

def windmillObjToNames(listWithObjects):
    return list(map(lambda x:x.name, listWithObjects)) 