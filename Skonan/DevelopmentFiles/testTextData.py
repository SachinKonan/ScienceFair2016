from scipy import signal
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import serial
from time import sleep
from scipy.linalg import hankel
from scipy.signal import butter, lfilter, freqz
from scipy.fftpack import hilbert
import scipy
from scipy import stats

class Radar(object):
    def __init__(self, samples, radar, samplingRate):
        self.samples = samples
        self.radar = radar
        self.samplingRate = samplingRate
        self.p = 5
        self.nfft = 512
        self.list = []

    def setupSerial(self, port, N):

        port = port
        self.samples = N
        n = N
        N = n * 2
        x = [0 for h in range(0, N)]
        radarData = [0 for h in range(0, n)]
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
                self.setupSerial(port, N)

        samples = 0;
        samples1 = 0;
        for i in range(0, N):
            if (i % 2 == 0):
                radarData[samples] = float(str(x[i], 'utf-8')) * 5.0 / 1023.0
                samples = samples + 1
            else:
                samples1 = samples1 + 1

        self.radar = np.asarray(radarData)

        self.samplingRate = 10 ** 6 / np.mean(np.diff(self.time))

        return self.samplingRate, self.radar, self.time

    def getVariables(self):
        return self.samplingRate, self.radar, self.time

    def slidingwindow(self):

        if (len(self.radar) > 0):

            n = 4 * 2
            fig, ax = plt.subplots(int(n / 2), n)
            overlap = 0.4

            nw = 450
            ns = int(nw * (1.0 - overlap))
            n0 = 0
            n1 = n0 + nw
            N = self.samples

            counter = 0
            counter1 = 1

            list1 = []
            while True:
                data = self.radar[n0:n1]
                array = Radar.HanningFunction(data)

                self.corrMtrx = self.getcorrMtrx(x=array, m=4)
                frequency, psd, eigenvals = self.musicAlg()

                # xf, yf = self.fft(array)


                r = counter // n
                c = counter % n
                # ax[r][c].plot(array)

                radarObject = RadarData(array, psd, eigenvals)
                self.list.append(radarObject)

                list1.append(eigenvals)

                ax[r][c].plot(eigenvals)
                ax[r][c + 1].plot(frequency, np.log(abs(psd)))

                # ax[r][c + 1].plot(xf, yf)

                """if(counter1 == 1):
                    sum1 = sum(eigenvals)
                    print('Explained Variance for Eigenvalues')

                    for i in range(0, len(eigenvals)):
                        print('The %d eigenvalue has a weight of %d'%(i, (eigenvals[i]/sum1) * 100))
                """

                # diff = Radar.diffCalc(self,list(eigenvals))

                # ax[r][c + 2].plot(diff)


                # if counter1 == 1:
                # break

                n0 += ns
                n1 += ns
                counter += 2
                counter1 += 1

                if n1 > N:
                    break
            plt.show()

            """
            from sklearn.preprocessing import StandardScaler
            X_std = StandardScaler().fit_transform(list1)

            cor_mat1 = np.corrcoef(X_std.T)

            eig_vals, eig_vecs = np.linalg.eig(cor_mat1)

            print(eig_vals)"""




        else:
            print("Error your data vector is not the proper length")

    def diffCalc(self, list1):
        list2 = []
        for i in range(1, len(list1)):
            list2.append(list1[i] - list1[i - 1])
        return list2

    def fft(self, array):
        yf = fft(array, n=self.nfft)
        xf = np.linspace(0.0, self.samplingRate / 2, self.nfft / 2)
        return xf, abs(yf[0:self.nfft / 2])

    def HanningFunction(radarData):
        return radarData * np.hanning(len(radarData))

    def getcorrMtrx(self, x, m):
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

        print(len(corrMatrix))
        return corrMatrix

    def musicAlg(self):
        u, s, v = np.linalg.svd(self.corrMtrx)

        self.nfft = 512

        frequencyVector = np.linspace(0, 1, self.nfft // 2)
        frequencyVector *= self.samplingRate / 2

        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=self.nfft)
            sum += abs(y) ** 2 / s[i]

        if(sum ==0): sum = 0.0000001

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector, sum, s



    def testSpectrum(self, data):
        corrMtrx = self.getcorrMtrx(data, 30)
        return self.musicAlg2(corrMtrx)

    def musicAlg2(self, corrMtrx):
        u, s, v = np.linalg.svd(corrMtrx)

        self.nfft = 512

        frequencyVector = np.linspace(0, 1, self.nfft // 2)
        frequencyVector *= self.samplingRate / 2

        sum = 0
        for i in range(self.p, len(v)):
            y = fft(v[i], n=self.nfft)
            sum += abs(y) ** 2 / s[i]

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector, sum, s

    def parabolic_polyfit(f, x, n):
        """Use the built-in polyfit() function to find the peak of a parabola

        f is a vector and x is an index for that vector.

        n is the number of samples of the curve used to fit the parabola.
        """
        a, b, c = np.polyfit(np.arange(x - n // 2, x + n // 2 + 1), f[x - n // 2:x + n // 2 + 1], 2)
        xv = -0.5 * b / a
        yv = a * xv ** 2 + b * xv + c
        return (xv, yv)

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
    file1 = open('Pics/testRadar4ft.out','r')
    file2 = open('Pics/controlradar.out','r')
    file3 = open('Pics/testTime4ft.out','r')
    file4 = open('Pics/controltime.out','r')

    radarData1 = []
    radarData2 = []
    timeData1 = []
    timeData2 = []

    numfiles = 4
    count = 0

    for i in range(0, numfiles):

        if(i ==0): a = file1
        elif(i == 1): a = file2
        elif(i == 2): a = file3
        elif(i ==3): a = file4

        count = 0
        for line in a.readlines():


            if (i == 0): radarData1.append(float(line))
            elif (i == 1): radarData2.append(float(line))
            elif (i == 2): timeData1.append(float(line))
            elif (i == 3): timeData2.append(float(line))

            count+=1

    samplingRate = (10 ** 6 / np.mean(np.diff(timeData1)) + 10 ** 6 / np.mean(np.diff(timeData2)))/2



    plt.plot(timeData1, radarData1)
    plt.xlabel('Time(microseconds)')
    plt.ylabel('Voltage(V)')
    plt.title('Control Group')
    plt.show()

    N = len(radarData1)
    xf = np.linspace(0.0, float(samplingRate)/2, N / 2)

    yf = fft(radarData1)

    plt.semilogy(xf[1:N / 2], np.abs(yf[1:N / 2]), '-b')
    plt.xlabel('Frequency(Hz)')
    plt.ylabel('Power(dB)')
    plt.grid()
    plt.show()


    filtered = scipy.signal.decimate(radarData1, 6)

    radar = Radar(radar=filtered, samples=N, samplingRate=10.83)

    radar.slidingwindow()

    """

    radar = Radar(radar=radarData1, samples=N, samplingRate=samplingRate, time=timeData1)

    newdata = []
    firstfillter = radar.graphFilterResults()

    plt.plot(firstfillter)

    plt.show()

    x1h = hilbert(firstfillter)


"""








