import Layer
import random
import csv


class Network:
    def __init__(self, error):
        self.error = error # erreur du réseau
        self.layers = [] # liste des couches du réseau

        self.idPicture = -1 # id de l'image courante
        self.name = "" # nom de l'image courante
        self.category = "" # catégorie de l'image courante
        self.pictures = [] # images du réseau
        self.numCategory = -1 # numéro de la catégorie de l'image courante
        self.erroredPicture = [] # images qui ont eu une erreur

    def addLayer(self, nbNeurons):
        print("Ajout d'une couche de " + str(nbNeurons) + " neurones")
        if len(self.layers) == 0: # si c'est la première couche
            self.layers.append(Layer.Layer(nbNeurons, None))
        else:
            self.layers.append(Layer.Layer(nbNeurons, self.layers[len(self.layers) - 1] )) # sinon on ajoute la couche avec la couche précédente en paramètre

    def setPictures(self, csvfile):
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[2] == "happy" or row[2] == "sad":
                self.pictures.append(row)

        random.shuffle(self.pictures)
        random.shuffle(self.pictures)
        for row in self.pictures:
            print("name :"+str(row[1])+" type:"+row[2])

    def chosePicture(self, index):
        self.idPicture = int(self.pictures[index][0])
        self.name = self.pictures[index][1]
        self.category = self.pictures[index][2]
        # switch sur la catégorie
        if self.category == "angry":
            self.numCategory = 0
        elif self.category == "disgusted":
            self.numCategory = 1
        elif self.category == "fearful":
            self.numCategory = 2
        elif self.category == "happy":
            self.numCategory = 3
        elif self.category == "neutral":
            self.numCategory = 4
        elif self.category == "sad":
            self.numCategory = 5
        elif self.category == "surprised":
            self.numCategory = 6

        for n in range(0, len(self.layers[0].neurons)):
            self.layers[0].neurons[n].output = float(self.pictures[index][3+n])

    #propagation avant
    def propagation(self):
        for l in range (1, len(self.layers)): # on commence à 1 car la première couche n'a pas de couche précédente
            for neuron in self.layers[l].neurons: # on parcourt les neurones de la couche
                for neuron2 in self.layers[l-1].neurons: # on parcourt les neurones de la couche précédente
                    neuron.previousOutput.append(neuron2.output) # on ajoute la sortie du neurone précédent à la liste des sorties précédentes
                neuron.output = neuron.activation() # on calcule la sortie du neurone


    def putError(self, index):
        for n in range (0, len(self.layers[-1].neurons)): # on parcourt les neurones de la couche de sortie
            if n == self.numCategory: # si c'est le neurone de la bonne catégorie
                if 1 - self.layers[-1].neurons[n].output > self.error:
                    self.erroredPicture.append(index)
                    return True
            else:
                if self.layers[-1].neurons[n].output > self.error:
                    self.erroredPicture.append(index)
                    return True
        return False

    # méthode qui dit s'il y a eu une erreur ou non
    def hasError(self): # on regarde si la sortie de la couche de sortie est correcte
        for n in range(0, len(self.layers[-1].neurons)): # on parcourt les neurones de la couche de sortie
            if n == self.numCategory: # si c'est le neurone de la bonne catégorie
                if (1 - self.layers[-1].neurons[n].output) > self.error: # si la sortie est trop éloignée de 1
                    return True
            else:
                if self.layers[-1].neurons[n].output > self.error:  # si la sortie est trop éloignée de 0
                    return True
        return False

    #retropropagation
    def retropropagation(self): # on calcule l'erreur de chaque neurone

        id = random.randint(0, len(self.erroredPicture)-1) # on prend une image au hasard parmi les images qui ont eu une erreur
        id = self.erroredPicture[id] # on prend une image au hasard parmi les images qui ont eu une erreur
        self.chosePicture(id)
        self.propagation()

        for n in range(0, len(self.layers[-1].neurons)): # on parcourt les neurones de la couche de sortie
            if n == self.numCategory: # si c'est le neurone de la bonne catégorie
                self.layers[-1].neurons[n].error = 1 - self.layers[-1].neurons[n].output
            else:
                self.layers[-1].neurons[n].error = 0 - self.layers[-1].neurons[n].output

        for l in range (len(self.layers)-2, 0, -1): # on parcourt les couches de l'avant dernière à la deuxième
            for n in self.layers[l].neurons:
                for n2 in self.layers[l+1].neurons:
                    n.nextError.append(n2.error)
                n.error = n.activationDerivative()

        self.updateWeights(0.08)
        self.clearLists()
        self.propagation()

    # on met à jour les poids avec la méthode stochastique
    def updateWeights(self, learningRate):
        for l in range (1, len(self.layers)):
            for n in self.layers[l].neurons:
                for w in range(0, len(n.weights)):
                    n.weights[w] = n.weights[w] + learningRate * n.error * n.previousOutput[w]

    # on vide les listes des sorties précédentes et des erreurs suivantes
    def clearLists(self):
        for l in range(0, len(self.layers)):
            for n in self.layers[l].neurons:
                n.previousOutput.clear()
                n.nextError.clear()
