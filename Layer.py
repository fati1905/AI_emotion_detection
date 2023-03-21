import Neuron
import random

#class Layer : composée d'une liste de neurones
class Layer:
    def __init__(self,id, nbrNeurons, previousLayer):
        self.id = id
        self.neurons = []
        self.previousLayer = previousLayer

        # Création des neurones
        for i in range(0,nbrNeurons):
            n = Neuron.Neuron(i)
            self.neurons.append(n)
        
        # Initialisation des liens et de leur poids sauf pour la première couche
        if previousLayer != None:
            for neuron in self.neurons:
                for i in range(0, len(self.previousLayer.neurons)):
                    neuron.weights.append((random.random()*4-2)/10) # Poids aléatoire entre -0.01 et 0.01
        else:
            for j in range(0, len(self.neurons)):
                for i in range(0,48*48):
                    self.neurons[j].weights.append(((random.random()*4-2)/10))