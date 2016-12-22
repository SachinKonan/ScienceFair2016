import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = plt.axes(xlim=(0, 5 * np.pi), ylim=(-10,10))
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Cancelled Output')
x = np.linspace(0, 5 * np.pi, 100000)
y = 5  * np.sin(2 * np.pi *1* (x ) + np.pi) +  3 * np.sin(2 * np.pi *0.3 * (x ) + np.pi)
plt.plot(x,y)
plt.savefig('Cancelled.png')
plt.show()