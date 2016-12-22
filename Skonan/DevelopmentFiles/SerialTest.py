import serial
import time
import matplotlib.pyplot as plt
import numpy as np

port = 'COM3'
n = 2000
N = n * 2
x = [0 for h in range(0,N)]
radarData = [0 for h in range(0,n)]
radarData2 =  [0 for h in range(0,n)]
timeData = [0 for h in range(0,n)]

ser = serial.Serial(port,9600)
time.sleep(2)

counter1 = 0
#if(input("Do you want to start communication?") == 'y'):
    #print("Ok Im Starting Serial COmmunicatiton")
if(ser.is_open):
    for i in range(0,N):
        ser.write(b"a")
        x[i] = ser.readline()
        print(x[i])
else:
    print("Serial port is not open")

samples = 0
samples1 = 0
samples2 = 0

count1 = 0
count2 = 0
count3 = 0


for i in range(0,N):
    if(i % 2 == 0):
        radarData[samples] = float(str(x[i], 'utf-8'))
        samples = samples + 1
    else:
        #timeData[samples1] = float(str(x[i], 'utf-8'))
        timeData[samples1] = float(str(x[i], 'utf-8'))
        samples1 = samples1 + 1
"""
for i in range(0,N):
    if(i == samples-1):
        radarData[count1] = (float(str(x[i], 'utf-8'))* 5.0/1023.0)
        count1+=1
        samples = samples + 3
    elif(i == samples1-1):
        #timeData[samples1] = float(str(x[i], 'utf-8'))
        radarData2[count2] = (float(str(x[i], 'utf-8')) * 5.0 / 1023.0)
        count2+=1
        samples1 = samples1 + 3
    elif(i == samples2-1):
        timeData[count3] = (float(str(x[i], 'utf-8')))
        count3+=1
        samples2 = samples2 + 3
"""
radar = np.asarray(radarData)
timeD = np.asarray(timeData)



samplingRate = 10**6/np.mean(np.diff(timeD))



np.savetxt('Pics/controlradar.out',radar)
np.savetxt('Pics/controltime.out',timeD)


plt.plot(timeD,radar)
plt.show()


