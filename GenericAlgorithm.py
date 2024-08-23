import random
from abc import ABC, abstractmethod
from FeedFowardNeuralNetwork import *


class Individual(ABC):
    def __init__(self):
        self.fitness = 0

    def getFitness(self):
        return self.fitness
    
    def addToFitness(self, fitness):
        self.fitness += fitness
    
    @abstractmethod
    def setFitness(self, fitness = 0) -> None:
        self.fitness = fitness


class GenericAlgorithm(ABC):

    OUTPUT_FILE = "Generic Algorithm Result.txt"

    def __init__(self, generations: int, populationSize: int, populationInit, parents: int, eliteIndividualsChance: int, outputFile: str = OUTPUT_FILE):
        
        print(f"""Generations: {generations}
Population Size: {populationSize}
Parents: {parents}
Elite Individuals: {eliteIndividualsChance}
Output File: {outputFile}\n""")

        self.generations = generations
        self.populationSize = populationSize
        self.parents = parents
        self.eliteIndividualsChance = eliteIndividualsChance
        self.outputFile = outputFile

        self.curGeneration = 0
        
        self.population: list[Individual] = [populationInit() for _ in range(populationSize)]
        # self.writeOutput(outputFile, self.population[0])
        self.setPopulationFitness()
        self.population.sort(key= lambda i: i.getFitness(), reverse=True)

        #print(f"""GENERATION #{self.curGeneration} Best Fitness: {self.population[0].getFitness()} AVG Fitness: {sum([i.getFitness() for i in self.population]) / populationSize}""")

        self.writeOutput(outputFile, self.population[0])


        bestNN = self.search()
        self.writeOutput(outputFile, bestNN)
    
    @abstractmethod
    def crossover(self, individuals: list[Individual]) -> Individual:
        pass

    @abstractmethod
    def mutation(self, individual: Individual) -> Individual:
        pass

    @abstractmethod
    def selectParents(self) -> list[Individual]:
        pass

    @abstractmethod
    def setPopulationFitness(self):
        pass


    
    def generateNewIndividual(self) -> Individual:

        parents = self.selectParents()
        child = self.crossover(parents)
        final = self.mutation(child)

        return final

    def randomIndividual(self) -> Individual:
        return self.population[int(random.random()*len(self.population))]
    
    def search(self) -> Individual:
        
        while self.curGeneration <= self.generations:

            self.population.sort(key= lambda i: i.getFitness(), reverse=True)
            print(f"""GENERATION #{self.curGeneration} Best Fitness: {self.population[0].getFitness()} AVG Fitness: {sum([i.getFitness() for i in self.population]) / self.populationSize}""")
            
            eliteIndividuals = int(self.eliteIndividualsChance * self.populationSize)
            newPopulation = self.population[:eliteIndividuals] 
            newPopulation += [self.generateNewIndividual() for _ in range(self.populationSize - eliteIndividuals)]

            self.population = newPopulation.copy()
            self.setPopulationFitness()
            self.writeOutput(self.outputFile, self.population[0])

            self.curGeneration += 1

        self.population.sort(key= lambda i: i.getFitness(), reverse=True)
        return self.population[0]
    
    def writeOutput(self, filename, individual: Individual):

        f = open(filename, "w")
        f.write(str(individual))
        f.close()


            

            
            
            
            





