from math import exp
#calcul sigmoid
def sigmoid(x):
    return 1/(1+exp(-x*3))

#calcul sigmoid dérivée
def sigmoidDerivative(x):
    return x*(1-x)*3