import time
import Adafruit_ADS1x15
from threading import Thread

class ADCThread:
	def __init__(self,address,gain,numthreads =1):
		self.i2caddress = address
		self.adc = Adafruit_ADS1x15.ADS1115(address)
		self.GAIN = gain
		self.numthreads = numthreads
		self.interrupt = False
		self.stopA1 = False
		self.stopA2 = False
		self.stopA3 = False
		self.adcval1 = 0
		self.adcval2 = 0
		self.adcval3 = 0
		self.adcval4 = 0
		
	def start(self):
		Thread(target= self.channel1,args =()).start()
		#Thread(target = self.channel2,args = ()).start()
	
	def channel1(self):
		i = 0
		i1 = 1
		while True:
			
			if(self.interrupt):
				return
			
			else:
				self.adcval1 = self.adc.read_adc(0, gain=self.GAIN)
				self.adcval2 = self.adc.read_adc(1, gain=self.GAIN)
				self.adcval3 = self.adc.read_adc(2, gain=self.GAIN)
				self.adcval4 = self.adc.read_adc(3, gain=self.GAIN)
				
	
	def channel2(self):
		i = 1
		
		while True:
			
			if(self.interrupt):
				return
			
			else:
				print(self.adc.read_adc(i, gain=self.GAIN))
				
	def getADCVal1(self):
		return self.adcval1
	
	def getADCVal2(self):
		return self.adcval2
	
	def getADCVal3(self):
		return self.adcval3
	
	def getADCVal4(self):
		return self.adcval4
		
	def stop(self):
		self.interrupt = True
			
			
		
