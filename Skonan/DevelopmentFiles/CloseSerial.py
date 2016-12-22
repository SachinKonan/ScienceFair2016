import numpy as np
import scipy.linalg as la
import scipy.signal as signal
N = 100 # num of samples
sRate = 25 # sampling rate

z = np.linspace(0,2*np.pi, num=N)
x = np.sin(2*np.pi * z) + np.sin(1 * np.pi * z)

autocorrMtx = la.toeplitz(signal.correlate(x,x,mode='full'))

print(len(autocorrMtx[0]))