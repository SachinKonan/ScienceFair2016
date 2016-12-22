import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

class Neural(object):

    def __init__(self):
        self.inputLayer = 2
        self.outputLayer = 1
        self.hiddenLayer = 3

        self.W1 = np.random.rand(self.inputLayer,self.hiddenLayer)

        self.W2 = np.random.rand(self.hiddenLayer, self.outputLayer)


    def forward(self, X):
        self.z2 = np.dot(X, self.W1)
        self.a2 = Neural.sigmoid(self.z2)
        self.z3 = np.dot(self.z2, self.W2)
        self.yHat = Neural.sigmoid(self.z3)

        return self.yHat

    def getVars(self):
        return self.yHat

    def sigmoid(z):
        return 1/(1 + np.exp(-z))

    def sigmoidPrime(x):
        return np.exp(-1*x)/(1+np.exp(-1*x))**2

    def costFunctionPrime(self,x,y):

        self.yHat = self.forward(X)

        delta3 = np.multiply(-(y - self.yHat), Neural.sigmoidPrime(self.z3))
        dJdW2 = np.dot(self.a2.T, delta3)

        delta2 = np.dot(delta3, self.W2.T) * Neural.sigmoidPrime(self.z2)
        dJdW1 = np.dot(X.T, delta2)

        return dJdW1, dJdW2

    def costFunction(self,x,y):
        self.yHat = self.forward(x)
        j = 0.5* sum((y - self.yHat)**2)
        return j

    def f(x):
        return x**2

    def getParams(self):
        # Get W1 and W2 unrolled into vector:
        params = np.concatenate((self.W1.ravel(), self.W2.ravel()))
        return params

    def setParams(self, params):
        # Set W1 and W2 using single paramater vector.
        W1_start = 0
        W1_end = self.hiddenLayerSize * self.inputLayerSize
        self.W1 = np.reshape(params[W1_start:W1_end], (self.inputLayerSize, self.hiddenLayerSize))
        W2_end = W1_end + self.hiddenLayerSize * self.outputLayerSize
        self.W2 = np.reshape(params[W1_end:W2_end], (self.hiddenLayerSize, self.outputLayerSize))

    def computeGradients(self, X, y):
        dJdW1, dJdW2 = self.costFunctionPrime(X, y)
        return np.concatenate((dJdW1.ravel(), dJdW2.ravel()))

    def computeNumericalGradient(self, N, X, y):
        paramsInitial = N.getParams()
        numgrad = np.zeros(paramsInitial.shape)
        perturb = np.zeros(paramsInitial.shape)
        e = 1e-4

        for p in range(len(paramsInitial)):
            # Set perturbation vector
            perturb[p] = e
            N.setParams(paramsInitial + perturb)
            loss2 = N.costFunction(X, y)

            N.setParams(paramsInitial - perturb)
            loss1 = N.costFunction(X, y)

            # Compute Numerical Gradient
            numgrad[p] = (loss2 - loss1) / (2 * e)

            # Return the value we changed to zero:
            perturb[p] = 0

        # Return Params to original value:
        N.setParams(paramsInitial)

        return numgrad

class trainer(object):
    def __init__(self,N):
        self.N = N

    def costFunctionWrapper(self,params, X,y):
        self.N.setParams(params)
        cost = self.N.costFunction(X,y)
        grad = self.N.computeGradients(X,y)
        return cost, grad


    def train(self, X,y):
        params0 = self.N.getParams()

        _res = optimize.minimize()


if __name__ == '__main__':

    X = np.array(([3, 5], [5, 1], [10, 2]), dtype=float)
    y = np.array(([75], [82], [93]), dtype=float)

    X = X / np.amax(X, axis=0)

    y = y / 100

    NN = Neural()
    num = NN.computeNumericalGradient(NN ,X ,y )
    print(num)