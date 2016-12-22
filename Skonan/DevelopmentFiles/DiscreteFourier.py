from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt

N = 256# num of samples
Fs = 64#sampling rate
T = 1.0 / Fs # sampling period ,nmnnnmnn mm
x = np.linspace(0.0, N*T, N)
y = np.sin(2*np.pi * x) + np.sin(1 * np.pi * x)  # sample signal

nig = np.random.normal(np.mean(y), np.std(y))

y = y + nig
yf = fft(y)#db
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)#frequency domain ranges from 0 to fs/2 becaus the result of the fft is symmetrix about the halfway point
plt.plot(xf, 2.0/N * np.abs(yf[0:N/2])) #plots the absolute value just getting rid of the complex values in the result of the FFT
plt.grid()
plt.show()