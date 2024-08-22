import random
from FeedFowardNeuralNetwork import *
from GenericAlgorithm import *
from GenericAlgorithm import Individual
from PopGame import*



class NeuralNetworkGenericAlgorithm(GenericAlgorithm):
    def __init__(self, generations: int, population: int, parents: int, k_tournment: int, eliteIndividuals: int, mutation_chance: float, mutation_index: float):

        self.k_tournment = k_tournment
        self.mutation_chance = mutation_chance
        self.mutation_index = mutation_index
        super().__init__(generations, population, NeuralNetwork.gerateNN, parents, eliteIndividuals)

    def generateIndividuals(self) -> list[Individual]:
        return [NeuralNetwork(3, 20, 1, activation_func=tanh, output_func=tanh) for i in range(super().population)]
    
    def selectParents(self) -> list[Individual]:

        individuals: list[Individual] = []

        for i in range(self.k_tournment):
            individuals.append(super().randomIndividual())

        return individuals

    def crossover(self, individuals: list[Individual]) -> Individual:

        neuralNetworks = [nn.getNeuralNetwork() for nn in individuals]
        size = len(neuralNetworks[0])

        child = [neuralNetworks[randomInteger(max=len(individuals))][i] for i in range(size)]
        sizes = individuals[0].getNNSizes()
        newNN = NeuralNetwork(sizes[0], sizes[1], sizes[2], child)

        return newNN
    
    def mutation(self, individual: Individual) -> Individual:
        
        if (random.random() > self.mutation_chance): return individual
        neuralNetwork = individual.getNeuralNetwork()

        for i in range(int(len(neuralNetwork) * self.mutation_index)):
            index = randomInteger(max=len(neuralNetwork))

            if type(neuralNetwork[index]) == list: neuralNetwork[index] = [randomNumber(NeuralNetwork.MINVALUE, NeuralNetwork.MAXVALUE) for i in range(len(neuralNetwork[index]))]
            else: neuralNetwork[index] = randomNumber(NeuralNetwork.MINVALUE, NeuralNetwork.MAXVALUE)

        
        sizes = individual.getNNSizes()
        newNN = NeuralNetwork(sizes[0], sizes[1], sizes[2], neuralNetwork)

        return newNN
    
    

    def setPopulationFitness(self):
        for i in range(len(self.population)):

            nn = self.population[i]
            g = Game(nn2 = nn, frames=1200)
            score = g.runGame()

            nn.setFitness(score[1][1])





    

        

if __name__ == "__main__":
    NeuralNetworkGenericAlgorithm(100, 50, 3, 3, 10, 0.2, 0.1)

