from scipy import signal
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import serial
from time import sleep
from scipy.linalg import hankel


class Radar:

    def setupSerial(port, N):
        port = port
        n = N - 1
        N = n * 2
        x = [0 for h in range(0, N)]
        radarData = [0 for h in range(0, n)]
        timeData = [0 for h in range(0, n)]
        ser = serial.Serial(port, 9600)
        sleep(2)

        if (input("Do you want to start communication?") == 'y'):
            print("Ok Im Starting Serial COmmunicatiton")
            if (ser.is_open):
                for i in range(0, N):
                    ser.write(b"a")
                    x[i] = ser.readline()
            else:
                print("Serial port is not open")
                return

        samples = 0;
        samples1 = 0;
        for i in range(0, N):
            if (i % 2 == 0):
                radarData[samples] = float(str(x[i], 'utf-8')) * 5.0 / 1023.0
                samples = samples + 1
            else:
                timeData[samples1] = float(str(x[i], 'utf-8'))
                samples1 = samples1 + 1

        radar = np.asarray(radarData)
        time = np.asarray(timeData)

        samplingRate = 10 ** 6 / np.mean(np.diff(time))
        return samplingRate, radarData,timeData

    def slidingwindow(radarData,samples):

        if(len(radarData) == 2500):
            n = 4*2
            fig, ax = plt.subplots(int(n/2),n)
            overlap = 0.4

            nw = 250
            ns = int(nw * (1.0 - overlap))
            n0 = 0
            n1 = n0+ nw
            N = samples

            counter = 0
            while True:
                data = radarData[n0:n1]
                array = Radar.HanningFunction(data)
                r = counter//n
                c = counter % n
                ax[r][c].plot(array)
                psd,f = Radar.spectrum(array,nw,64)
                ax[r][c+1].plot(f,psd)
                n0 += ns
                n1 += ns
                counter += 2
                if n1 > N:
                    break
            plt.show()
        else: print("Error your data vector is not the proper length")

    def HanningFunction(radarData):
        return radarData * np.hanning(len(radarData))

    def corrMtrx(x, m):
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

    def spectrum(radarData,N,Fs):
        yf = fft(radarData)  # db
        xf = np.linspace(0.0, Fs/2, N / 2)
        yf = yf[0:N/2]
        return abs(yf),xf



if __name__ == '__main__':
    N = 2500
    sRate = 64  # sampling rate


    z = np.linspace(0, N * 1/sRate,N)
    x = 1*np.sin(1* np.pi * z) + 2*np.sin(4 * np.pi * z)
    #plt.plot(z,x)
    #plt.show()

    #Radar.setupSerial('COM5',N)
    Radar.slidingwindow(x,N)