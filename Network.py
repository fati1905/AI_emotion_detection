import Layer
import Neuron


#class Network : composée d'une liste de layers et d'une erreur en entrée
class Network:

    #constructeur
    def __init__(self, error):
        self.layers = []
        self.error = error
        self.picture = None
        self.category = -1 

    #Méthode qui ajoute une image dans le réseau
    def setPicture(self, picture):
        self.picture = picture

        if self.picture.category == "Angry":
            self.category = 0
        if self.picture.category == "Happy":
            self.category = 1
        if self.picture.category == "Fearful":
            self.category = 2
        if self.picture.category == "Disgusted":
            self.category = 3
        

    #fonction qui ajoute les pixels de l'image dans le réseau
    def setPixels(self):
        for i in range(0, len(self.layers[0].neurons)):
            for p in self.picture.pixel:
                self.layers[0].neurons[i].previousOutput.append(p) 

    #fonction d'ajout d'une couche dans le réseau, prend en paramètre un nombre de neurones
    def addFirstLayer(self,id, nbrNeurons):
        
        if len(self.layers) == 0:
            layer = Layer.Layer(id,nbrNeurons, None)
            self.layers.append(layer)
            # Ajouter les pixels dans le réseaux
            self.setPixels() #  Première image (TEST!!! À changer après)$

    #fonction qui ajoute une couche non première
    def addLayer(self,id, nbrNeurons):
        layer = Layer.Layer(id,nbrNeurons, self.layers[len(self.layers)-1])
        self.layers.append(layer)
                    

    #Méthode qui propage les données dans le réseau
    def propage(self):
        
        # Calcul des sorties dans la première couche
        for n in self.layers[0].neurons: # Pour chaque neurones de la première couche, on appliquer la fonction sigmoide
            n.output = n.newOutput()
        
        print("Fini avec la première couche")
        # Propagation et calcul des sorties des prochaines couches
        for i in range(1, len(self.layers)):
            for n in self.layers[i].neurons:
                for n2 in self.layers[i-1].neurons:
                    n.previousOutput.append(n2.output)
                n.output = n.newOutput()
        print("Fini avec la propagation")

    #Méthode qui dit s'il y a eu une erreur
    def hasError(self):  

        for n in range(0, len(self.layers[-1].neurons)): # Pour chaque neurones de la dernière couche

            if n == self.category: # Si c'est la bonne catégorie
                if (1 - self.layers[-1].neurons[n].output) > self.error:
                    return True
            else :
                if (self.layers[-1].neurons[n].output) > self.error:
                    return True
        
        return False
    
    #calcul de l'erreur
    def errorCalculus(self):
        for n in range(0, len(self.layers[-1].neurons)):
            if n == self.category:
                self.layers[-1].neurons[n].error = 1 - self.layers[-1].neurons[n].output
            else:
                self.layers[-1].neurons[n].error = -self.layers[-1].neurons[n].output
        
        for i in range(len(self.layers)-2, -1, -1):
            for n in self.layers[i].neurons:
                for n2 in self.layers[i+1].neurons:
                    n.nextError.append(n2.error)
                n.error = n.newError()
