import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725

class dacThreadSin:
    def __init__(self,address):
        self.i2caddress = address
        self.interrupt = False
        self.dac = Adafruit_MCP4725.MCP4725(self.i2caddress)
        
    def start(self):
        print('Starting DAC Thread')
        Thread(target = self.cycle, args = ()).start()
        
    def cycle(self):
        while True:
            
            if(self.interrupt):
                return
            
            for i in range(0, 360):
                radians = i * np.pi/180
                val = np.sin(radians) * 2048 + 2048
                #print(round(val))
                self.dac.set_voltage(int(round(val)),True)
                time.sleep(0.01)
    
    def stop(self):
        self.interrupt = True

    
        
