import Fonction as fct

class Neuron:

    def __init__(self, id) -> None:
        self.id = id # L'identifiant du neurone
        self.output = 0 # La sortie du neurone
        self.weights = []   # Les poids des entrés du neurone
        self.previousOutput = [] # La sortie des neurones de la couche précédente
        self.nextError = [] # L'erreur de la couche suivante
        self.error = 0 # L'erreur
    
    # *************************** Pour la propagation ********************
    # La somme des produits de l'entrées
    def sumOfProducts(self):
        sum = 0
        for i in range(0, len(self.previousOutput)):
            sum += self.previousOutput[i] * self.weights[i]
        return sum
    
    # Appliquer sigmoide à la somme des produits des entrées et leurs poids
    def newOutput(self):
        self.output = fct.sigmoid(self.sumOfProducts())
        return self.output
    
    # ************************* Pour la rétropropagation **********************

    def sumOfProductsOfErrors(self):
        sum = 0
        for i in range(0, len(self.nextError)):
            sum += self.nextError[i] * self.weights[i]
        return sum

    # Appliquer la dérivée de la fonction de sigmoid
    def newError(self):
        self.error = fct.sigmoidDerivative(self.output)*self.sumOfProductsOfErrors()
        return self.error    