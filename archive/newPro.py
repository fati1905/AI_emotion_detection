from math import exp
import random
import file_reader as fr

random.seed(1)


# fonction sigmoide
def sigmoide(x):
    return 1 / (1 + exp(-1 * x))


# Class link comprenant un neurone de la couche précédente et son poids/résultat
class Link:
    def __init__(self, entry, weight):
        self.weight = weight
        self.entry = entry # Entry représente les entrées de l'image


# La classe neurone contient un identifiant, les liens avec les anciens neurones ou les pixels de l'image et puis
# une sortie qui est la valeur de sortie du neurone
class Neurone:
    def __init__(self, id):
        self.id = id
        self.links = []
        self.output = 0

    # Calculer la somme des produits des entrées avec leurs poids
    def sumOfProducts(self):
        sum = 0
        for link in self.links:
            sum += link.weight * link.entry
        return sum

    # fonction qui calcule la sortie du neurone
    def newOutput(self):
        self.output = sigmoide(self.sumOfProducts())


# class layer comprenant une liste de neurones
class Layer:
    def __init__(self, nbrNeurons):
        self.neurones = []  # liste des neurones

        # création des neurones
        for i in range(nbrNeurons):
            n = Neurone(i)
            self.neurones.append(n)

    # getter pour la liste des neurones
    def getNeurons(self):
        return self.neurones


# class network comprenant une liste de layers et une erreur en entrée
class Network:
    def __init__(self, error):
        self.layers = []  # liste des couches
        self.error = error  # erreur en entrée pour les résultats

    # fonction d'ajout d'une couche dans le réseau, prend en paramètre un nombre de neurones
    def addLayer(self, nbrNeurons):
        self.layers.append(Layer(nbrNeurons))  # ajout de la couche dans la liste des couches

    # Ajout des pixels de l'image dans la première couche
    def upload_image(self, picture):
        for n in self.layers[0].neurones:
            for i in range(0, len(picture.pixel)):
                n.links.append(Link(picture.pixel[i], (random.random()*2-1)/100))

    # Méthode qui propage les données dans le réseau de neurones
    def propagate1(self):
        # Calculer les outputs de la première couche
        for n in self.layers[0].neurones:
            for l in n.links:
                n.output = n.newOutput()

        # Créer les liens avec la prochaine couche
        # Puis la couche calcule ses outputs
        for i in range(1, len(self.layers)):
            # Pour chaque neurone de la couche actuelle
            for n in self.layers[i].neurones:
                # Pour chaque neurone de la couche ancienne
                for n2 in self.layers[i-1].neurones:
                    # nous allons créer un lien qui prend comme entrée les sorties des neurones de l'ancienne couche
                    n.links.append(Link(n2.output, (random.random()*2-1)/100))

                # On calcule la sortie du neurone actuelle
                #n.output = n.newOutput()


if __name__ == '__main__':
    # Nous allons lire tous les fichiers dans les dossiers Données qui contient les dossiers de chaque emotions
    fr.read_all_files("Données")
    print("Fin de lecture des fichiers")

    # Création du réseau de neurones
    Network = Network(0.2)

    # Ajout des couches dans le réseau
    Network.addLayer(500)
    Network.addLayer(300)
    Network.addLayer(100)
    Network.addLayer(50)
    Network.addLayer(4)

    # Test pour savoir le nombre de neurones dans chaque couche
    # i = 0
    # for layer in Network.layers:
    #     print("Nombre de neurones dans la couche "+str(i)+" est : "+str(len(layer.neurones)))
    #     i = i+1

    # Ajouter l'image dans le réseau
    Network.upload_image(fr.angry_picture[0])

    # Nombre de liens pour chaque neurone
    # for neurone in Network.layers[0].neurones:
    #     print("Nombre de lien :"+str(len(neurone.links)))

    # Propager la sortie
    Network.propagate1()

    count = 0
    for layer in Network.layers:
        print("******************************* Layer "+str(count))
        count += 1
        for link in layer.neurones[0].links:
            print(str(link.entry)+" --> "+str(link.weight))

    # Affiche les sorties de la dernière couche
    # for n in Network.layers[4]:
    #     print("The output is : "+str(n.output))