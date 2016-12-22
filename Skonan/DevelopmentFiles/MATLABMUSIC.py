from scipy import signal
import scipy.linalg as la
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import serial
from time import sleep
from scipy.linalg import hankel
from scipy.signal import butter, lfilter, freqz



class Radar(object):
    def __init__(self,samples,radar,time,samplingRate):
        self.samples = samples
        self.radar = radar
        self.time = time
        self.samplingRate = samplingRate
        self.p = 5
        self.nfft = 512
        self.list = []


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

            self.radar = self.graphFilterResults()
            n = 4*2
            fig, ax = plt.subplots(int(n/2), n)
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

                self.corrMtrx = self.getcorrMtrx(x=array,m= 35)
                frequency, psd,eigenvals = self.musicAlg()

                #xf, yf = self.fft(array)


                r = counter // n
                c = counter % n
                #ax[r][c].plot(array)

                radarObject = RadarData(array,psd,eigenvals)
                self.list.append(radarObject)

                list1.append(eigenvals)

                ax[r][c].plot(eigenvals)
                ax[r][c+1].plot(frequency,np.log(abs(psd)))

                #ax[r][c + 1].plot(xf, yf)

                """if(counter1 == 1):
                    sum1 = sum(eigenvals)
                    print('Explained Variance for Eigenvalues')

                    for i in range(0, len(eigenvals)):
                        print('The %d eigenvalue has a weight of %d'%(i, (eigenvals[i]/sum1) * 100))
                """

                #diff = Radar.diffCalc(self,list(eigenvals))

                #ax[r][c + 2].plot(diff)


                #if counter1 == 1:
                    #break
                    
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
        for i in range(1,len(list1)):
            list2.append(list1[i] - list1[i-1])
        return list2

    def fft(self,array):
        yf = fft(array,n=self.nfft)
        xf = np.linspace(0.0, self.samplingRate/2,self.nfft/2)
        return xf, abs(yf[0:self.nfft/2])

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

        print(len(corrMatrix))
        print(len(corrMatrix[0]))
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

        sum = 1 / sum

        sum = sum[0:self.nfft // 2]

        return frequencyVector,sum,s

    def graphFilterResults(self):
        order = 6
        cutoff = 2

        b, a = Radar.butter_lowpass(cutoff, self.samplingRate, order)

        w, h = freqz(b, a, worN=8000)
        plt.subplot(2, 1, 1)
        plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
        plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
        plt.axvline(cutoff, color='k')
        plt.xlim(0, 0.5 * fs)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()

        y = Radar.butter_lowpass_filter(self.radar, cutoff, fs, order)

        plt.subplot(2, 1, 2)
        plt.plot(self.time, self.radar, 'b-', label='data')
        plt.plot(self.time, y, 'g-', linewidth=2, label='filtered data')
        plt.xlabel('Time [sec]')
        plt.grid()
        plt.legend()

        plt.subplots_adjust(hspace=0.35)
        plt.show()
        return y

    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = Radar.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def testSpectrum(self,data):
        corrMtrx  = self.getcorrMtrx(data, 30)
        return self.musicAlg2(corrMtrx)

    def musicAlg2(self,corrMtrx):
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


class RadarData(object):

    def __init__(self,array,power,vals):
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
    x =  0.12 * np.sin(1.2 * np.pi * (n)) + 0.12* np.sin(0.6 * np.pi *(n))
    mean = np.mean(x)
    std = np.std(x)

    noise = np.random.normal(mean, std, len(x))
    x1 = x +  noise

    radar = Radar(radar=x1,samples=N,samplingRate=sRate,time=n)

    fs,radardata,timedata = radar.getVariables()
    print(fs, len(radardata), len(timedata))

    radar.slidingwindow()