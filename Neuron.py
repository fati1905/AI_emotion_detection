import fonction as f
class Neuron:
    def __init__(self, id):
        self.id = id
        self.output = 0
        self.weights = [] #liste des poids
        self.previousOutput = [] #liste des valeurs des neurones précédents
        self.nextError = []
        self.error = 0

    #somme pondérée des entrées
    def sum(self):
        sum = 0
        for i in range(0,len(self.previousOutput)):
            sum += self.previousOutput[i] * self.weights[i]
        return sum

    #fonction d'activation
    def activation(self):
        return f.sigmoid(self.sum())

    #somme pondérée des erreurs
    def sumError(self):
        sum = 0
        for i in range(0, len(self.nextError)):
            sum += self.nextError[i] * self.weights[i]
        return sum

    #dérivée de la fonction d'activation
    def activationDerivative(self):
        return f.sigmoidDerivative(self.output) * self.sumError()


