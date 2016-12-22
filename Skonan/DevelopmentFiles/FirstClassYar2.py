from scipy import signal
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import serial
from time import sleep
from scipy.linalg import hankel

class Radar(object):
    def __init__(self):
        self.samples = 0
        self.radar = 0
        self.time = 0
        self.samplingRate = 0
        self.p = 4

    def setupSerial(self,port, N):
        port = port
        self.samples = N
        n = N
        N = n * 2
        x = [0 for h in range(0, N)]
        radarData = [0 for h in range(0, n)]
        timeData = [0 for h in range(0, n)]
        ser = serial.Serial(port, 9600)
        sleep(2)

        if (input("Do you want to start communication?") == 'y'):

            print("Ok Im Starting Serial COmmunicatiton")
            if (ser.is_open):
                sleep(3)
                for i in range(0, N):
                    ser.write(b"a")
                    x[i] = ser.readline()
                    print(x[i])
            else:
                print("Serial port is not open")
                self.setupSerial(port,N)

        samples = 0;
        samples1 = 0;
        for i in range(0, N):
            if (i % 2 == 0):
                radarData[samples] = float(str(x[i], 'utf-8')) * 5.0 / 1023.0
                samples = samples + 1
            else:
                timeData[samples1] = float(str(x[i], 'utf-8'))
                samples1 = samples1 + 1

        self.radar = np.asarray(radarData)
        self.time = np.asarray(timeData)

        self.samplingRate = 10 ** 6 / np.mean(np.diff(self.time))


        return self.samplingRate, self.radar, self.time


    def getVariables(self):
        return self.samplingRate, self.radar,self.time

    def slidingwindow(self):

        if (len(self.radar) == 2500):
            n = 4*2
            fig, ax = plt.subplots(int(n/2), n)
            overlap = 0.4

            nw = 250
            ns = int(nw * (1.0 - overlap))
            n0 = 0
            n1 = n0 + nw
            N = self.samples

            counter = 0
            while True:
                data = self.radar[n0:n1]
                array = Radar.HanningFunction(data)

                self.corrMtrx = self.getcorrMtrx(x=array,m=14)
                frequency, psd = self.musicAlg()

                r = counter // n
                c = counter % n
                ax[r][c].plot(array)
                ax[r][c+1].plot(frequency,psd)
                n0 += ns
                n1 += ns
                counter += 2
                if n1 > N:
                    break
            plt.show()
        else:
            print("Error your data vector is not the proper length")


    def HanningFunction(radarData):
        return radarData * np.hanning(len(radarData))

    def getcorrMtrx(self,x, m):
        x = np.array(x)
        m = m
        N = len(x)

        xlen = m + 1
        rowVector = x[N - xlen: N]
        columnVector = x[0: N - m]

        hanMatrix = hankel(c=np.array(columnVector).T, r=rowVector)
        X_unscaled = np.fliplr(hanMatrix)

        X = X_unscaled / np.sqrt(N - m)

        Xnew = np.conj(np.fliplr(X))

        corrMatrix = np.vstack((X, Xnew)) / np.sqrt(2)

        return corrMatrix

    def musicAlg(self):
        u, s, v = np.linalg.svd(self.corrMtrx)

        nfft = 512

        frequencyVector = np.linspace(0, 1, nfft // 2)
        frequencyVector *= self.samplingRate / 2

        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=nfft)
            sum += abs(y) ** 2 / s[i]

        sum = 1 / sum

        sum = sum[0:nfft // 2]

        return frequencyVector,sum




if __name__ == '__main__':

    radar = Radar()

    radar.setupSerial(port='COM5',N=2500)
    fs,radardata,timedata = radar.getVariables()
    print(fs, len(radardata), len(timedata))

    print('Process took: ')
    print(timedata[len(timedata) - 1])
    plt.plot(timedata,radardata)
    plt.show()

    radar.slidingwindow()


