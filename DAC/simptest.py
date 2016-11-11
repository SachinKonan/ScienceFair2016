# Simple demo of setting the output voltage of the MCP4725 DAC.
# Will alternate setting 0V, 1/2VDD, and VDD each second.
# Author: Tony DiCola
# License: Public Domain
import time
import numpy as np
from threading import Thread
import Adafruit_MCP4725


def squarewave(dutys,dut):
	if(dut == True):
		dac.set_voltage(4096,True)
		time.sleep(dutys)

	else:
		dac.set_voltage(0,True)
		time.sleep(dutys)
		
def valueset(val):
	if(val >= 0 and val <= 4096):
		dac.set_voltage(val,True)
		
def triwave():
	for i in range(0, 2):
		for x in range(0, 4096):
			if( i == 0):
				val = x
			elif(i == 1):
				val = 4096 - x
			dac1.set_voltage(val,True)
def cycle():
	for i in range(0, 360):
			radians = i * np.pi/180
			val = np.sin(radians) * 2048 + 2048
			print(round(val))
			dac2.set_voltage(int(round(val)),True)
			time.sleep(0.01)

class dacThread:
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

if __name__ == "__main__":
	#python '/home/pi/Documents/PythonProjects/DAC/simptest.py'
	dac1 = dacThread(0x63)
	
	dac2 = dacThread(0x62)
	
	dac1.start()
	time.sleep(1.5)
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
	
		

		
