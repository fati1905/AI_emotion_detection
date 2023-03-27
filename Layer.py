import Neuron
import random

class Layer:
    def __init__(self, nbNeurons, previousLayer):
        self.neurons = [] # liste des neurones de la couche
        self.previousLayer = previousLayer # couche précédente
        for i in range(0, nbNeurons): # on ajoute les neurones
            self.neurons.append(Neuron.Neuron(i))

        #initialisation des liens entre les neurones
        if previousLayer != None:
            for neuron in self.neurons:
                for previousNeuron in previousLayer.neurons:
                    neuron.weights.append((random.random()*10-5)/10)
        else:
            for neuron in self.neurons: # si c'est la première couche, on initialise les poids à 1
                neuron.weights.append(1) # on initialise les poids à 1