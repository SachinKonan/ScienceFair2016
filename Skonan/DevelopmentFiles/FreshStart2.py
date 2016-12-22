import cmath
from scipy.fftpack import fft
from scipy.linalg import hankel
import numpy as np
import numpy
import matplotlib.pyplot as plt

import scipy.sparse


class Unknown(object):

    def corrMtrx(x,m):
        x = np.array(x)
        m = m
        N = len(x)

        xlen = m + 1
        rowVector = x[N - xlen: N]
        columnVector = x[0: N - m]

        hanMatrix = hankel(c=np.array(columnVector).T, r=rowVector)
        X_unscaled = np.fliplr(hanMatrix)

        X = X_unscaled/ np.sqrt(N - m)

        Xnew = np.conj(np.fliplr(X))

        corrMatrix = np.vstack((X,Xnew))/np.sqrt(2)

        return corrMatrix

    def getSignalSpace(p):
        return p

    def example(D):
        """Eigenvalues and -vectors, based on SVD."""
        u, s, v = np.linalg.svd(D, full_matrices=False);
        return np.diag(s) ** 2, u

if __name__ == '__main__':

    N = 250
    sRate = 5

    f2 = 0.257
    n = np.linspace(0, N/sRate, N)
    x = np.sin(np.pi * f2*(n))

    mean = np.mean(x)
    std = np.std(x)

    noise = np.random.normal(mean, std,len(x))*0.1

    x += noise

    plt.plot(x)
    plt.show()


    p = 4
    hannmatrix = Unknown.corrMtrx(x,7)

    u, s, v = np.linalg.svd(hannmatrix)

    f = 0.257
    nfft = 512

    frequencyVector = np.linspace(0, 1, nfft//2)
    frequencyVector *= sRate/2

    sum = 0
    for i in range(p, len(v)):
        y = fft(v[i],n = nfft)
        sum += abs(y)**2/s[i]

    sum = 1/sum

    sum = sum[0:nfft//2]

    plt.plot(frequencyVector,sum)
    plt.show()