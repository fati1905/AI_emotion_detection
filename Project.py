from math import exp
import random

random.seed(1)

# fonction sigmoide
def sigmoide(x):
    return 1 / (1 + exp(-1*x))


#class neuron comprenant un identifiant et un poids
class Neuron:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight

#class layer comprenant une liste de neurones
class Layer:
    def __init__(self, nbrNeurons):
        self.neurons = [] # liste des neurones
        for i in range(nbrNeurons):
            self.neurons.append(Neuron(i, random.random()*2-1)) # création d'un neurone


#class network comprenant une liste de layers et une erreur en entrée
class Network:
    def __init__(self, error):
        self.layers = [] # liste des couches
        self.error = error # erreur en entrée pour les résultats
        self.links = [] # liste des liens entre les couches
        self.values = [] # liste des valeurs des neurones

    #fonction d'ajout d'une couche dans le réseau, prend en paramètre un nombre de neurones
    def addLayer(self, nbrNeurons):
        layer = Layer(nbrNeurons) # création d'une couche

    def addLayer(self, layer):
        self.layers.append(layer)

    def getLayer(self, index):
        return self.layers[index]

    def getLayers(self):
        return self.layers

    def getError(self):
        return self.error

    def getLink(self, index):
        return self.links[index]

    def getLinks(self):
        return self.links

    def getValue(self, index):
        return self.values[index]

    def getValues(self):
        return self.values

    def getNbrLayers(self):
        return len(self.layers)

    def getNbrLinks(self):
        return len(self.links)

    def getNbrValues(self):
        return len(self.values)

    def getLastLayer(self):
        return self.layers[-1]







