from scipy import signal
import scipy.linalg as la
import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import serial
from time import sleep
from scipy.linalg import hankel
from scipy.signal import butter, lfilter, freqz


class Radar(object):
    def __init__(self, samples, radar, time, samplingRate):
        self.samples = samples
        self.radar = radar
        self.time = time
        self.samplingRate = samplingRate
        self.p = 5
        self.nfft = 512
        self.list = []

    def setupSerial(self,P=30):
        N = len(self.radar)
        NP = N - P

        assert 2 * NP > P - 1, 'decrease the second argument'
        if NP > 100:
            NP = 100
        FB = numpy.zeros((2 * NP, P), dtype=complex)
        # FB = numpy.zeros((MAXU, IP), dtype=complex)
        Z = numpy.zeros(512, dtype=complex)
        PSD = numpy.zeros(512)

        # These loops can surely be replaced by a function that create such matrix
        for I in range(0, NP):
            for K in range(0, P):
                FB[I, K] = self.radar[I - K + P - 1]
                FB[I + NP, K] = self.radar[I + K + 1].conjugate()

        print(len(FB[0]))

    def eigen(self, X, P, NSIG=2, method='music', threshold=None, NFFT=4096, criteria='aic', verbose=False):

        N = len(X)
        NP = N - P

        assert 2 * NP > P - 1, 'decrease the second argument'
        if NP > 100:
            NP = 100
        FB = numpy.zeros((2 * NP, P), dtype=complex)
        # FB = numpy.zeros((MAXU, IP), dtype=complex)
        Z = numpy.zeros(NFFT, dtype=complex)
        PSD = numpy.zeros(NFFT)

        # These loops can surely be replaced by a function that create such matrix
        for I in range(0, NP):
            for K in range(0, P):
                FB[I, K] = X[I - K + P - 1]
                FB[I + NP, K] = X[I + K + 1].conjugate()

        # This commented line produces the correct FB, as the 2 for loops above
        # It is more elegant but slower...corrmtx needs to be optimised (20/4/11)
        # FB2 = spectrum.linalg.corrmtx(X, P-1, method='modified')

        # Compute the eigen
        _U, S, V = la.svd(FB)
        # U and V are not the same as in Marple. Real or Imaginary absolute values
        # are correct but signs are not. This is wierd because the svd function
        # gives the same result as cvsd in Marple. Is FB correct ? it seems so.
        # The following operation has to be done. Otherwise, the resulting PSD is
        # not corect
        V = -V.transpose()

        # C   AI or Expert Knowledge to choose "signal" singular values, or input
        # C   NSIG at this point
        for I in range(NSIG, P):
            Z[0:P] = V[0:P, I]
            Z[P:NFFT] = 0

            Z = fft(Z, NFFT)

            if method == 'music':
                PSD = PSD + abs(Z) ** 2.
            elif method == 'ev':
                PSD = PSD + abs(Z) ** 2. / S[I]

        PSD = 1. / PSD

        # for some reasons, we need to rearrange the output. this is related to
        # the way U and V are order in the routine svd
        nby2 = NFFT / 2
        newpsd = numpy.append(PSD[nby2:0:-1], PSD[nby2 * 2 - 1:nby2 - 1:-1])

        return newpsd, S


class RadarData(object):
    def __init__(self, array, power, vals):
        self.data = array
        self.psd = power
        self.eigenvals = vals

    def getData(self):
        return self.data

    def getEigenVals(self):
        return self.eigenvals




if __name__ == '__main__':
    N = 2500
    sRate = 10

    n = np.linspace(0, N / sRate, N)
    x = 0.1 * np.sin(1.2 * np.pi * (n)) + 0.2 * np.sin(0.6 * np.pi * (n))
    mean = np.mean(x)
    std = np.std(x)

    noise = np.random.normal(mean, std, len(x))
    x1 = x + noise

    radar = Radar(radar=x1, samples=N, samplingRate=sRate, time=n)

    psd,S = radar.eigen(X = x1,P=100)

    plt.plot(psd)
    plt.show()


