# Pop Game IA

A small Python project that implements a Pong-style game with an evolving neural network AI using a generic genetic algorithm.

## Overview

- `Play.py`: a simple playable Pong-style game where the left paddle is controlled by the keyboard and the right paddle is a hard-coded bot.
- `PopGame.py`: the Pong game engine designed to run neural networks as paddle controllers.
- `FeedFowardNeuralNetwork.py`: a feed-forward neural network implementation with support for custom activation/output functions.
- `GenericAlgorithm.py`: a generic evolutionary algorithm base class for populations of `Individual` objects.
- `NeuralNetworkGenericAlgorithm.py`: a genetic algorithm implementation that evolves `NeuralNetwork` objects by playing games and using fitness score.

## Requirements

- Python 3.10+ (or compatible)
- `pygame`
- `numpy`

Install dependencies with:

```bash
python3 -m pip install pygame numpy
```

## How to run the game

### 1. Play manually with `Play.py`

This is the easiest way to run the game.

```bash
python3 Play.py
```

Controls:

- `W` / `S`: move the left paddle up/down
- Arrow keys: nudge the ball in the window for testing

The right paddle is controlled by a simple rule-based bot that tracks the ball vertically.

### 2. Train a neural network with genetic evolution

Run the genetic algorithm trainer:

```bash
python3 NeuralNetworkGenericAlgorithm.py
```

This will:

- initialize a population of neural networks
- evaluate each network by letting it play in `PopGame.Game` as the right paddle (`nn2`)
- use tournament selection, crossover, and mutation to create new generations
- write the best evolved neural network to `Generic Algorithm Result.txt`

### 3. Run a neural-network-controlled game in `PopGame.py`

`PopGame.py` contains the game logic for using neural networks as controllers. It does not have a direct command-line entry point, but you can launch it from a Python script or interactive session.

Example to run a trained model from `Generic Algorithm Result.txt`:

```python
from FeedFowardNeuralNetwork import NeuralNetwork
from PopGame import Game

nn = NeuralNetwork.getNNFromFile(3, 20, 1, "Generic Algorithm Result.txt")
game = Game(nn2=nn)
score = game.runGame()
print("Result:", score)
```

### 4. Let two models play each other

Use two neural networks with `Game(nn1=..., nn2=...)`:

```python
from FeedFowardNeuralNetwork import NeuralNetwork
from PopGame import Game

nn1 = NeuralNetwork.getNNFromFile(3, 20, 1, "Generic Algorithm Result.txt")
nn2 = NeuralNetwork.getNNFromFile(3, 20, 1, "Generic Algorithm Result.txt")

game = Game(nn1=nn1, nn2=nn2)
score = game.runGame()
print("Result:", score)
```

This will make both paddles controlled by neural networks.

## How to play against the model

Currently:

- `Play.py` is human vs a simple bot.
- `PopGame.py` is built to run neural networks automatically.


## AI and Evolution Architecture

### Neural network structure

The model is a classic feed-forward neural network with:

- 3 input values
- 1 hidden layer
- 1 output neuron by default
- `tanh` activation and output functions

The network encodes both weights and biases as a single linear genome.

### Network inputs used by the game

`PopGame.Game.nextMove()` sends the following values to the neural network:

1. paddle Y position
2. ball Y position
3. distance from the ball to the paddle

The output is interpreted as a movement command:

- with 1 output: move up or down depending on the sign
- with 2 outputs: compare values to choose up/down
- with 3 outputs: choose one of [up, none, down]

### Genetic Algorithm logic

`GenericAlgorithm.py` implements the evolution loop:

- initialize a population of individuals
- evaluate fitness for each individual
- sort by fitness descending
- keep a small elite fraction unchanged
- generate new individuals by crossover and mutation
- repeat for the specified number of generations

Key hooks:

- `crossover(individuals)` creates a child from parent genomes
- `mutation(individual)` randomly perturbs the genome
- `selectParents()` chooses parents for reproduction
- `setPopulationFitness()` evaluates the current population

### Neural network evolution in `NeuralNetworkGenericAlgorithm.py`

This subclass specializes the generic algorithm for neural networks:

- selects parents using tournament-style selection
- performs crossover by gene-level mixing from random parents
- mutates a network by randomly replacing weights/biases with new values
- evaluates each network by letting it play a game and using its hit count as fitness

Fitness metric:

- the algorithm measures `score[1][1]` from `PopGame.Game.runGame()`, which reflects the number of successful paddle hits by the neural network


## Notes

- `NeuralNetworkGenericAlgorithm.py` can take some time to run depending on population size and generation count.
- `pygame` must be installed before running either game script.
- The best evolved model is saved in `Generic Algorithm Result.txt`.
