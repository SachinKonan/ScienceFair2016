import numpy as np
import matplotlib.pyplot as plt


n= 2000
x =  np.sin(1.2 * np.pi * (n)) + np.sin(0.6 * np.pi *(n))
mean = np.mean(x)
std = np.std(x)

noise = np.random.normal(mean, std, len(x))
x1 = x +  noise

plt.plot(x1)
plt.show()