from math import exp
import random

random.seed(1)

# fonction sigmoide
def sigmoide(x):
    return 1 / (1 + exp(-1*x))

# fonction dérivée de la sigmoide
def sigmoideDerivative(x):
    return x * (1 - x)

#class link comprenant un poids et deux neurones
class Link:
    def __init__(self, weight):
        self.weight = weight

#class neuron comprenant un identifiant et un poids
class Neuron:
    def __init__(self, id):
        self.id = id
        self.links = [] # liste des liens
        self.output = 0 # sortie du neurone

    # fonction qui calcule la somme pondérée des entrées
    def sum(self, previousLayer):
        sum = 0
        for i in range(len(previousLayer.getNeurons())):
            sum += previousLayer.neurons[i].output * self.links[i].weight
        return sum

    # fonction qui calcule la sortie du neurone
    def output(self, inputs):
        self.output = sigmoide(self.sum(inputs))


#class layer comprenant une liste de neurones
class Layer:
    def __init__(self, nbrNeurons):
        self.neurons = [] # liste des neurones
        for i in range(nbrNeurons):
            self.neurons.append(Neuron(i)) # création d'un neurone

    # getter pour la liste des neurones
    def getNeurons(self):
        return self.neurons


#class network comprenant une liste de layers et une erreur en entrée
class Network:
    def __init__(self, error):
        self.layers = [] # liste des couches
        self.error = error # erreur en entrée pour les résultats

    #fonction d'ajout d'une couche dans le réseau, prend en paramètre un nombre de neurones
    def addLayer(self, nbrNeurons):
        layer = Layer(nbrNeurons) # création d'une couche
        self.layers.append(layer) # ajout de la couche dans la liste des couches

    # fonction qui crée et initialise les liens entre les couches
    def createLinks(self):
        for i in range(len(self.layers)-1):
            for neuron in self.layers[i].neurons:
                for neuron2 in self.layers[i+1].neurons:
                    neuron.links.append(Link((random.random()*2-1)/100))
    def getLayer(self, index):
        return self.layers[index]

    def getLayers(self):
        return self.layers

    def getError(self):
        return self.error

    def getNbrLayers(self):
        return len(self.layers)



if __name__ == '__main__':
    print("test")