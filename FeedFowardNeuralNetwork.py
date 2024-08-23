import random
import math
from GenericAlgorithm import *
import numpy as np

def randomFloat(min=0, max=1):
    return min + (max - min) * random.random()

def randomInteger(min=0, max=2) -> int:
    return min + int((max - min) * random.random())

def relu(n):
    return n if n >= 0 else 0

def sigmoid(n):
    return 1 / (1 + np.exp(-n))

def tanh(n):
    # return ((math.e ** n) - (math.e ** -n)) / ((math.e ** n) + (math.e ** -n))
    return math.tanh(n)

def softmax(arr):

    #d = sum([round(math.e ** i, 5) for i in arr])
    s = 0
    for i in arr:
        s += math.e ** i


    return [(math.e ** i) / s for i in arr]

class NeuralNetwork(Individual):

    MINVALUE, MAXVALUE = -0.5, 0.5

    MINWEIGHT, MAXWEIGHT = MINVALUE, MAXVALUE
    MINBIAS, MAXBIAS = MINVALUE, MAXVALUE

    def __init__(self, num_inputs, num_hidden, num_output, values=[], activation_func=tanh, output_func=tanh):
        
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.activation_func = activation_func
        self.output_func = output_func
        self.fitness = 0

        if values == []:
            
            self.weights_hidden_layer = [randomFloat(self.MINWEIGHT, self.MAXWEIGHT) for _ in range(num_inputs * num_hidden)]
            self.weights_output_layer = [randomFloat(self.MINWEIGHT, self.MAXWEIGHT) for _ in range(num_hidden * num_output)]

            self.bias_hidden_layer = [randomFloat(self.MINBIAS, self.MAXBIAS) for _ in range(num_hidden)]
            self.bias_output_layer = [randomFloat(self.MINBIAS, self.MAXBIAS) for _ in range(num_output)]
        
        else:

            self.weights_hidden_layer = values[: num_inputs * num_hidden]
            n = num_inputs * num_hidden

            self.bias_hidden_layer = values[ n: n + num_hidden ]
            n += num_hidden

            self.weights_output_layer = values[ n : n + num_hidden * num_output ]
            n += num_hidden * num_output

            self.bias_output_layer = values[ n : n + num_output ]

#         print(f"""Weights hidden layer: {self.weights_hidden_layer}
# Bias hidden layer: {self.bias_hidden_layer}
# Weights output layer: {self.weights_output_layer}
# Bias output layer: {self.bias_output_layer}""")

            
    def output(self, inputValues):

        hiddenLayer = self.bias_hidden_layer.copy()
        outputLayer = self.bias_output_layer.copy()

        #print(f"HiddenLayer: {hiddenLayer}\nOutputLayer: {outputLayer}")

        for i in range(self.num_hidden):
            for j in range(self.num_inputs):

                hiddenLayer[i] += inputValues[j] * self.weights_hidden_layer[ i * self.num_inputs + j ]

            hiddenLayer[i] = self.activation_func(hiddenLayer[i])

        for i in range(self.num_output):
            for j in range(self.num_hidden):

                outputLayer[i] += hiddenLayer[j] * self.weights_output_layer[ i * self.num_hidden + j ]

            if self.output_func != softmax: outputLayer[i] = self.output_func(outputLayer[i])
        
        if self.output_func == softmax: outputLayer = softmax(outputLayer)
        return outputLayer



    def getNeuralNetwork(self):
        return self.weights_hidden_layer + self.bias_hidden_layer + self.weights_output_layer + self.bias_output_layer
    
    def getFitness(self):
        return self.fitness
    
    def setFitness(self, fitness = 0):
        self.fitness = fitness
    
    def getNNSizes(self) -> tuple[int, int, int]:
        return self.num_inputs, self.num_hidden, self.num_output
    
    @classmethod
    def gerateNN(cls, input=3, hidden=10, output=1):
        return NeuralNetwork(input, hidden, output, values=[], activation_func=tanh, output_func=tanh)
    
    @classmethod
    def getNNFromFile(cls, num_input: int, num_hidden: int, num_output: int, fileName: str ="Generic Algorithm Result.txt"):

        file = open(fileName, "r")
        values = file.read()[2:-2]
        values = values.split(",")
        
        values = [float(value) for value in values]
        #print(values)
        return NeuralNetwork(num_input, num_hidden, num_output, values)
    
    def __str__(self) -> str:
        return f"[{self.getNeuralNetwork()}]"




    
    




    
