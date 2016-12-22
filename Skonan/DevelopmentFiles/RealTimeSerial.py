import serial
import time
import matplotlib.pyplot as plt
import numpy as np

port = 'COM3'
n = 1000
N = n * 2
radarData = [0 for h in range(0,n)]
timeData = [0 for h in range(0,n)]
ser = serial.Serial(port,9600)
time.sleep(2)



x=list()
y=list()

plt.ion()

counter1 = 0
if(input("Do you want to start communication?") == 'y'):
    print("Ok Im Starting Serial COmmunicatiton")
    if(ser.is_open):
        for i in range(0,N):
            ser.write(b"a")

            if(counter1 %2 ==0): y.append(float(str(ser.readline(), 'utf-8')) * 5.0 / 1023.0)
            else: x.append(float(str(ser.readline(), 'utf-8')) * 10 ** -6)

            counter1+=1
            if(counter1 != 0 and counter1 % 2 == 0): plt.scatter(x[i],y[i])
            plt.pause(0.05)

        while True:
            plt.pause(0.05)

    else:
        print("Serial port is not open")

samples = 0;
samples1 = 0;
for i in range(0,N):
    if(i % 2 == 0):
        radarData[samples] = float(str(x[i], 'utf-8'))* 5.0/1023.0
        samples = samples + 1
    else:
        timeData[samples1] = float(str(x[i], 'utf-8'))
        samples1 = samples1 + 1

radar = np.asarray(radarData)
time = np.asarray(timeData)

samplingRate = 10**6/np.mean(np.diff(time))

print(samplingRate)

plt.plot(radar)
plt.show()