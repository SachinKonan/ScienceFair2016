from scipy import signal
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import cmath
import scipy
from scipy.linalg import toeplitz
import time

N = 100
sRate = 25 # sampling rate

z = np.linspace(0,2*np.pi, num=N)
x = np.sin(2*np.pi * z) + np.sin(1 * np.pi * z) # sample signal

noise = np.random.normal(np.mean(x), np.std(x)) * 0.01

conj = np.conj(x);

l = len(conj)


p = 2
flipped  = [0 for h in range(0, l)]

flipped = conj[::-1]


acf = signal.convolve(x,flipped,'full')


a1 = np.asarray(toeplitz(c=np.asarray(acf),r=np.asarray(acf)))#autocorrelation matrix that will be decomposed into eigenvectors


eigenValues,eigenVectors = LA.svd(a1)


idx = eigenValues.argsort()[::-1]
eigenValues = eigenValues[idx]
eigenVectors = eigenVectors[:,idx]


idx = eigenValues.argsort()[::-1]

eigenValues = eigenValues[idx]# soriting the eigenvectors and eigenvalues from greatest to least eigenvalue
eigenVectors = eigenVectors[:,idx]


signal_eigen = np.array(eigenVectors[0:p])
noise_eigen = np.array(eigenVectors[p:len(eigenVectors)]) # noise subspace
noise_eigenVal = eigenValues[p:len(eigenValues)]




num_sum = np.zeros( len(noise_eigen))
sum1 = 0
for n in range(0, len(noise_eigen)):

    h,w = signal.freqz(noise_eigen[n],1,worN= 256,whole = [0,int(sRate/2)])

    wm = np.absolute(w)

    sum1 = sum1 + wm **2/noise_eigenVal[n]

plt.plot(h, sum1)
plt.show()
