from math import exp

#fonction sigmoid
def sigmoid(x):
    return 1 / (1 + exp(-1*x*4))

#fonction sigmoid derivée
def sigmoidDerivative(x):
    return x * (1 - x)*4
