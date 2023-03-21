from math import exp
import random
import file_reader as fr

random.seed(1)

# fonction sigmoide
def sigmoide(x):
    return 1 / (1 + exp(-1*x))

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
        for i in range(0, len(previousLayer.neurons)):
            print("i "+str(i))
            sum += previousLayer.neurons[i].output
        return sum

    # fonction qui calcule la sortie du neurone
    def newOutput(self, inputs):
        self.output = sigmoide(self.sum(inputs))


#class layer comprenant une liste de neurones
class Layer:
    def __init__(self, nbrNeurons):
        self.neurons = [] # liste des neurones
        for i in range(nbrNeurons):
            n = Neuron(i)
            self.neurons.append(n) # création d'un neurone

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
                    neuron2.links.append(Link((random.random()*2-1)/100))
    def getLayer(self, index):
        return self.layers[index]

    def getLayers(self):
        return self.layers

    def getError(self):
        return self.error

    def getNbrLayers(self):
        return len(self.layers)

    #fonction qui insère les données dans le réseau de neurones pour chaque neurone de la première couche
    def insertPixel(self, picture):
        for neuron in self.layers[0].neurons:
            for i in range(0, len(picture.pixel)):
                neuron.output += picture.pixel[i] * ((random.random()*2-1)/100)

    #Fonction qui propage les données dans le réseau de neurones
    def propagate(self):
        for i in range(1, len(self.layers)):
            for neuron in self.layers[i].neurons:
                neuron.output = neuron.newOutput(self.layers[i-1])


if __name__ == '__main__':
    # Nous allons lire tous les fichiers dans les dossiers Données qui contient les dossiers de chaque emotions
    fr.read_all_files("Données")
    print("Fin de lecture des fichiers")

    #création du réseau de neurones
    Network = Network(0.2)
    Network.addLayer(500)
    Network.addLayer(300)
    Network.addLayer(100)
    Network.addLayer(50)
    Network.addLayer(4)

    #récupération du premier layer
    layer = Network.getLayer(0)


    Network.insertPixel(fr.angry_picture[0])

    #affichage du premier layer
    #for neuron in Network.getLayer(0).neurons:
        #print(neuron.output)

    # Network.propagate()
    #affichage de tous les neurones du réseau
    for layer in Network.layers:
        print("\n\n")
        for neuron in layer.neurons:
            print(str(neuron.id)+" "+str(len(neuron.links))+" "+str(neuron.output))


    #affichage du dernier layer
    # print("\n\nlast layer")
    # for neuron in Network.getLayer(4).neurons:
        # print("Last Output"+neuron.output)




    Network.createLinks()
