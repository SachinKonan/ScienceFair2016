import time
import numpy as np
from sinwave import dacThreadSin
from triwave import dacThreadTriangle

if __name__ == "__main__":
    #/home/pi/Documents/PythonProjects/ScienceFair2016/DAC/simptest.py
    dac1 = dacThreadSin(0x63)
    dac2 = dacThreadTriangle(0x62)
    dac1.start()
    dac2.start()
    
    """
    print('Press Ctrl-C to quit...')
    dut = True
    while True:
        #valueset(int(input('Value is: ')))
        #squarewave(0.1,dut)
        
        dac1
        
        if(dut == True):
            dut = False
        else:
            dut = True
    """
    
        

        
